from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.database.database import async_engine, async_session_factory
from bot.database.exceptions import DatabaseError
from bot.database.models import Base, UsersORM, WeatherReportsORM


class AsyncDBClient:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user(tg_id) -> UsersORM:
        async with async_session_factory() as session:
            query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
            if user is None:
                session.add(UsersORM(tg_id=tg_id))
                await session.commit()
                user = (await session.execute(query)).scalar()
                if user is None:
                    raise DatabaseError('User does not exist')
            return user

    @staticmethod
    async def set_user_city(tg_id, city):
        async with async_session_factory() as session:
            query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
            user.city = city
            await session.commit()

    @staticmethod
    async def get_user_city(tg_id):
        async with async_session_factory() as session:
            query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
            return user.city

    @staticmethod
    async def create_weather_report(
            tg_id: int,
            temp: float,
            feels_like: float,
            wind_speed: float,
            pressure_mm: float,
            city: str,
            country: str,
            visibility: float,
            weather_condition: str
    ):
        async with async_session_factory() as session:
            user = await db_client.add_user(tg_id)
            report = WeatherReportsORM(
                owner=user.id,
                temp=temp,
                feels_like=feels_like,
                wind_speed=wind_speed,
                pressure_mm=pressure_mm,
                city=city,
                country=country,
                visibility=visibility,
                weather_condition=weather_condition
            )
            session.add(report)
            await session.commit()

    @staticmethod
    async def get_user_reports(tg_id):
        async with async_session_factory() as session:
            query = (
                select(UsersORM)
                .filter(UsersORM.tg_id == tg_id)
                .options(selectinload(UsersORM.reports))
            )
            result = await session.execute(query)
            user = result.scalar()
            return user.reports

    @staticmethod
    async def get_report(report_id):
        async with async_session_factory() as session:
            report = await session.get(WeatherReportsORM, report_id)
            return report

    @staticmethod
    async def delete_user_report(report_id):
        async with async_session_factory() as session:
            report = await session.get(WeatherReportsORM, report_id)
            await session.delete(report)
            await session.commit()

    @staticmethod
    async def get_all_users():
        async with async_session_factory() as session:
            query = select(UsersORM).options(selectinload(UsersORM.reports))
            users = (await session.execute(query)).scalars().all()
            return users

    @staticmethod
    async def get_all_reports():
        async with async_session_factory() as session:
            query = select(WeatherReportsORM)
            reports = (await session.execute(query)).scalars().all()
            return reports


db_client = AsyncDBClient()
