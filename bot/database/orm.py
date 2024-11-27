from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.database.database import async_engine, async_session_factory
from bot.database.exceptions import DatabaseError
from bot.database.models import Base, UsersORM, WeatherReportsORM


class AsyncDBClient:
    @staticmethod
    async def create_tables() -> None:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def _get_user(
            cls,
            tg_id: int,
            *,
            load_reports: bool = False,
    ) -> UsersORM | None:
        async with async_session_factory() as session:
            if load_reports:
                query = select(UsersORM).filter(
                    UsersORM.tg_id == tg_id
                ).options(selectinload(UsersORM.reports))
            else:
                query = select(UsersORM).filter(UsersORM.tg_id == tg_id)
            user = (await session.execute(query)).scalar()
            return user

    @classmethod
    async def add_user(cls, tg_id: int) -> UsersORM:
        async with async_session_factory() as session:
            user = await cls._get_user(tg_id)
            if user is None:
                session.add(UsersORM(tg_id=tg_id))
                await session.commit()
                user = await cls._get_user(tg_id)
                if user is None:
                    raise DatabaseError('User does not exist')
            return user

    @classmethod
    async def set_user_city(cls, tg_id: int, city: str) -> None:
        async with async_session_factory() as session:
            user = await cls._get_user(tg_id)
            if user is None:
                raise DatabaseError(f"User with tg_id={tg_id} does not exist")
            user.city = city
            await session.commit()

    @classmethod
    async def get_user_city(cls, tg_id: int) -> str:
        async with async_session_factory() as session:
            user = await cls._get_user(tg_id)
            if user is None:
                raise DatabaseError(f"User with tg_id={tg_id} does not exist")
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
    ) -> None:
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
    async def get_user_reports(tg_id: int) -> list[WeatherReportsORM]:
        async with async_session_factory() as session:
            user = await db_client._get_user(tg_id, load_reports=True)
            if user is None:
                raise DatabaseError(f"User with tg_id={tg_id} does not exist")
            reports = user.reports
            return reports

    @classmethod
    async def get_report(cls, report_id: int) -> WeatherReportsORM:
        async with async_session_factory() as session:
            report = await session.get(WeatherReportsORM, report_id)
            if report is None:
                raise DatabaseError(f"Can't get report with id {report_id}")
            return report

    @classmethod
    async def delete_user_report(cls, report_id: int) -> None:
        async with async_session_factory() as session:
            report = await cls.get_report(report_id)
            await session.delete(report)
            await session.commit()

    @staticmethod
    async def get_all_users() -> Sequence[UsersORM]:
        async with async_session_factory() as session:
            query = select(UsersORM).options(selectinload(UsersORM.reports))
            users = (await session.execute(query)).scalars().all()
            return users

    @staticmethod
    async def get_all_reports() -> Sequence[WeatherReportsORM]:
        async with async_session_factory() as session:
            query = select(WeatherReportsORM)
            reports = (await session.execute(query)).scalars().all()
            return reports


db_client = AsyncDBClient()
