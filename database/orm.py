from sqlalchemy.orm import selectinload

from database.database import sync_engine, session_factory
from database.models import Base, UsersORM, WeatherReportsORM


class DBClient:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def add_user(tg_id):
        with session_factory() as session:
            user = session.query(UsersORM).filter(UsersORM.tg_id == tg_id).first()
            if user is None:
                new_user = UsersORM(tg_id=tg_id)
                session.add(new_user)
                session.commit()

    @staticmethod
    def set_user_city(tg_id, city):
        with session_factory() as session:
            user = session.query(UsersORM).filter(UsersORM.tg_id == tg_id).first()
            user.city = city
            session.commit()

    @staticmethod
    def get_user_city(tg_id):
        with session_factory() as session:
            user = session.query(UsersORM).filter(UsersORM.tg_id == tg_id).first()
            return user.city

    @staticmethod
    def create_weather_report(tg_id, temp, feels_like, wind_speed, pressure_mm, city, country):
        with session_factory() as session:
            user = session.query(UsersORM).filter(UsersORM.tg_id == tg_id).first()
            report = WeatherReportsORM(
                owner=user.id, temp=temp, feels_like=feels_like,
                wind_speed=wind_speed, pressure_mm=pressure_mm, city=city,
                country=country
            )
            session.add(report)
            session.commit()

    @staticmethod
    def get_user_reports(tg_id):
        with session_factory() as session:
            user = session.query(UsersORM).filter(UsersORM.tg_id == tg_id).first()
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
            users = session.query(UsersORM).options(selectinload(UsersORM.reports)).all()
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
            user_7 = UsersORM(tg_id=700, city="Тула")
            session.add_all([user_1, user_2, user_3, user_4, user_5, user_6, user_7])
            session.commit()


db_client = DBClient()







