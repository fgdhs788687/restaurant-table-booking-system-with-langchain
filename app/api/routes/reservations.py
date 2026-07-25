from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdate
from app.db.models import Reservation, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()

# Create a new reservation:
@router.post("/")
async def reservations(
    reservation: ReservationCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)    
) -> ReservationResponse:
    
    new_reservation = Reservation(
        customer_name=reservation.customer_name,
        phone_number=reservation.phone_number,
        party_size=reservation.party_size,
        reservation_date=reservation.reservation_date,
        reservation_time=reservation.reservation_time,
        user_id=current_user.id
    )
    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    return new_reservation




# Get all reservations:
@router.get("/")
async def all_reservation(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[ReservationResponse]:
    all_reserv = await db.execute(
        select(Reservation).where(Reservation.user_id == current_user.id)
    )
    result = all_reserv.scalars().all()
    return result




# Get a particular reservation detail:
@router.get("/{reservation_id}")
async def get_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ReservationResponse:
    
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalar_one_or_none()

    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation




# Update the reservation:
@router.patch("/{reservation_id}")
async def update_reservation(
    reservation_id: int, 
    update_data: ReservationUpdate ,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)    
) -> ReservationResponse:
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalar_one_or_none()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    # Updation taking place:
    update_field = update_data.model_dump(exclude_unset=True)
    for field, value in update_field.items():
        setattr(reservation, field, value)

    await db.commit()
    await db.refresh(reservation)

    return reservation



# Deletion of the reservation:
@router.delete("/{reservation_id}")
async def delete_reservation(
    reservation_id:int,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> dict:
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalar_one_or_none()

    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Deletion of this reservation:
    await db.delete(reservation)
    await db.commit()
    return {"message": f"Reservation with id:{reservation_id} is deleted."}