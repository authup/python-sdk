import asyncio
import os
import sys

import pytest

from ....domains.realm.api import RealmClient
from ....domains.realm.types import Realm, RealmCreate
from ....domains.robot.api import RobotClient
from ....domains.robot.types import Robot, RobotCreate, RobotUpdate

if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def robot_client(authup_client):
    return RobotClient(Robot, authup_client.http, prefix="robots")


@pytest.fixture
def realm_client(authup_client):
    return RealmClient(Realm, authup_client.http, prefix="realms")


@pytest.mark.asyncio
async def test_robot_get_many(robot_client):
    robots = await robot_client.get_many()
    assert robots
    assert isinstance(robots[0], Robot)

    print(f"\n{[r.id for r in await robot_client.get_many()]}")


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
