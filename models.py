from pydantic import BaseModel, constr, EmailStr, validator
from typing import Union

USERNAME_REGEX = r"^[a-zA-Z0-9_-]+$"
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&_-]+$'
class CreateUser(BaseModel):
    """
    Represents a user account creation request.

    Attributes:
        username: The username for the new account. Must be between 3 and 50 characters long, and can only contain
            alphanumeric characters, underscores, and hyphens.
        email : The email address for the new. Must be a valid email address.
        password: The password for the new account. Must be a Strong password between 8 to 100 chars
    """
    username: constr(min_length=3, max_length=50, regex=USERNAME_REGEX)
    email: EmailStr
    password: constr(min_length=8, max_length=100, regex=PASSWORD_REGEX)

class LoginUser(BaseModel):
    """
    Represents a user account login request.

    Attributes:
        username (Union[str, None]): The username for the login request. Optional, but at least one of username or
            email must be provided.
        email (Union[EmailStr, None]): The email address for the login request. Optional, but at least one of username
            or email must be provided.
        password (str): The password for the login request. Must be between 8 and 100 characters long
    """
    username: Union[constr(min_length=3, max_length=50, regex=USERNAME_REGEX), None]
    email: Union[EmailStr, None]
    password:constr(min_length=8, max_length=100, regex=PASSWORD_REGEX)
    @validator('email', 'username')
    def email_or_username(cls, v, values):
        if v is None and values.get('username') is None and values.get('email') is None:
            raise ValueError("Either email or username is required")
        return v

class CreateQuote(BaseModel):
    author: constr(min_length=3, max_length=50, regex=USERNAME_REGEX)
    text: constr(min_length=10, max_length=255)


class LoginResponse(BaseModel):
    message:str
    username: str
    access_token: str

