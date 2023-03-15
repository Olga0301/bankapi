from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str = Field(
        title='JWT',
        description='Json Web Token'
    )
    token_type: str = Field(
        title='Token Type',
        description='Token Type'
    )
