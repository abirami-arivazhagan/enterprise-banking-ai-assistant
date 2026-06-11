from fastapi import APIRouter
import yaml
router = APIRouter()
@router.get("/roles")
def get_roles():
    with open(
        "config/roles.yaml",
        "r"
    ) as file:
        roles = yaml.safe_load(file)
    return roles