import asyncio
import os
import sys

import pytest

from ....domains.permission.api import PermissionAPI
from ....domains.permission.types import Permission, PermissionCreate
from ....domains.realm.api import RealmAPI
from ....domains.realm.types import Realm, RealmCreate
from ....domains.robot.api import RobotAPI
from ....domains.robot.robot_permission.api import RobotPermissionAPI
from ....domains.robot.robot_permission.types import (
    RobotPermission,
    RobotPermissionCreate,
)
from ....domains.robot.robot_role.api import RobotRoleAPI
from ....domains.robot.robot_role.types import RobotRole, RobotRoleCreate
from ....domains.robot.types import Robot, RobotCreate, RobotUpdate
from ....domains.role.api import RoleAPI
from ....domains.role.types import Role, RoleCreate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def robot_client(authup_client):
    return RobotAPI(Robot, authup_client.http, prefix="robots")


@pytest.fixture
def robot_permission_client(authup_client):
    return RobotPermissionAPI(
        RobotPermission, authup_client.http, prefix="robot-permissions"
    )


@pytest.fixture
def robot_role_client(authup_client):
    return RobotRoleAPI(RobotRole, authup_client.http, prefix="robot-roles")


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
async def test_robot_get_many(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )

    robots = await robot_client.get_many()
    assert robots
    assert isinstance(robots[0], Robot)

    print(f"\n{[r.id for r in await robot_client.get_many()]}")

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_robot_permission_get_many(
    robot_permission_client, robot_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_robot_permission")
    )
    await robot_permission_client.create(
        RobotPermissionCreate(robot_id=robot.id, power=999, permission_id=permission.id)
    )

    robot_permissions = await robot_permission_client.get_many()
    assert robot_permissions
    assert isinstance(robot_permissions[0], RobotPermission)

    print(f"\n{[rp.id for rp in await robot_permission_client.get_many()]}")

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_robot_role_get_many(
    robot_role_client, robot_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_robot_role"))
    await robot_role_client.create(RobotRoleCreate(robot_id=robot.id, role_id=role.id))

    robot_roles = await robot_role_client.get_many()
    assert robot_roles
    assert isinstance(robot_roles[0], RobotRole)

    print(f"\n{[rr.id for rr in await robot_role_client.get_many()]}")

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_robot_get_one(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    test_robot = await robot_client.get_one(robot.id)  # , '?include=user,realm,secret')
    assert robot
    assert isinstance(robot, Robot)
    assert robot.id == test_robot.id
    assert robot.name == test_robot.name

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_robot_permission_get_one(
    robot_permission_client, robot_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_robot_permission")
    )
    robot_permission = await robot_permission_client.create(
        RobotPermissionCreate(robot_id=robot.id, power=999, permission_id=permission.id)
    )
    test_robot_permission = await robot_permission_client.get_one(robot_permission.id)
    assert robot_permission
    assert isinstance(robot_permission, RobotPermission)
    assert robot_permission.id == test_robot_permission.id
    assert robot_permission.robot_id == test_robot_permission.robot_id
    assert robot_permission.power == test_robot_permission.power
    assert robot_permission.permission_id == test_robot_permission.permission_id

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_robot_role_get_one(
    robot_role_client, robot_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_robot_role"))
    robot_role = await robot_role_client.create(
        RobotRoleCreate(robot_id=robot.id, role_id=role.id)
    )
    test_robot_role = await robot_role_client.get_one(
        robot_role.id
    )  # , '?include=user,realm,secret')
    assert robot_role
    assert isinstance(robot_role, RobotRole)
    assert robot_role.id == test_robot_role.id
    assert robot_role.robot_id == test_robot_role.robot_id
    assert robot_role.role_id == test_robot_role.role_id

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_robot_create(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    test_robot = RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    robot = await robot_client.create(test_robot)
    assert robot
    assert isinstance(robot, Robot)
    assert robot.name == test_robot.name
    print(f"\nID: {robot.id}")
    print(f"\nName: {robot.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_robot.created_at}\n\tUpdated: {test_robot.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_robot_permission_create(
    robot_permission_client, robot_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_robot_permission")
    )
    test_robot_permission = RobotPermissionCreate(
        robot_id=robot.id, power=999, permission_id=permission.id
    )
    robot_permission = await robot_permission_client.create(test_robot_permission)
    assert robot_permission
    assert isinstance(robot_permission, RobotPermission)
    assert robot_permission.robot_id == test_robot_permission.robot_id
    assert robot_permission.power == test_robot_permission.power
    assert robot_permission.permission_id == test_robot_permission.permission_id
    print(f"\nID: {robot_permission.id}")
    print(
        f"\nDatetime:\n\tCreated: {test_robot_permission.created_at}\n\tUpdated: {test_robot_permission.updated_at}"
    )

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_robot_role_create(
    robot_role_client, robot_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_robot_role"))
    test_robot_role = RobotRoleCreate(robot_id=robot.id, role_id=role.id)
    robot_role = await robot_role_client.create(test_robot_role)
    assert robot_role
    assert isinstance(robot_role, RobotRole)
    assert robot_role.robot_id == test_robot_role.robot_id
    assert robot_role.role_id == test_robot_role.role_id
    print(f"\nID: {robot_role.id}")
    print(
        f"\nDatetime:\n\tCreated: {test_robot_role.created_at}\n\tUpdated: {test_robot_role.updated_at}"
    )

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_robot_update(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    updated_name = os.urandom(8).hex()
    test_robot_updated = RobotUpdate(
        name=updated_name, secret="test", realm_id=realm.id
    )
    updated_robot = await robot_client.update(robot.id, test_robot_updated)

    assert updated_robot
    assert isinstance(updated_robot, Robot)
    assert updated_robot.name == updated_name
    print(f"\nID: {robot.id}")
    print(f"\nName:\n\tOriginal: {robot.name}\n\tUpdated: {updated_robot.name}")
    print(
        f"\nDatetime:\n\tCreated: {test_robot_updated.created_at}\n\tUpdated: {test_robot_updated.updated_at}"
    )

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_robot_delete(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    deleted_id = await robot_client.delete(robot.id)
    print(f"\nRobot generated: id={robot.id}")
    print(f"Delete robot with id={deleted_id}")
    print(
        f"Deleted id in list of current robots: {deleted_id in [r.id for r in await robot_client.get_many()]}"
    )
    assert deleted_id == robot.id
    assert deleted_id not in [r.id for r in await robot_client.get_many()]

    await realm_client.delete(realm.id)


@pytest.mark.asyncio
async def test_robot_permission_delete(
    robot_permission_client, robot_client, realm_client, permission_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    permission = await permission_client.create(
        PermissionCreate(name="test_robot_permission")
    )
    robot_permission = await robot_permission_client.create(
        RobotPermissionCreate(robot_id=robot.id, power=999, permission_id=permission.id)
    )
    deleted_id = await robot_permission_client.delete(robot_permission.id)
    print(f"\nRobotPermission generated: id={robot_permission.id}")
    print(f"Delete robot permission with id={deleted_id}")
    print(
        f"Deleted id in list of current robot permissions: "
        f"{deleted_id in [rp.id for rp in await robot_permission_client.get_many()]}"
    )
    assert deleted_id == robot_permission.id
    assert deleted_id not in [rp.id for rp in await robot_permission_client.get_many()]

    await realm_client.delete(realm.id)
    await permission_client.delete(permission.id)


@pytest.mark.asyncio
async def test_robot_role_delete(
    robot_role_client, robot_client, realm_client, role_client
):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    role = await role_client.create(RoleCreate(name="test_robot_role"))
    robot_role = await robot_role_client.create(
        RobotRoleCreate(robot_id=robot.id, role_id=role.id)
    )
    deleted_id = await robot_role_client.delete(robot_role.id)
    print(f"\nRobotRole generated: id={robot_role.id}")
    print(f"Delete robot role with id={deleted_id}")
    print(
        f"Deleted id in list of current robot roles: "
        f"{deleted_id in [rr.id for rr in await robot_role_client.get_many()]}"
    )
    assert deleted_id == robot_role.id
    assert deleted_id not in [rr.id for rr in await robot_role_client.get_many()]

    await realm_client.delete(realm.id)
    await role_client.delete(role.id)


@pytest.mark.asyncio
async def test_robot_integrity(robot_client, realm_client):
    realm = await realm_client.create(RealmCreate(name=os.urandom(8).hex()))
    robot = await robot_client.create(
        RobotCreate(name=os.urandom(8).hex(), secret="test", realm_id=realm.id)
    )
    robot_integrity = await robot_client.integrity(robot.id)

    assert robot_integrity == 202

    await realm_client.delete(realm.id)
