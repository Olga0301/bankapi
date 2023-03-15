from inspect import iscoroutinefunction
from typing import Any, Type, Sequence

from sqlalchemy import Column, INT, VARCHAR, DECIMAL, ForeignKey, BOOLEAN, \
    create_engine, select, Row, RowMapping
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker, Session


class Base(DeclarativeBase):
    pk = Column('id', INT, primary_key=True)

    engine = create_engine('postgresql://admin:admin@localhost:5432/bank')
    session = sessionmaker(bind=engine)

    async_engine = create_async_engine('postgresql+asyncpg://admin:admin@localhost:5432/bank')
    async_session = async_sessionmaker(bind=async_engine)

    @staticmethod
    def create_session(func):
        def wrapper(*args, **kwargs):
            with Base.session() as session:
                return func(*args, **kwargs, session=session)

        async def async_wrapper(*args, **kwargs):
            async with Base.async_session() as session:
                return await func(*args, **kwargs, session=session)

        return async_wrapper if iscoroutinefunction(func) else wrapper

    @declared_attr
    def __tablename__(cls):
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

    @create_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_session
    async def get(cls, pk: Any, session: AsyncSession = None) -> Type["Base"]:
        return await session.get(cls, pk)

    @classmethod
    @create_session
    async def select(
            cls,
            *args,
            order_by: Any = 'id',
            limit: int = None,
            offset: int = None,
            session: AsyncSession = None
    ) -> Sequence[Row | RowMapping | Any]:
        objs = await session.scalars(
            select(cls)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
            .filter(*args)
        )
        return objs.all()

    @create_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()

    def dict(self) -> dict:
        data = self.__dict__
        data['id'] = data['pk']
        del data['pk']
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']
        return data
