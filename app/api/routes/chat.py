from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.schemas.chat import ChatMessage, ChatResponse
from app.schemas.reservation import ReservationExtract, ReservationResponse, ReservationUpdate
from app.db.models import User, Reservation
from app.services.llm import llm
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.llm import get_extract_system_prompt
from langchain_core.messages import HumanMessage
import time

router = APIRouter()

# Normal chat with ai:
@router.post("/")
async def user_prompt(
    chat: ChatMessage,
    current_user: User = Depends(get_current_user))-> ChatResponse:
    msg = chat.message
    reply = llm.invoke(msg)
    return {"reply": f"{reply.content}"}

# TOOLS:
# Route to extract the data from ai-conversation and make new reservation:
@router.post("/extract")
async def extract_details(
    chat: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
)-> ReservationResponse:
    msg = chat.message
    structured_reply = llm.with_structured_output(ReservationExtract, method="function_calling")
    # Sometimes the free-model glitches so the output can be broken this try block saves us from the long error(maybe error-500) and returns us this HTTPException one instead.
    # This will try for 3 times then give up:
    max_attempt = 3
    for attempt in range(max_attempt):
        try:
            result = structured_reply.invoke([get_extract_system_prompt(), HumanMessage(content=msg)])
            from pprint import pprint
            pprint(result)
            break
        except Exception as e:
            print(f"EXTRACTION ERROR (attempt {attempt + 1}): {e}")
            if attempt == max_attempt - 1:
                raise HTTPException(
                    status_code=422,
                    detail="Could'nt understand the request please try rephrasing your message."
                )
            time.sleep(1)
    for field, value in result.model_dump().items():
        if value is None:
            raise HTTPException(status_code=422, detail=f"Missing required info: {field}")

    # If everthing's okay then add the extracted result to this new reservation:
    extract_reservation = Reservation(
        customer_name = result.customer_name,
        phone_number = result.phone_number,
        party_size = result.party_size,
        reservation_date = result.reservation_date,
        reservation_time = result.reservation_time,
        user_id = current_user.id
    )
    db.add(extract_reservation)
    await db.commit()
    await db.refresh(extract_reservation)
    return extract_reservation

# Updation of reservation with ai:
@router.patch("/update-reservation/{reservation_id}")
async def update_reservation(
    reservation_id: int,
    chat: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
)-> ReservationResponse:
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalar_one_or_none()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this reservation")
    msg = chat.message
    structured_reply = llm.with_structured_output(ReservationUpdate, method="function_calling")

    # This will try for 3 times then give up:
    max_attempt = 3
    for attempt in range(max_attempt):
        try:
            structured_result = structured_reply.invoke([get_extract_system_prompt(), HumanMessage(content=msg)])
            break
        except Exception as e:
            print(f"EXTRACTION ERROR (attempt {attempt + 1}): {e}")
            if attempt == max_attempt - 1:
                raise HTTPException(
                    status_code=422,
                    detail="Could'nt understand the request please try rephrasing your message."
                )
            time.sleep(1)

    # Updation Taking Place:
    update_field = structured_result.model_dump()
    # We dont want the user to change or update the status field:
    update_field.pop("status", None)

    for field, value in update_field.items():
        if value is not None:
            setattr(reservation, field, value)
    await db.commit()
    await db.refresh(reservation)
    return reservation