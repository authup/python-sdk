import asyncio
import os
import sys

import pytest

from ....domains.permission.api import PermissionAPI
from ....domains.permission.types import Permission, PermissionCreate
from ....domains.realm.api import RealmAPI
from ....domains.realm.types import Realm, RealmCreate
from ....domains.role.api import RoleAPI
from ....domains.role.types import Role, RoleCreate
from ....domains.user.api import UserAPI
from ....domains.user.types import User, UserCreate, UserUpdate
from ....domains.user.user_attribute.api import UserAttributeAPI
from ....domains.user.user_attribute.types import (
    UserAttribute,
    UserAttributeCreate,
    UserAttributeUpdate,
)
from ....domains.user.user_permission.api import UserPermissionAPI
from ....domains.user.user_permission.types import UserPermission, UserPermissionCreate
from ....domains.user.user_role.api import UserRoleAPI
from ....domains.user.user_role.types import UserRole, UserRoleCreate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def user_client(authup_client):
    return UserAPI(User, authup_client.http, prefix="users")


@pytest.fixture
def user_attribute_client(authup_client):
    return UserAttributeAPI(UserAttribute, authup_client.http, prefix="user-attributes")


@pytest.fixture
def user_permission_client(authup_client):
    return UserPermissionAPI(
        UserPermission, authup_client.http, prefix="user-permissions"
    )


@pytest.fixture
def user_role_client(authup_client):
    return UserRoleAPI(UserRole, authup_client.http, prefix="user-roles")


@pytest.fixture
def realm_client(authup_client):
    return RealmAPI(Realm, authup_client.http, prefix="realms")


@pytest.fixture
def permission_client(authup_client):
    return PermissionAPI(Permission, authup_client.http, prefix="permissions")


@pytest.fixture
def role_client(authup_client):
    return RoleAPI(Role, authup_client.http, prefix="roles")


@pytest.mark.asyncio
async def test_user_get_many(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )

    users = await user_client.get_many()
    assert users
    assert isinstance(users[0], User)

    print(f"\n{[u.id for u in await user_client.get_many()]}")

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_attribute_get_many(
    user_attribute_client, user_client, realm_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    await user_attribute_client.create(
        UserAttributeCreate(
            name=os.urandom(8).hex(), user_id=user.id, realm_id=realm.id
        )
    )

    user_attributes = await user_attribute_client.get_many()
    assert user_attributes
    assert isinstance(user_attributes[0], UserAttribute)

    print(f"\n{[ua.id for ua in await user_attribute_client.get_many()]}")

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_permission_get_many(
    user_permission_client, user_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_user_permission")
    )
    await user_permission_client.create(
        UserPermissionCreate(user_id=user.id, power=999, permission_id=permission.id)
    )

    user_permissions = await user_permission_client.get_many()
    assert user_permissions
    assert isinstance(user_permissions[0], UserPermission)

    print(f"\n{[up.id for up in await user_permission_client.get_many()]}")

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_user_role_get_many(
    user_role_client, user_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_user_role"))
    await user_role_client.create(UserRoleCreate(user_id=user.id, role_id=role.id))

    user_roles = await user_role_client.get_many()
    assert user_roles
    assert isinstance(user_roles[0], UserRole)

    print(f"\n{[ur.id for ur in await user_role_client.get_many()]}")

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_user_get_one(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    test_user = await user_client.get_one(user.id)
    assert user
    assert isinstance(user, User)
    assert user.id == test_user.id
    assert user.name == test_user.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_attribute_get_one(user_attribute_client, user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    user_attribute = await user_attribute_client.create(
        UserAttributeCreate(
            name=os.urandom(8).hex(), user_id=user.id, realm_id=realm.id
        )
    )

    test_user_attribute = await user_attribute_client.get_one(user_attribute.id)
    assert user_attribute
    assert isinstance(user_attribute, UserAttribute)
    assert user_attribute.id == test_user_attribute.id
    assert user_attribute.name == test_user_attribute.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_permission_get_one(
    user_permission_client, user_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_user_permission")
    )
    user_permission = await user_permission_client.create(
        UserPermissionCreate(user_id=user.id, power=999, permission_id=permission.id)
    )

    test_user_permission = await user_permission_client.get_one(user_permission.id)
    assert user_permission
    assert isinstance(user_permission, UserPermission)
    assert user_permission.id == test_user_permission.id
    assert user_permission.user_id == test_user_permission.user_id
    assert user_permission.power == test_user_permission.power
    assert user_permission.permission_id == test_user_permission.permission_id

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_user_role_get_one(
    user_role_client, user_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_user_role"))
    user_role = await user_role_client.create(
        UserRoleCreate(user_id=user.id, role_id=role.id)
    )

    test_user_role = await user_role_client.get_one(user_role.id)
    assert user_role
    assert isinstance(user_role, UserRole)
    assert user_role.id == test_user_role.id
    assert user_role.user_id == test_user_role.user_id
    assert user_role.role_id == test_user_role.role_id

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_user_create(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    test_user = UserCreate(
        name=os.urandom(8).hex(), display_name="test", realm_id=realm.id
    )

    user = await user_client.create(test_user)
    assert user
    assert isinstance(user, User)
    assert user.name == test_user.name
    print(f"\nID: {user.id}")
    print(f"\nName: {user.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_user.created_at}\n\tUpdated: {test_user.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_attribute_create(user_attribute_client, user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    test_user_attribute = UserAttributeCreate(
        name=os.urandom(8).hex(), user_id=user.id, realm_id=realm.id
    )

    user_attribute = await user_attribute_client.create(test_user_attribute)
    assert user_attribute
    assert isinstance(user_attribute, UserAttribute)
    assert user_attribute.name == test_user_attribute.name

    print(f"\nID: {user_attribute.id}")
    print(f"\nName: {user_attribute.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_user_attribute.created_at}\n\tUpdated: {test_user_attribute.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_permission_create(
    user_permission_client, user_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_user_permission")
    )
    test_user_permission = UserPermissionCreate(
        user_id=user.id, power=999, permission_id=permission.id
    )

    user_permission = await user_permission_client.create(test_user_permission)
    assert user_permission
    assert isinstance(user_permission, UserPermission)
    assert user_permission.user_id == test_user_permission.user_id
    assert user_permission.power == test_user_permission.power
    assert user_permission.permission_id == test_user_permission.permission_id
    print(f"\nID: {user_permission.id}")
    print(
        f"\nDatetime:\n\tCreated: {test_user_permission.created_at}\n\tUpdated: {test_user_permission.updated_at}"
    )

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_user_role_get_create(
    user_role_client, user_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_user_role"))
    test_user_role = UserRoleCreate(user_id=user.id, role_id=role.id)

    user_role = await user_role_client.create(test_user_role)
    assert user_role
    assert isinstance(user_role, UserRole)
    assert user_role.user_id == test_user_role.user_id
    assert user_role.role_id == test_user_role.role_id
    print(f"\nID: {user_role.id}")
    print(
        f"\nDatetime:\n\tCreated: {test_user_role.created_at}\n\tUpdated: {test_user_role.updated_at}"
    )

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_user_update(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )

    updated_name = os.urandom(8).hex()
    test_user_updated = UserUpdate(name=updated_name, display_name=user.display_name)
    updated_user = await user_client.update(user.id, test_user_updated)

    assert updated_user
    assert isinstance(updated_user, User)
    assert updated_user.name == updated_name
    print(f"\nID: {user.id}")
    print(f"\nName:\n\tOriginal: {user.name}\n\tUpdated: {updated_user.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_user_updated.created_at}\n\tUpdated: {test_user_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_attribute_update(user_attribute_client, user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    user_attribute = await user_attribute_client.create(
        UserAttributeCreate(
            name=os.urandom(8).hex(), user_id=user.id, realm_id=realm.id
        )
    )

    updated_name = os.urandom(8).hex()
    test_user_attribute_updated = UserAttributeUpdate(
        name=updated_name, user_id=user.id, realm_id=realm.id
    )
    updated_user_attribute = await user_attribute_client.update(
        user_attribute.id, test_user_attribute_updated
    )

    assert updated_user_attribute
    assert isinstance(updated_user_attribute, UserAttribute)
    assert updated_user_attribute.name == updated_name
    print(f"\nID: {user_attribute.id}")
    print(
        f"\nName:\n\tOriginal: {user_attribute.name}\n\tUpdated: {updated_user_attribute.name}"
    )
    print(
        f"\nDatetime:\n\tCreated: {test_user_attribute_updated.created_at}\n\t"
        f"Updated: {test_user_attribute_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_delete(user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    deleted_id = await user_client.delete(user.id)
    print(f"\nUser generated: id={user.id}")
    print(f"Delete user with id={deleted_id}")
    print(
        f"Deleted id in list of current users: {deleted_id in [u.id for u in await user_client.get_many()]}"
    )
    assert deleted_id == user.id
    assert deleted_id not in [u.id for u in await user_client.get_many()]

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_attribute_delete(user_attribute_client, user_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    user_attribute = await user_attribute_client.create(
        UserAttributeCreate(
            name=os.urandom(8).hex(), user_id=user.id, realm_id=realm.id
        )
    )
    deleted_id = await user_attribute_client.delete(user_attribute.id)
    print(f"\nUserAttribute generated: id={user_attribute.id}")
    print(f"Delete user attribute with id={deleted_id}")
    print(
        f"Deleted id in list of current user attributes: "
        f"{deleted_id in [ua.id for ua in await user_attribute_client.get_many()]}"
    )
    assert deleted_id == user_attribute.id
    assert deleted_id not in [ua.id for ua in await user_attribute_client.get_many()]

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_user_permission_delete(
    user_permission_client, user_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_user_permission")
    )
    user_permission = await user_permission_client.create(
        UserPermissionCreate(user_id=user.id, power=999, permission_id=permission.id)
    )
    deleted_id = await user_permission_client.delete(user_permission.id)
    print(f"\nUserPermission generated: id={user_permission.id}")
    print(f"Delete user permission with id={deleted_id}")
    print(
        f"Deleted id in list of current user permissions: "
        f"{deleted_id in [up.id for up in await user_permission_client.get_many()]}"
    )
    assert deleted_id == user_permission.id
    assert deleted_id not in [up.id for up in await user_permission_client.get_many()]

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_user_role_get_delete(
    user_role_client, user_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    user = await user_client.create(
        UserCreate(name=os.urandom(8).hex(), display_name="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_user_role"))

    user_role = await user_role_client.create(
        UserRoleCreate(user_id=user.id, role_id=role.id)
    )
    deleted_id = await user_role_client.delete(user_role.id)
    print(f"\nUserRole generated: id={user_role.id}")
    print(f"Delete user role with id={deleted_id}")
    print(
        f"Deleted id in list of current user roles: {deleted_id in [ur.id for ur in await user_role_client.get_many()]}"
    )
    assert deleted_id == user_role.id
    assert deleted_id not in [ur.id for ur in await user_role_client.get_many()]

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)
