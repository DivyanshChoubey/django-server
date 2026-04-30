from rest_framework import status


class ResponseStatuses:
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    FORBIDDEN = status.HTTP_403_FORBIDDEN
    NO_CONTENT = status.HTTP_204_NO_CONTENT
    CONFLICT = status.HTTP_409_CONFLICT
    UNPROCESSABLE_ENTITY = status.HTTP_422_UNPROCESSABLE_ENTITY

class Constants:
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

    USER_TYPES = {
        USER: "User",
        ADMIN: "Admin",
        SUPER_ADMIN: "Super Admin",
    }

class DailyReportConstants:
    DRAFT = "draft"
    SUBMITTED = "submitted"

    STATUS_CHOICES = (
        (DRAFT, "Draft"),
        (SUBMITTED, "Submitted"),
    )


class TaskConstants:
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    STATUS_CHOICES = (
        (NOT_STARTED, "Not Started"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    )
