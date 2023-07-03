from enum import Enum


class FileOwnerTypes(str, Enum):
    EVENT = 'EVENT'
    TASK = 'TASK'
    USER = 'USER'
    PROCESS = 'PROCESS'
