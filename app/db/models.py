from sqlalchemy import Column, String, Integer, DateTime, Time, Date, Enum, ForeignKey
from app.db.session import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum

# This function gives the current time
def utc_now():
    return datetime.now(timezone.utc)

# This class is used to create enum
class ReservationStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

'''
User table

id — primary key
username — unique, indexed
email — unique (optional, up to you)
hashed_password — never store plain passwords
created_at — timestamp, defaults to now
'''

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_passwords = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now) # Gives current time

    reservations = relationship(
        "Reservation",
        back_populates="user"
    )

'''
Reservation table:

id — primary key
customer_name
phone_number
email (optional)
party_size
reservation_date
reservation_time
seating_preference (optional)
special_requests (optional)
status — e.g. pending/confirmed/cancelled, default "pending"
created_at
user_id — foreign key → links to User.id
'''
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    party_size = Column(Integer, nullable=False)
    reservation_date = Column(Date, nullable=False)
    reservation_time = Column(Time, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)

    user = relationship(
        "User",
        back_populates="reservations"
    )