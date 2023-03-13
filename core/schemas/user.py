from pydantic import BaseModel, Field, EmailStr, root_validator

from ..settings import PWD_CONTEXT


class RegisterForm(BaseModel):
    email: EmailStr = Field(
        title='User Email',
        description='User Unique Email'
    )
    username: str = Field(
        title='Username',
        description='Unique Username',
        max_length=128,
        min_length=2
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )
    repeat_password: str = Field(
        title='Repeat Password',
        description='Repeat Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )

    @root_validator(pre=True)
    def validator(cls, values: dict) -> dict:
        if values.get('password') != values.get('repeat_password'):
            raise ValueError('пароли не совпадают')

        if values.get('username').lower() in values.get('password').lower():
            raise ValueError('имя пользователя не должно содержаться в пароле')

        if values.get('email').lower().split('@')[0] in values.get('password').lower():
            raise ValueError('почта не должна содержаться в пароле')

        return values


class UserInfo(BaseModel):
    pk: int = Field(ge=1, default=None)
    email: EmailStr = Field(
        title='User Email',
        description='User Unique Email'
    )
    username: str = Field(
        title='Username',
        description='Unique Username',
        max_length=128,
        min_length=2
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        default=None,
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )
    hashed_password: str = Field(
        default=None,
        max_length=512
    )

    @root_validator
    def validator(cls, values: dict) -> dict:
        if values.get('password') and not values.get('hashed_password'):
            # register
            values['hashed_password'] = PWD_CONTEXT.hash(values.get('password'))
        elif values.get('password') and values.get('hashed_password'):
            # login
            if not PWD_CONTEXT.verify(values.get('password'), values.get('hashed_password')):
                raise ValueError('не верный пароль')
        return values

    class Config:
        orm_mode = True


class LoginForm(BaseModel):
    email: EmailStr = Field(
        title='User Email',
        description='User Unique Email'
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )
