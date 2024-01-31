import asyncio
import sys

import pytest

from ....domains.permission.api import PermissionAPI
from ....domains.permission.types import Permission
from ....domains.role.api import RoleAPI
from ....domains.role.role_attribute.api import RoleAttributeAPI
from ....domains.role.role_attribute.types import (
    RoleAttribute,
)
from ....domains.role.role_permission.api import RolePermissionAPI
from ....domains.role.role_permission.types import RolePermission
from ....domains.role.types import Role, RoleCreate, RoleUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def role_client(authup_client):
    return RoleAPI(Role, authup_client.http, prefix="roles")


@pytest.fixture
def role_attribute_client(authup_client):
    return RoleAttributeAPI(RoleAttribute, authup_client.http, prefix="role-attributes")


@pytest.fixture
def role_permission_client(authup_client):
    return RolePermissionAPI(
        RolePermission, authup_client.http, prefix="role-permissions"
    )


@pytest.fixture
def permission_client(authup_client):
    return PermissionAPI(Permission, authup_client.http, prefix="permissions")


@pytest.mark.asyncio
async def test_role_get_many(role_client):
    role = await role_client.create(RoleCreate(name="test_role"))

    roles = await role_client.get_many()
    assert roles
    assert isinstance(roles[0], Role)

    print(f"\n{[r.id for r in await role_client.get_many()]}")

    await role_client.delete(role.id)


# @pytest.mark.asyncio
# async def test_role_attribute_get_many(role_attribute_client, role_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     await role_attribute_client.create(RoleAttributeCreate(name=os.urandom(8).hex(), role_id=role.id))
#
#     role_attributes = await role_attribute_client.get_many()
#     assert role_attributes
#     assert isinstance(role_attributes[0], RoleAttribute)
#
#     print(f"\n{[ra.id for ra in await role_attribute_client.get_many()]}")
#
#     await role_client.delete(role.id)
#
#
# @pytest.mark.asyncio
# async def test_role_permission_get_many(role_permission_client, role_client, permission_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     permission = await permission_client.create(
#         PermissionCreate(name="test_role_permission")
#     )
#     await role_permission_client.create(
#         RolePermissionCreate(role_id=role.id, power=999, permission_id=permission.id)
#     )
#
#     role_permissions = await role_permission_client.get_many()
#     assert role_permissions
#     assert isinstance(role_permissions[0], RolePermission)
#
#     print(f"\n{[rp.id for rp in await role_permission_client.get_many()]}")
#
#     await role_client.delete(role.id)
#     await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_role_get_one(role_client):
    role = await role_client.create(RoleCreate(name="test_role"))
    test_role = await role_client.get_one(role.id)
    assert role
    assert isinstance(role, Role)
    assert role.id == test_role.id
    assert role.name == test_role.name

    await role_client.delete(role.id)


# @pytest.mark.asyncio
# async def test_role_attribute_get_one(role_attribute_client, role_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     role_attribute = await role_attribute_client.create(
#         RoleAttributeCreate(name=os.urandom(8).hex(), role_id=role.id)
#     )
#     test_role_attribute = await role_attribute_client.get_one(role_attribute.id)
#     assert role_attribute
#     assert isinstance(role_attribute, RoleAttribute)
#     assert role_attribute.id == test_role_attribute.id
#     assert role_attribute.name == test_role_attribute.name
#
#     await role_client.delete(role.id)
#
#
# @pytest.mark.asyncio
# async def test_role_permission_get_one(role_permission_client, role_client, permission_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     permission = await permission_client.create(
#         PermissionCreate(name="test_role_permission")
#     )
#     role_permission = await role_permission_client.create(
#         RolePermissionCreate(role_id=role.id, power=999, permission_id=permission.id)
#     )
#     test_role_permission = await role_permission_client.get_one(role_permission.id)
#     assert role_permission
#     assert isinstance(role_permission, RolePermission)
#     assert role_permission.id == test_role_permission.id
#     assert role_permission.role_id == test_role_permission.role_id
#     assert role_permission.power == test_role_permission.power
#     assert role_permission.permission_id == test_role_permission.permission_id
#
#     await role_client.delete(role.id)
#     await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_role_create(role_client):
    test_role = RoleCreate(name="test_role")

    role = await role_client.create(test_role)
    assert role
    assert isinstance(role, Role)
    assert role.name == test_role.name
    print(f"\nID: {role.id}")
    print(f"\nName: {role.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_role.created_at}\n\tUpdated: {test_role.updated_at}"
    )

    await role_client.delete(role.id)


# @pytest.mark.asyncio
# async def test_role_attribute_create(role_attribute_client, role_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     test_role_attribute = RoleAttributeCreate(name=os.urandom(8).hex(), role_id=role.id)
#
#     role_attribute = await role_attribute_client.create(test_role_attribute)
#     assert role_attribute
#     assert isinstance(role_attribute, RoleAttribute)
#     assert role_attribute.name == test_role_attribute.name
#     print(f"\nID: {role_attribute.id}")
#     print(f"\nName: {role_attribute.name}")
#     print(
#         f"\nDatetime:\n\tCreated: {test_role_attribute.created_at}\n\tUpdated: {test_role_attribute.updated_at}"
#     )
#
#     await role_client.delete(role.id)
#
#
# @pytest.mark.asyncio
# async def test_role_permission_create(role_permission_client, role_client, permission_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     permission = await permission_client.create(
#         PermissionCreate(name="test_role_permission")
#     )
#     test_role_permission = RolePermissionCreate(role_id=role.id, power=999, permission_id=permission.id)
#
#     role_permission = await role_permission_client.create(test_role_permission)
#     assert role_permission
#     assert isinstance(role_permission, RolePermission)
#     assert role_permission.role_id == test_role_permission.role_id
#     assert role_permission.power == test_role_permission.power
#     assert role_permission.permission_id == test_role_permission.permission_id
#     print(f"\nID: {role_permission.id}")
#     print(
#         f"\nDatetime:\n\tCreated: {test_role_permission.created_at}\n\tUpdated: {test_role_permission.updated_at}"
#     )
#
#     await role_client.delete(role.id)
#     await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_role_update(role_client):
    role = await role_client.create(RoleCreate(name="test_role"))

    updated_name = "test_role_updated"
    test_role_updated = RoleUpdate(name=updated_name)
    updated_role = await role_client.update(role.id, test_role_updated)

    assert updated_role
    assert isinstance(updated_role, Role)
    assert updated_role.name == updated_name
    print(f"\nID: {role.id}")
    print(f"\nName:\n\tOriginal: {role.name}\n\tUpdated: {updated_role.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_role_updated.created_at}\n\tUpdated: {test_role_updated.updated_at}"
    )

    await role_client.delete(role.id)


# @pytest.mark.asyncio
# async def test_role_attribute_update(role_attribute_client, role_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     role_attribute = await role_attribute_client.create(
#         RoleAttributeCreate(name=os.urandom(8).hex(), role_id=role.id, value="before")
#     )
#
#     updated_value = "after"
#     test_role_attribute_updated = RoleAttributeUpdate(
#         name=role_attribute.name, role_id=role_attribute.id, value=updated_value
#     )
#     updated_role_attribute = await role_attribute_client.update(role_attribute.id, test_role_attribute_updated)
#
#     assert updated_role_attribute
#     assert isinstance(updated_role_attribute, RoleAttribute)
#     assert updated_role_attribute.value == updated_value
#     print(f"\nID: {role_attribute.id}")
#     print(f"\nName:\n\tOriginal: {role_attribute.value}\n\tUpdated: {updated_role_attribute.value}")
#     print(
#         f"\nDatetime:\n\tCreated: {test_role_attribute_updated.created_at}\n\t"
#         f"Updated: {test_role_attribute_updated.updated_at}"
#     )
#
#     await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_role_delete(role_client):
    role = await role_client.create(RoleCreate(name="test_role"))
    deleted_id = await role_client.delete(role.id)
    print(f"\nRole generated: id={role.id}")
    print(f"Delete role with id={deleted_id}")
    print(
        f"Deleted id in list of current roles: {deleted_id in [r.id for r in await role_client.get_many()]}"
    )
    assert deleted_id == role.id
    assert deleted_id not in [r.id for r in await role_client.get_many()]


# @pytest.mark.asyncio
# async def test_role_attribute_delete(role_attribute_client, role_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     role_attribute = await role_attribute_client.create(
#         RoleAttributeCreate(name=os.urandom(8).hex(), role_id=role.id)
#     )
#     deleted_id = await role_attribute_client.delete(role_attribute.id)
#     print(f"\nRoleAttribute generated: id={role_attribute.id}")
#     print(f"Delete role attribute with id={deleted_id}")
#     print(
#         f"Deleted id in list of current role attributes: "
#         f"{deleted_id in [ra.id for ra in await role_attribute_client.get_many()]}"
#     )
#     assert deleted_id == role_attribute.id
#     assert deleted_id not in [ra.id for ra in await role_attribute_client.get_many()]
#
#     await role_client.delete(role.id)
#
#
# @pytest.mark.asyncio
# async def test_role_permission_delete(role_permission_client, role_client, permission_client):
#     role = await role_client.create(RoleCreate(name="test_role"))
#     permission = await permission_client.create(
#         PermissionCreate(name="test_role_permission")
#     )
#     role_permission = await role_permission_client.create(
#         RolePermissionCreate(role_id=role.id, power=999, permission_id=permission.id)
#     )
#     deleted_id = await role_permission_client.delete(role_permission.id)
#     print(f"\nRolePermission generated: id={role_permission.id}")
#     print(f"Delete role permission with id={deleted_id}")
#     print(
#         f"Deleted id in list of current role permissions: "
#         f"{deleted_id in [rp.id for rp in await role_permission_client.get_many()]}"
#     )
#     assert deleted_id == role_permission.id
#     assert deleted_id not in [rp.id for rp in await role_permission_client.get_many()]
#
#     await role_client.delete(role.id)
#     await permission_client.delete(permission.id)
