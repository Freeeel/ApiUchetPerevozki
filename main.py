from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import joinedload
from dataBase import *
from datetime import datetime
import logging
from typing import Optional
app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#python -m  uvicorn main:app --reload --host 172.20.10.11

class UserLogin(BaseModel):
    login: str
    password: str


class RepairCreate(BaseModel):
    description_breakdown: str
    date_and_time_repair: str
    address_point_repair: str
    user_id: int
    status_id: int

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    phone: str
    date_of_birthday: str  # Или использовать datetime, если хотите
    address_residential: str
    bank_account_number: int
    role_id: int
    login: str
    password: str

class UserCreate(BaseModel):
    name: str
    surname: str
    patronymic: str
    phone: str
    date_of_birthday: str
    address_residential: str
    bank_account_number: int
    login: str
    password: str
    car_id: int  # Добавляем car_id


class ReportCreate(BaseModel):
    point_departure: str
    type_point_departure: str
    sender: str
    point_destination: str
    type_point_destination: str
    recipient: str
    view_wood: str
    length_wood: int
    volume_wood: float
    report_date_time: str
    assortment_wood_type: str
    variety_wood_type: str
    user_id: int

class ReportResponseWithUser(BaseModel):
    user_name: str
    user_surname: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    address_residential: Optional[str] = None
    bank_account_number: Optional[int] = None
    login: Optional[str] = None
    password: Optional[str] = None
    car_id: Optional[int] = None

class ReportResponse(BaseModel):
    id: int
    point_departure: str
    type_point_departure: str
    sender: str
    point_destination: str
    type_point_destination: str
    recipient: str
    view_wood: str
    length_wood: int
    volume_wood: float
    report_date_time: str
    assortment_wood_type: str
    variety_wood_type: str
    user_id: int
    user_name: Optional[str] = None
    user_surname: Optional[str] = None
    user_patronymic : Optional[str] = None

class CarParkResponse(BaseModel):
    id: int
    state_number: str
    model: str
    stamp: str

class UserCarCreate(BaseModel):
    user_id: int
    car_id: int

class RepairUpdate(BaseModel):
    status_id: int


class RepairWithUserNameResponse(BaseModel):
    id: int
    description_breakdown: str
    date_and_time_repair: str
    address_point_repair: str
    status_id: int
    user_id: int
    user_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user_login.login, User.password == user_login.password).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    return {
        "id": db_user.id,
        "name": db_user.name,
        "surname": db_user.surname,
        "patronymic": db_user.patronymic,
        "phone": db_user.phone,
        "date_of_birthday": db_user.date_of_birthday,
        "address_residential": db_user.address_residential,
        "bank_account_number": db_user.bank_account_number,
        "role_id": db_user.role_id,
        "password": db_user.password,
        "login": db_user.login
    }


@app.get("/getuser/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Получаем пользователя по user_id
    db_user = db.query(User).filter(User.id == user_id).first()

    # Если пользователь не найден, выбрасываем ошибку
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Возвращаем данные пользователя
    return {
        "id": db_user.id,  # Здесь вы ранее использовали db_user, что вызвало ошибку
        "name": db_user.name,
        "surname": db_user.surname,
        "patronymic": db_user.patronymic,
        "phone": db_user.phone,
        "date_of_birthday": db_user.date_of_birthday,
        "address_residential": db_user.address_residential,
        "bank_account_number": db_user.bank_account_number,
        "role_id": db_user.role_id,
        "password": db_user.password,
        "login": db_user.login
    }


@app.post("/repairs/")
async def create_repair(repair: RepairCreate, db: Session = Depends(get_db)):
    new_repair = Repair(
        description_breakdown=repair.description_breakdown,
        date_and_time_repair=repair.date_and_time_repair,
        address_point_repair=repair.address_point_repair,
        user_id=repair.user_id,
        status_id=repair.status_id)
    try:
        db.add(new_repair)
        db.commit()
        db.refresh(new_repair)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_repair


@app.post("/reports/")
async def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    report_date_time = datetime.strptime(report.report_date_time, '%d/%m/%Y').date()

    new_report = Report(
        point_departure=report.point_departure,
        type_point_departure=report.type_point_departure,
        sender=report.sender,
        point_destination=report.point_destination,
        type_point_destination=report.type_point_destination,
        recipient=report.recipient,
        view_wood=report.view_wood,
        length_wood=report.length_wood,
        volume_wood=report.volume_wood,
        report_date_time=report_date_time,
        assortment_wood_type=report.assortment_wood_type,
        variety_wood_type=report.variety_wood_type,
        user_id=report.user_id
    )
    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Internal server error")
    return new_report



@app.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "car_id":
            continue
        setattr(db_user, key, value)

    if user_update.car_id is not None:

        target_car = db.query(CarPark).filter(CarPark.id == user_update.car_id).first()
        if not target_car:
            raise HTTPException(status_code=400, detail=f"Car with ID {user_update.car_id} not found in CarPark.")
        existing_user_car = db.query(UserCar).filter(UserCar.user_id == user_id).first()
        if existing_user_car:

            existing_user_car.car_id = user_update.car_id
        else:

            new_user_car = UserCar(user_id=user_id, car_id=user_update.car_id)
            db.add(new_user_car)
    try:
        db.commit()
        db.refresh(db_user)
        return {
            "id": db_user.id,
            "name": db_user.name,
            "surname": db_user.surname,
            "patronymic": db_user.patronymic,
            "phone": db_user.phone,
            "address_residential": db_user.address_residential,
            "bank_account_number": db_user.bank_account_number,
            "login": db_user.login,
            "password": db_user.password,
        }
    except Exception as e:
        db.rollback()

        print(f"Error updating user or user's car: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")
@app.get("/user/{user_id}/car")
async def get_user_car(user_id: int, db: Session = Depends(get_db)):
    user_cars = db.query(UserCar).filter(UserCar.user_id == user_id).all()

    if not user_cars:
        raise HTTPException(status_code=404, detail="Нет привязанных автомобилей для этого пользователя")
    car = user_cars[0]
    car_details = {
        "car_id": car.id,
        "state_number": car.car_park.state_number,
        "model": car.car_park.model,
        "stamp": car.car_park.stamp
    }

    return car_details


@app.get("/reports/user/{user_id}", response_model=list[ReportResponse])
async def get_reports_by_user(user_id: int, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.user_id == user_id).all()

    if not reports:
        raise HTTPException(status_code=404, detail="Нет отчетов для данного пользователя")

    return [{
        **report.__dict__,
        "report_date_time": report.report_date_time.isoformat()  # Преобразуем дату в строку
    } for report in reports]


# @app.get("/reports/all", response_model=list[ReportResponse])
# async def get_all_reports(db: Session = Depends(get_db)):
#     reports = db.query(Report).all()
#     if not reports:
#         raise HTTPException(status_code=404, detail="В базе данных нет отчетов")
#     return [{
#         **report.__dict__,
#         "report_date_time": report.report_date_time.isoformat()  # Преобразуем дату в строку
#     } for report in reports]

@app.get("/users/role/1", response_model=list[UserResponse])
async def get_users_with_role_1(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.role_id == 1).all()

    if not users:
        raise HTTPException(status_code=404, detail="Пользователи с role_id 1 не найдены")

    return [UserResponse(
        id=user.id,
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        phone=user.phone,
        date_of_birthday=user.date_of_birthday.isoformat(),  # Преобразование в строку, если нужно
        address_residential=user.address_residential,
        bank_account_number=user.bank_account_number,
        role_id=user.role_id,
        login=user.login,
        password=user.password
    ) for user in users]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_car_park(db: Session, car_id: int):
    return db.query(CarPark).filter(CarPark.id == car_id).first()

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        date_of_birthday = datetime.strptime(user.date_of_birthday, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    db_user = User(
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        phone=user.phone,
        date_of_birthday=date_of_birthday,
        address_residential=user.address_residential,
        bank_account_number=user.bank_account_number,
        login=user.login,
        password=user.password,
        role_id=1)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        car_park = get_car_park(db, user.car_id)
        if car_park is None:
            raise HTTPException(status_code=400, detail=f"Car with id {user.car_id} not found")
        user_car = UserCar(user_id=db_user.id, car_id=user.car_id)
        db.add(user_car)
        db.commit()
        db.refresh(user_car)
        return UserResponse(
            id=db_user.id,
            name=db_user.name,
            surname=db_user.surname,
            patronymic=db_user.patronymic,
            phone=db_user.phone,
            date_of_birthday=db_user.date_of_birthday.isoformat(),
            address_residential=db_user.address_residential,
            bank_account_number=db_user.bank_account_number,
            role_id=db_user.role_id,
            login=db_user.login,
            password=db_user.password)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")
@app.post("/user_cars/")
async def create_user_car(user_car: UserCarCreate, db: Session = Depends(get_db)):
    db_user_car = UserCar(**user_car.dict())
    db.add(db_user_car)
    db.commit()
    db.refresh(db_user_car)
    return db_user_car

# Эндпоинт для получения всех автомобилей из таблицы CarPark
@app.get("/car_parks/", response_model=list[CarParkResponse])
async def get_car_parks(db: Session = Depends(get_db)):
    car_parks = db.query(CarPark).all()
    return [CarParkResponse(
        id=car.id,
        state_number=car.state_number,
        model=car.model,
        stamp=car.stamp
    ) for car in car_parks]

@app.get("/repairs_with_users/", response_model=list[RepairWithUserNameResponse])
async def get_repairs_with_users(db: Session = Depends(get_db)):
    """
    Получает список всех ремонтов с именем и фамилией пользователя.
    """
    repairs_with_users = (
        db.query(Repair, User)
        .join(User, Repair.user_id == User.id)
        .all()
    )

    if not repairs_with_users:
        raise HTTPException(status_code=404, detail="Ремонты не найдены")

    result = []
    for repair, user in repairs_with_users:
        user_full_name = f"{user.name} {user.surname}"
        result.append({
            "id": repair.id,
            "description_breakdown": repair.description_breakdown,
            "date_and_time_repair": str(repair.date_and_time_repair), # Преобразуем дату в строку
            "address_point_repair": repair.address_point_repair,
            "status_id": repair.status_id,
            "user_id": repair.user_id,
            "user_name": user_full_name
        })

    return result

@app.put("/repairs/{repair_id}")
async def update_repair(repair_id: int, repair_update: RepairUpdate, db: Session = Depends(get_db)):

    db_repair = db.query(Repair).filter(Repair.id == repair_id).first()
    if db_repair is None:
        raise HTTPException(status_code=404, detail="Ремонт не найден")

    for key, value in repair_update.dict(exclude_unset=True).items():
        setattr(db_repair, key, value)
    try:
        db.commit()
        db.refresh(db_repair)
        return db_repair
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удалось обновить ремонт: {e}")

@app.get("/statuses/")
async def get_statuses(db: Session = Depends(get_db)):
    """
    Возвращает список всех статусов.
    """
    # Запрос к базе данных для получения всех объектов Status
    statuses = db.query(Status).all()
    # Возвращаем список объектов статусов
    return statuses


@app.get("/reports/all", response_model=list[ReportResponse])
async def get_all_reports(db: Session = Depends(get_db)):

    reports = db.query(Report).options(joinedload(Report.user)).all()
    if not reports:
        raise HTTPException(status_code=404, detail="В базе данных нет отчетов")
    formatted_reports = []
    for report in reports:
        report_dict = report.__dict__.copy()
        if report.user:
            report_dict["user_name"] = report.user.name
            report_dict["user_surname"] = report.user.surname
            report_dict["user_patronymic"] = report.user.patronymic
        else:
            report_dict["user_name"] = None
            report_dict["user_surname"] = None
            report_dict["user_patronymic"] = None

        report_dict["report_date_time"] = report_dict["report_date_time"].isoformat()

        formatted_reports.append(ReportResponse(**report_dict))

    return formatted_reports


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    try:

        db.query(UserCar).filter(UserCar.user_id == user_id).delete(synchronize_session=False)

        db.query(Report).filter(Report.user_id == user_id).delete(synchronize_session=False)

        db.query(Repair).filter(Repair.user_id == user_id).delete(synchronize_session=False)

        db.delete(db_user)
        db.commit()

        return {"message": f"Пользователь с ID {user_id} успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удалось удалить пользователя: {e}")


@app.delete("/reports/{report_id}")
async def delete_report(report_id: int, db: Session = Depends(get_db)):

    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        raise HTTPException(status_code=404, detail="Отчет не найден")

    try:
        db.delete(db_report)
        db.commit()

        return {"message": f"Отчет с ID {report_id} успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удалось удалить отчет: {e}")


@app.delete("/car_parks/{car_id}")
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(CarPark).filter(CarPark.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")

    try:
        # Сначала удаляем привязки к пользователям
        db.query(UserCar).filter(UserCar.car_id == car_id).delete()

        # Затем удаляем сам автомобиль
        db.delete(db_car)
        db.commit()

        return {"message": f"Автомобиль с ID {car_id} успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удалось удалить автомобиль: {e}")


# Получение всех привязок пользователей к автомобилям
@app.get("/user_cars/")
async def get_all_user_cars(db: Session = Depends(get_db)):
    user_cars = db.query(UserCar).all()
    return user_cars