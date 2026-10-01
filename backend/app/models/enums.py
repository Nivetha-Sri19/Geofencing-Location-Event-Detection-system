from enum import StrEnum
class UserRole(StrEnum):
    ADMIN="admin"; OPERATOR="operator"; VIEWER="viewer"
class GeofenceType(StrEnum):
    CIRCLE="circle"; POLYGON="polygon"
class GeofenceState(StrEnum):
    INSIDE="inside"; OUTSIDE="outside"
class GeofenceEventType(StrEnum):
    ENTER="enter"; EXIT="exit"; INSIDE="inside"; OUTSIDE="outside"
