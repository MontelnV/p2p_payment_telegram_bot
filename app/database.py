from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import pytz

engine = create_async_engine(
    "sqlite+aiosqlite:///users.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class PaymentsORM(Base):
    __tablename__ = 'payments'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    username: Mapped[Optional[str]] = mapped_column(default=None)
    label: Mapped[Optional[str]] = mapped_column(default=None)
    check: Mapped[bool] = mapped_column(default=False)
    subscribe_type: Mapped[Optional[int]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))

class Sendler(Base):
    __tablename__ = 'sendler'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
