
class AccountTools:

    @staticmethod
    def block_card(
        card_last4,
        reason
    ):
        return {
            "status": "success",
            "message":
            f"Card ending with "
            f"{card_last4} blocked successfully.",
            "reason": reason
        }
    @staticmethod
    def freeze_account(
        account_number
    ):
        return {
            "status": "success",
            "message":
            f"Account {account_number} frozen."
        }
    @staticmethod
    def unblock_account(
        reason
    ):
        return {
            "status":
            "requires_verification",
            "message":
            (
                "I understand you want the account unblocked. For security reasons, I cannot directly unblock or change an account status from chat. "
                "The safest next step is to raise a support complaint for account access review, then the bank team can verify your identity and check why the account was blocked or frozen. "
                "Please describe the issue, such as the failed payment message, when it happened, and whether your account or card appears blocked. Do not share OTP, PIN, CVV, full card number, or full account number."
            ),

            "reason":
            reason
        }
    @staticmethod
    def calculate_loan_eligibility(
        monthly_salary,
        existing_emi,
        credit_score
    ):
        eligible_emi = (
            monthly_salary * 0.4
        ) - existing_emi

        eligible_emi = max(
            eligible_emi,
            0
        )
        estimated_loan = (
            eligible_emi * 40
        )
        return {

            "status":
            "success",

            "eligible_emi":
            eligible_emi,

            "estimated_loan_amount":
            estimated_loan,

            "credit_score":
            credit_score
        }
