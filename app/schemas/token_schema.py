from pydantic import BaseModel as PydanticSchema


class TokenDto(PydanticSchema):
    access_token: str
    token_type: str
