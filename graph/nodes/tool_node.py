from app_tools.tool_registry import (
    TOOL_REGISTRY
)

import re

from graph.nodes.memory_node import (
    memory_manager
)

from memory.dialog_state import (
    dialog_state_store
)

from memory.upload_context import (
    upload_context_store
)

# =========================================================
# TOOL NODE
# =========================================================

def tool_node(state):

    raw_question = (
        state.get(
            "question"
        )
        or
        state.get(
            "query",
            ""
        )
    )

    state["question"] = raw_question

    question = (
        raw_question
        .lower()
    )

    session_id = (
        state.get(
            "session_id"
        )
        or
        "default"
    )

    state["citations"] = []

    dialog_state = dialog_state_store.get(
        session_id
    )

    latest_upload = upload_context_store.get_latest(
        session_id
    )

    def is_generic_complaint_request():

        generic_phrases = [
            "i need to raise a complaint",
            "i want to raise a complaint",
            "i need to file a complaint",
            "i want to file a complaint",
            "raise a complaint",
            "create a complaint",
            "register a complaint",
            "file a complaint",
            "i need to create a complaint",
            "i want to create a complaint"
        ]

        cleaned = question.strip().rstrip(".")

        return cleaned in generic_phrases

    def is_low_value_issue(text):

        cleaned = text.strip().lower()

        generic_complaint_phrases = [
            "i need to raise a complaint",
            "i want to raise a complaint",
            "i need to file a complaint",
            "i want to file a complaint",
            "raise a complaint",
            "create a complaint",
            "register a complaint",
            "file a complaint",
            "i need to create a complaint",
            "i want to create a complaint"
        ]

        vague_issue_phrases = [
            "facing this issue",
            "i am facing this issue",
            "i'm facing this issue",
            "this issue",
            "same issue",
            "that issue",
            "issue",
            "problem",
            "facing problem",
            "i have an issue",
            "i have a problem"
        ]

        return (
            not cleaned
            or
            cleaned.rstrip(".") in generic_complaint_phrases
            or
            cleaned.rstrip(".") in vague_issue_phrases
            or
            cleaned in [
                "hi",
                "hello",
                "hey",
                "ok",
                "okay",
                "yes",
                "no"
            ]
            or
            len(cleaned.split()) < 3
        )

    def low_value_issue_reply():

        if latest_upload:

            return (
                "I can see that you uploaded a file, but I still need the issue details before I create a complaint ID. Please describe what the screenshot shows, such as payment failed, account blocked, card charged twice, refund delayed, ATM cash not dispensed, or service not resolved. If it is transaction-related, include date/time, amount, and reference/UTR if available. Do not share OTP, PIN, CVV, passwords, or full card/account numbers."
            )

        return (
            "I can raise that complaint for you, but I need the actual issue first. Please describe what happened, such as a failed payment, blocked account, wrong charge, delayed refund, or service problem."
        )

    def uploaded_issue_context():

        if not latest_upload:

            return None

        preview = (
            latest_upload.get(
                "preview"
            )
            or
            ""
        ).strip()

        if not preview:

            return None

        return (
            f"Uploaded file {latest_upload.get('filename')}: {preview}"
        )

    def needs_complaint_details(text):

        issue_text = text.lower()

        return (
            "payment" in issue_text
            or
            "transaction" in issue_text
            or
            "upi" in issue_text
            or
            "card" in issue_text
            or
            "debit" in issue_text
            or
            "charge" in issue_text
            or
            "refund" in issue_text
            or
            "atm" in issue_text
        )

    def has_enough_complaint_details(text):

        lowered = text.lower()

        has_date_or_time = bool(
            re.search(
                r"\b(\d{1,2}[:/-]\d{1,2}|today|yesterday|am|pm|morning|evening|night)\b",
                lowered
            )
        )

        has_amount_or_reference = bool(
            re.search(
                r"(rs\.?|₹|inr|amount|utr|ref|reference|transaction id|txn|rrn|\d{3,})",
                lowered
            )
        )

        return (
            has_date_or_time
            and
            has_amount_or_reference
        )

    def previous_user_issue():

        memory = memory_manager.get_memory(
            session_id
        )

        for message in reversed(
            memory.load_context()
        ):

            if message.get("role") != "user":

                continue

            content = message.get(
                "content",
                ""
            )

            lowered = content.lower()

            if (
                "complaint" not in lowered
                and
                "ticket" not in lowered
                and
                "list" not in lowered
            ):

                return content

        return raw_question

    def has_create_complaint_intent():

        return (
            "complaint" in question
            and
            (
                "raise" in question
                or
                "create" in question
                or
                "register" in question
                or
                "file" in question
            )
        )

    def has_list_complaint_intent():

        return (
            (
                "list" in question
                and
                "complaint" in question
            )
            or
            "complaint number" in question
            or
            "ticket" in question
        )

    def format_complaints(complaints):

        if not complaints:

            return "No complaints found for this chat session."

        lines = [
            "Here are the complaints raised in this chat:"
        ]

        for complaint in complaints:

            lines.append(
                (
                    f"- Ticket {complaint['ticket_id']}: "
                    f"{complaint['issue_type']} - "
                    f"{complaint['description']}"
                )
            )

        return "\n".join(
            lines
        )

    def create_complaint():

        tool = TOOL_REGISTRY[
            "create_complaint"
        ]

        description = raw_question

        if (
            "raise" in question
            and
            "complaint" in question
            and
            len(question.split()) <= 8
        ):

            description = previous_user_issue()

        if dialog_state.get("pending") == "complaint_issue":

            description = raw_question

            if is_low_value_issue(
                raw_question
            ) and uploaded_issue_context():

                description = uploaded_issue_context()

        issue_type = "General"

        issue_text = description.lower()

        if (
            "payment" in issue_text
            or
            "blocked" in issue_text
            or
            "frozen" in issue_text
            or
            "unblock" in issue_text
            or
            "transaction" in issue_text
            or
            "upi" in issue_text
            or
            "card" in issue_text
            or
            "refund" in issue_text
            or
            "atm" in issue_text
        ):

            issue_type = "Account access / payment failure"

        result = tool(

            issue_type=issue_type,

            description=description,

            session_id=session_id
        )

        return result

    def list_complaints():

        tool = TOOL_REGISTRY[
            "list_complaints"
        ]

        result = tool(
            session_id=session_id
        )

        return result[
            "complaints"
        ]

    def extract_numbers():

        return [

            float(
                value.replace(
                    ",",
                    ""
                )
            )

            for value in re.findall(
                r"\d[\d,]*(?:\.\d+)?",
                raw_question
            )
        ]

    print("\n[TOOL NODE EXECUTED]\n")

    # =====================================================
    # BLOCK CARD
    # =====================================================

    if dialog_state.get("pending") == "complaint_details":

        original_issue = dialog_state.get(
            "issue",
            ""
        )

        if is_low_value_issue(
            raw_question
        ) and uploaded_issue_context():

            raw_question = uploaded_issue_context()

        combined_description = (
            f"{original_issue}. Details: {raw_question}"
        )

        if not has_enough_complaint_details(
            raw_question
        ):

            state["answer"] = (
                "I can register this complaint, but I need a little more detail so the ticket is useful. Please share the transaction date or time, amount, and any reference/UTR/transaction ID if available. Do not share OTP, PIN, CVV, passwords, or full card/account numbers."
            )

            state["tool_used"] = (
                "complaint_detail_clarification"
            )

        else:

            raw_question = combined_description
            question = raw_question.lower()

            result = create_complaint()

            dialog_state_store.clear(
                session_id
            )

            state["answer"] = (
                (
                    "I have registered the complaint with the details you provided.\n\n"
                    f"Complaint ID: {result['ticket_id']}\n"
                    f"Issue: {result['issue_type']}\n"
                    f"Description: {result['description']}\n\n"
                    "Please keep this complaint ID for follow-up."
                )
            )

            state["tool_used"] = (
                "create_complaint"
            )

    elif dialog_state.get("pending") == "complaint_issue":

        if is_low_value_issue(raw_question) and not uploaded_issue_context():

            state["answer"] = (
                low_value_issue_reply()
            )

            state["tool_used"] = (
                "complaint_clarification"
            )

        else:

            if is_low_value_issue(
                raw_question
            ) and uploaded_issue_context():

                raw_question = uploaded_issue_context()
                question = raw_question.lower()

            if needs_complaint_details(
                raw_question
            ):

                dialog_state_store.set(
                    session_id,
                    {
                        "pending": "complaint_details",
                        "issue": raw_question
                    }
                )

                if uploaded_issue_context():

                    state["answer"] = (
                        (
                            "I reviewed the uploaded file and can use it as the issue context for your complaint.\n\n"
                            "Before I create the complaint ID, please share the transaction date or time, amount, and any reference/UTR/transaction ID if available. "
                            "Do not share OTP, PIN, CVV, passwords, or full card/account numbers."
                        )
                    )

                else:

                    state["answer"] = (
                        "I can raise that complaint. Please share the transaction date or time, amount, and any reference/UTR/transaction ID if available. Do not share OTP, PIN, CVV, passwords, or full card/account numbers."
                    )

                state["tool_used"] = (
                    "complaint_detail_clarification"
                )

                return state

            result = create_complaint()

            dialog_state_store.clear(
                session_id
            )

            state["answer"] = (
                (
                    "I have registered the complaint based on the issue you described.\n\n"
                    f"Complaint ID: {result['ticket_id']}\n"
                    f"Issue: {result['issue_type']}\n"
                    f"Description: {result['description']}\n\n"
                    "Please keep this complaint ID for follow-up. A support executive can use it to track the case, verify details securely, and update you on the next action."
                )
            )

            state["tool_used"] = (
                "create_complaint"
            )

    elif question.strip() in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        state["answer"] = (
            (
                "Hello, welcome to Nexus Bank support. I can help you understand banking policies, payment or card issues, account access problems, complaints, and uploaded document queries.\n\n"
                "Tell me what you are trying to do or what problem you are facing, and I will guide you step by step. Please avoid sharing OTPs, PINs, CVV, full card numbers, or full account numbers here."
            )
        )

        state["tool_used"] = (
            "greeting"
        )

    elif "block" in question and "card" in question:

        tool = TOOL_REGISTRY[
            "block_card"
        ]

        result = tool(

            card_last4="1234",

            reason="User Request"
        )

        state["answer"] = (
            result["message"]
        )

        state["tool_used"] = (
            "block_card"
        )

    elif (

        "loan" in question
        and
        (
            "eligibility" in question
            or
            "eligible" in question
            or
            "calculate" in question
        )

    ):

        numbers = extract_numbers()

        if len(numbers) < 3:

            state["answer"] = (
                (
                    "I can estimate loan eligibility, but I need three details: monthly salary, existing monthly EMI, and credit score.\n\n"
                    "For example: `monthly salary 80000, existing EMI 10000, credit score 760`."
                )
            )

            state["tool_used"] = (
                "loan_eligibility_clarification"
            )

        else:

            tool = TOOL_REGISTRY[
                "calculate_loan_eligibility"
            ]

            result = tool(

                monthly_salary=numbers[0],

                existing_emi=numbers[1],

                credit_score=int(numbers[2])
            )

            state["answer"] = (
                (
                    "Here is an indicative loan eligibility estimate based on the details provided:\n\n"
                    f"- Eligible EMI capacity: Rs. {result['eligible_emi']:,.0f} per month\n"
                    f"- Estimated loan amount: Rs. {result['estimated_loan_amount']:,.0f}\n"
                    f"- Credit score considered: {result['credit_score']}\n\n"
                    "This is only an estimate. Final approval can depend on bank policy, income verification, credit bureau checks, existing liabilities, and internal risk rules."
                )
            )

            state["tool_used"] = (
                "calculate_loan_eligibility"
            )

    # =====================================================
    # COMPLAINT
    # =====================================================

    elif has_create_complaint_intent():

        if is_generic_complaint_request():

            previous_issue = previous_user_issue()

            if is_low_value_issue(
                previous_issue
            ):

                dialog_state_store.set(
                    session_id,
                    {
                        "pending": "complaint_issue"
                    }
                )

                state["answer"] = (
                    (
                        "Of course, I can help raise a complaint. I just need the actual issue before I create a complaint ID, so the ticket is mapped correctly.\n\n"
                        "Please describe what happened in one or two lines. For example: payment failed, account blocked, card charged twice, refund delayed, ATM cash not dispensed, or service request not resolved. "
                        "Once you share that, I will register the complaint against the right issue type."
                    )
                )

                state["tool_used"] = (
                    "complaint_clarification"
                )

                return state

            result = create_complaint()

            state["answer"] = (
                (
                    "I have registered the complaint based on the issue you already described.\n\n"
                    f"Complaint ID: {result['ticket_id']}\n"
                    f"Issue: {result['issue_type']}\n"
                    f"Description: {result['description']}\n\n"
                    "Please keep this complaint ID for follow-up. A support executive can use it to track the case and continue the resolution process securely."
                )
            )

            state["tool_used"] = (
                "create_complaint"
            )

            return state

        if needs_complaint_details(
            raw_question
        ) and not has_enough_complaint_details(
            raw_question
        ):

            dialog_state_store.set(
                session_id,
                {
                    "pending": "complaint_details",
                    "issue": raw_question
                }
            )

            state["answer"] = (
                "I can raise that complaint. Please share the transaction date or time, amount, and any reference/UTR/transaction ID if available. Do not share OTP, PIN, CVV, passwords, or full card/account numbers."
            )

            state["tool_used"] = (
                "complaint_detail_clarification"
            )

            return state

        result = create_complaint()

        answer = (
            (
                f"Complaint created: {result['ticket_id']}\n"
                f"Issue: {result['issue_type']}\n"
                f"Description: {result['description']}"
            )
        )

        if has_list_complaint_intent():

            answer = (
                f"{answer}\n\n"
                f"{format_complaints(list_complaints())}"
            )

        state["answer"] = answer

        state["tool_used"] = (
            "create_complaint"
        )

    elif has_list_complaint_intent():

        state["answer"] = format_complaints(
            list_complaints()
        )

        state["tool_used"] = (
            "list_complaints"
        )

    elif (

        "unblock" in question
        or
        "blocked account" in question
        or
        "account blocked" in question
        or
        "frozen account" in question
        or
        "account frozen" in question

    ):

        tool = TOOL_REGISTRY[
            "unblock_account"
        ]

        result = tool(
            reason=raw_question
        )

        state["answer"] = (
            result["message"]
        )

        state["tool_used"] = (
            "unblock_account"
        )

    else:

        state["answer"] = (
            "Tool unavailable."
        )

    return state
