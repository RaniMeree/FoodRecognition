from enum import Enum
import os

primary_path = os.path.dirname(os.path.abspath(__file__))


class Tags(Enum):
    users = "Users"
