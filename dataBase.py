
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text, LargeBinary, create_engine, Float
from sqlalchemy.orm import relationship, DeclarativeBase
import psycopg2


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'  # Используйте нижний регистр для имен таблиц

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    phone = Column(String(12), nullable=False)
    date_of_birthday = Column(Date, nullable=False)  # Изменено для удобочитаемости
    password = Column(String(50), nullable=False)
    login = Column(String(50), nullable=False)
    address_residential = Column(String(100), nullable=False)  # Изменено для удобочитаемости
    bank_account_number = Column(Integer, nullable=False)  # Исправлено в названии переменной
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)  # Исправлено на нижний регистр для имен таблиц

    role = relationship("Role", back_populates="users")
    user_cars = relationship("UserCar", back_populates="user")
    repairs = relationship("Repair", back_populates="user")
    reports = relationship("Report", back_populates="user")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    role_name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")


class CarPark(Base):
    __tablename__ = 'car_parks'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    state_number = Column(String(8), nullable=False)
    model = Column(String(50), nullable=False)
    stamp = Column(String(50), nullable=False)

    user_cars = relationship("UserCar", back_populates="car_park")


class UserCar(Base):
    __tablename__ = 'user_cars'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    car_id = Column(Integer, ForeignKey('car_parks.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    car_park = relationship("CarPark", back_populates="user_cars")
    user = relationship("User", back_populates="user_cars")


class Repair(Base):
    __tablename__ = 'repairs'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    description_breakdown = Column(String, nullable=False)
    date_and_time_repair = Column(Date, nullable=False)
    address_point_repair = Column(String(100), nullable=False)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="repairs")
    status = relationship("Status", back_populates="repairs")

class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status_name = Column(String(50), nullable=False)

    repairs = relationship("Repair", back_populates="status")

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    point_departure = Column(String(50), nullable=False)
    type_point_departure = Column(String(50), nullable=False)
    sender = Column(String(100), nullable=False)
    point_destination = Column(String(50), nullable=False)
    type_point_destination = Column(String(50), nullable=False)
    recipient = Column(String(100), nullable=False)
    view_wood = Column(String(50), nullable=False)
    length_wood = Column(Integer, nullable=False)
    volume_wood = Column(Float, nullable=False)
    report_date_time = Column(Date, nullable=False)
    assortment_wood_type = Column(String(50), nullable=False)
    variety_wood_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="reports")




engine = create_engine("postgresql://dmitriy:1ltcIsxaElWBxHmnYlr9qUZMYrZy4XtP@dpg-d1cqb23uibrs73fh4200-a.oregon-postgres.render.com/uchetperevozki_qbwc", echo=True)

Base.metadata.create_all(engine)
