import logging
from typing import List

from authup.schemas.token import Permission


def check_permissions(
    permissions: List[Permission],
    required_permissions: List[Permission],
) -> bool:
    """
    Check if a token has the required permissions
    :param permissions:
    :param required_permissions:
    :return:
    """
    if not required_permissions:
        return True

    if not permissions:
        return False

    return _check_permissions(permissions, required_permissions)


def _check_permissions(
    token_permissions: List[Permission],
    required_permissions: List[Permission],
) -> bool:
    """
    Compare the required permissions with the token permissions, taking inverse and power into account
    :param token_permissions:
    :param token_permissions:
    :return:
    """

    token_perm_dict = {p.name: p for p in token_permissions}

    authorized = True

    missed_permissions = []

    for required_permission in required_permissions:
        # the required permission is not in the token permissions
        token_permission = token_perm_dict.get(required_permission.name)
        if not token_permission:
            authorized = False
            missed_permissions.append(required_permission)
            continue

        # check for inverse and compare power
        if required_permission.inverse:
            if token_permission.power >= required_permission.power:
                authorized = False
                missed_permissions.append(required_permission.name)
        else:
            if token_permission.power < required_permission.power:
                authorized = False
                missed_permissions.append(required_permission.name)

        # check condition
        # todo: implement condition check
    logging.info(f"Missed permissions: {missed_permissions}")
    return authorized
