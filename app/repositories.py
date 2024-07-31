from app.database import new_session, PaymentsORM, Sendler
from sqlalchemy import delete, select, update

class UserRepository:

    @classmethod
    async def add_transaction(cls, user_id: int, label: str, subscribe_type: int, username: str):
        async with new_session() as session:

            existing_transactions = await session.execute(
                select(PaymentsORM).where(
                    PaymentsORM.user_id == user_id,
                    PaymentsORM.check == False
                )
            )

            existing_transactions = existing_transactions.scalars().all()

            if existing_transactions:
                await session.execute(
                    delete(PaymentsORM).where(PaymentsORM.user_id == user_id)
                )
                await session.commit()

            transaction = PaymentsORM(
                user_id=user_id,
                label=label,
                subscribe_type=subscribe_type,
                username=username
            )
            session.add(transaction)
            await session.commit()

    @classmethod
    async def delete_transaction(cls, user_id: int, label: str, subscribe_type: int):
        async with new_session() as session:
            query = delete(PaymentsORM).where(PaymentsORM.user_id == user_id, PaymentsORM.label == label, PaymentsORM.subscribe_type == subscribe_type)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_payment_status(cls, user_id: int, label: str):
        async with new_session() as session:
            query = select(PaymentsORM).where(PaymentsORM.user_id == user_id, PaymentsORM.label == label)
            result = await session.execute(query)
            user = result.scalars().all()
            return user

    @classmethod
    async def update_payment_status(cls, user_id: int, label: str, subscribe_type: int):
        async with new_session() as session:
            query = update(PaymentsORM).where(PaymentsORM.user_id == user_id, PaymentsORM.label == label, PaymentsORM.subscribe_type == subscribe_type).values(check=True)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def add_user_to_sendlist(cls, user_id: int):
        async with new_session() as session:
            q = select(Sendler).filter_by(user_id=user_id)
            result = await session.execute(q)
            user_in_sendlist = result.scalars().first()
            if user_in_sendlist:
                return
            sendler = Sendler(user_id=user_id)
            session.add(sendler)
            await session.commit()

    @classmethod
    async def get_all_users_from_sendlist(cls):
        async with new_session() as session:
            q = select(Sendler)
            result = await session.execute(q)
            users = result.scalars().all()
            return users