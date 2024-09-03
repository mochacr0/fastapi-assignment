import enum


class TaskPriority(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TaskStatus(enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class CompanyMode(enum.Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"


class Role(enum.Enum):
    USER = "User"
    ADMIN = "Admin"


class SortDirection(enum.Enum):
    ASC = "Asc"
    DESC = "Desc"
