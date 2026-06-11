from fastapi import APIRouter
from fastapi import Query

import yaml


router = APIRouter()


@router.get("/auth/context")

def auth_context(
    role: str = Query(
        default="l1_agent"
    )
):

    with open(
        "config/roles.yaml",
        "r"
    ) as file:

        config = yaml.safe_load(
            file
        )

    roles = config.get(
        "roles",
        {}
    )

    if role not in roles:

        role = "l1_agent"

    role_config = roles.get(
        role,
        {}
    )

    return {

        "project": config.get(
            "project",
            {}
        ),

        "role": role,

        "permissions": role_config.get(
            "permissions",
            []
        ),

        "allowed_doc_types": role_config.get(
            "allowed_doc_types",
            []
        )
    }
