from enum import Enum


class DomainType(Enum):
    CLIENT = "client"
    CLIENT_SCOPE = "clientScope"
    IDENTITY_PROVIDER = "identityProvider"
    IDENTITY_PROVIDER_ACCOUNT = "identityProviderAccount"
    IDENTITY_PROVIDER_ATTRIBUTE = "identityProviderAttribute"
    IDENTITY_PROVIDER_ROLE = "identityProviderRole"
    PERMISSION = "permission"
    REALM = "realm"
    ROBOT = "robot"
    ROBOT_PERMISSION = "robotPermission"
    ROBOT_ROLE = "robotRole"
    ROLE = "role"
    ROLE_ATTRIBUTE = "roleAttribute"
    ROLE_PERMISSION = "rolePermission"
    SCOPE = "scope"
    USER = "user"
    USER_ATTRIBUTE = "userAttribute"
    USER_PERMISSION = "userPermission"
    USER_ROLE = "userRole"


class DomainEventName(Enum):
    CREATED = "created"
    DELETED = "deleted"
    UPDATED = "updated"


class DomainEventSubscriptionName(Enum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
