from datetime import datetime

from pydantic import BaseModel, Field


class PostCreateForm(BaseModel):
    title: str = Field(
        max_length=128,
        title='Post Title',
        description='Post Unique Title'
    )
    body: str = Field(
        title='Post Body',
        description='Post Body',
    )

    class Config:
        orm_mode = True



class PostDetail(PostCreateForm):
    pk: int = Field(
        ge=1,
        title='Post ID',
        description='Post Unique ID'
    )
    date_create: datetime = Field(
        title='Post Date Created',
        description='Post Date Created',
    )
    author_id: int = Field(
        ge=1,
        title='Post Author ID',
        description='Post Author Unique ID',
    )
