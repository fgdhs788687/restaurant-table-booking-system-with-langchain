from langchain_openai import ChatOpenAI
from app.core.config import settings
from langchain_core.messages import SystemMessage
from datetime import datetime

# Instruction for the ai model while extracting fields:
def get_extract_system_prompt():
    today = datetime.today().isoformat()
    return SystemMessage(content=(
        "Extract only the reservation fields explicitly mentioned in the user's message. "
        "Leave any field not mentioned as null. Do not guess, invent, or infer values for unmentioned fields. "
        f"Today's date is {today}. "
        "Format reservation_date strictly as YYYY-MM-DD, using the current year unless the user explicitly states a different year. "
        "Format reservation_time strictly as HH:MM:SS in 24-hour time (e.g. 23:30:00 for 11:30pm). "
        "Format phone_number as digits only, with no extra characters, letters, or symbols."
    ))


llm = ChatOpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
    model=settings.openrouter_model
)
