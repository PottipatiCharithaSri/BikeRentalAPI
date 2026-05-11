from enum import Enum

class ReturnReason(str, Enum):
    COMPLETED = "COMPLETED"
    EARLY_RETURN = "EARLY_RETURN"
    BIKE_ISSUE = "BIKE_ISSUE"
    CUSTOMER_REQUEST = "CUSTOMER_REQUEST"