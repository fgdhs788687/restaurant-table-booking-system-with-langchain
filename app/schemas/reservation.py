from pydantic import BaseModel, field_validator
from datetime import datetime, date, time
from app.db.models import ReservationStatus

class ReservationCreate(BaseModel):
    customer_name: str
    phone_number: str
    party_size: int
    reservation_date: date
    reservation_time: time


class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    phone_number: str
    party_size: int
    reservation_date: date
    reservation_time: time
    status: ReservationStatus
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class ReservationUpdate(BaseModel):
    customer_name: str | None = None
    phone_number: str | None = None
    party_size: int | None = None
    reservation_date: date | None = None
    reservation_time: time | None = None
    status: ReservationStatus | None = None

    @field_validator("phone_number", mode="before")
    @classmethod
    def coerce_phone_to_str(cls, value):
        if value is None:
            return value
        return str(value)


# For tool:
class ReservationExtract(BaseModel):
    customer_name: str | None = None
    phone_number: str | None = None
    party_size: int | None = None
    reservation_date: date | None = None
    reservation_time: time | None = None

    @field_validator("phone_number", mode="before")
    @classmethod
    def coerce_phone_to_str(cls, value):
        if value is None:
            return value
        return str(value)