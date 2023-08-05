from magicdb.Models import MagicModel
from pydantic import EmailStr


class CurrentUser(MagicModel):
    uid: str
    phone_number: str = None
    email: EmailStr = None
    email_verified: bool = None
    auth_time: int
    iat: int
    exp: int
    iss: str = None
    aud: str = None
    user_id: str = None
    sub: str = None
    firebase: dict = {}
