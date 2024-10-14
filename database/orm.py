from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.database import (sync_engine, session_factory, async_engine,
                               async_session_factory)
from database.models import Base, UsersORM, WeatherReportsORM


class SyncDBClient:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def add_user(tg_id):
        with session_factory() as session:
            result = session.query(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = result.first()
            if user is None:
                session.add(UsersORM(tg_id=tg_id))
                session.commit()

    @staticmethod
    def set_user_city(tg_id, city):
        with session_factory() as session:
            result = session.query(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = result.first()
            user.city = city
            session.commit()

    @staticmethod
    def get_user_city(tg_id):
        with session_factory() as session:
            result = session.query(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = result.first()
            return user.city

    @staticmethod
    def create_weather_report(
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
        with session_factory() as session:
            result = session.query(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = result.first()
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
            session.commit()

    @staticmethod
    def get_user_reports(tg_id):
        with session_factory() as session:
            result = session.query(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = result.first()
            return user.reports

    @staticmethod
    def get_report(report_id):
        with session_factory() as session:
            report = session.get(WeatherReportsORM, report_id)
            return report

    @staticmethod
    def delete_user_report(report_id):
        with session_factory() as session:
            report = session.get(WeatherReportsORM, report_id)
            session.delete(report)
            session.commit()

    @staticmethod
    def get_all_users():
        with session_factory() as session:
            users = session.query(UsersORM).options(
                selectinload(UsersORM.reports)
            ).all()
            return users

    @staticmethod
    def get_all_reports():
        with session_factory() as session:
            reports = session.query(WeatherReportsORM).all()
            return reports

    @staticmethod
    def add_fake_users():
        with session_factory() as session:
            user_1 = UsersORM(tg_id=100, city="Томск")
            user_2 = UsersORM(tg_id=200, city="Минск")
            user_3 = UsersORM(tg_id=300, city="Хабаровск")
            user_4 = UsersORM(tg_id=400, city="Пермь")
            user_5 = UsersORM(tg_id=500, city="Астана")
            user_6 = UsersORM(tg_id=600, city="Мурманск")
            session.add_all([user_1, user_2, user_3, user_4, user_5, user_6])
            session.commit()


class AsyncDBClient:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user(tg_id):
        async with async_session_factory() as session:
            query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
            if user is None:
                session.add(UsersORM(tg_id=tg_id))
                await session.commit()

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
            query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
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
