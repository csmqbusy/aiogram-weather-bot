from datetime import datetime

from sqlalchemy import ForeignKey, BigInteger, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from bot.database.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    city: Mapped[str] = mapped_column(nullable=True)
    connection_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())"),
        nullable=False,
    )
    reports: Mapped[list["WeatherReportsORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} tg_id={self.tg_id}>"


class WeatherReportsORM(Base):
    __tablename__ = "weather_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE ('utc', now())"),
        nullable=False,
    )
    temp: Mapped[float] = mapped_column(nullable=False)
    feels_like: Mapped[float] = mapped_column(nullable=False)
    wind_speed: Mapped[float] = mapped_column(nullable=False)
    pressure_mm: Mapped[float] = mapped_column(nullable=False)
    visibility: Mapped[float] = mapped_column(nullable=False)
    weather_condition: Mapped[str] = mapped_column(
        nullable=False,
        server_default="Данные отсутствуют",
    )
    city: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=True)
    user: Mapped[list["UsersORM"]] = relationship(back_populates="reports")

    def __repr__(self) -> str:
        message = (
            f"<WeatherReport "
            f"{self.city}, {self.date.day}.{self.date.month}.{self.date.year}>"
        )
        return message
