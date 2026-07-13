from enum import IntEnum

class ActionType(IntEnum):
    CREATE_DEVICE = 1
    UPDATE_DEVICE = 2
    ASSIGN_DEVICE = 3

class RoleType(IntEnum):
    ADMIN = 1
    EMPLOYEE = 2