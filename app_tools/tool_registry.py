from app_tools.account_tools import (
    AccountTools
)

from app_tools.complaint_tools import (
    ComplaintTools
)

TOOL_REGISTRY = {
    "block_card":
    AccountTools.block_card,
    "freeze_account":
    AccountTools.freeze_account,
    "unblock_account":
    AccountTools.unblock_account,
    "calculate_loan_eligibility":
    AccountTools.calculate_loan_eligibility,
    "create_complaint":
    ComplaintTools.create_complaint,
    "list_complaints":
    ComplaintTools.list_complaints
}
