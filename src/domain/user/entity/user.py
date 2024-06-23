from dataclasses import dataclass

from src.domain.user.value_object.login import UserLogin
from src.domain.user.value_object.password import UserPassword


@dataclass
class User:
    login: UserLogin
    password: UserPassword
    
