# Restaurant Table Booking API

A FastAPI backend for restaurant table reservations, with an AI-powered chat assistant that can create and update bookings from natural language — no forms required.

**Live API:** https://restaurant-table-booking-system-with.onrender.com/docs
*(Free-tier hosting — first request after inactivity may take 30–60s to wake up.)*

## Features

- **Auth** — JWT-based register/login, secure password hashing (bcrypt via passlib)
- **Reservation CRUD** — create, list, view, update, and delete table reservations, scoped per user
- **AI chat assistant** — plain conversational chat endpoint
- **AI-powered booking** — describe a reservation in natural language and have it automatically extracted and saved (`POST /chat/extract`)
- **AI-powered updates** — modify an existing reservation conversationally, e.g. *"change the party size to 6"* (`PATCH /chat/update-reservation/{id}`)
- Ownership checks on every reservation route — users can only view/modify their own bookings

## Tech Stack

- **Framework:** FastAPI (fully async)
- **Database:** PostgreSQL (Neon), SQLAlchemy 2.0 (async, `asyncpg`), Alembic migrations
- **Auth:** JWT (`python-jose`), password hashing (`passlib[bcrypt]`)
- **AI:** LangChain + OpenRouter (`poolside/laguna-xs-2.1:free`), structured output via function-calling for reliable field extraction
- **Package management:** `uv`
- **Deployment:** Render

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Log in, receive a JWT |
| POST | `/reservations/` | Create a reservation manually |
| GET | `/reservations/` | List your reservations |
| GET | `/reservations/{id}` | Get one reservation |
| PATCH | `/reservations/{id}` | Update a reservation manually |
| DELETE | `/reservations/{id}` | Delete a reservation |
| POST | `/chat/` | Chat with the AI assistant |
| POST | `/chat/extract` | Describe a booking in natural language → AI creates the reservation |
| PATCH | `/chat/update-reservation/{id}` | Describe a change in natural language → AI updates the reservation |

Full interactive documentation (Swagger UI) is available at `/docs` on the live link above.

## Running Locally

```bash
git clone https://github.com/fgdhs788687/restaurant-table-booking-system-with-langchain.git
cd restaurant-table-booking-system-with-langchain/backend

uv sync
```

Create a `.env` file with:
```
DATABASE_URL=postgresql+asyncpg://<your-neon-connection-string>
JWT_SECRET=<a-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENROUTER_API_KEY=<your-openrouter-key>
OPENROUTER_MODEL=poolside/laguna-xs-2.1:free
```

Run migrations and start the server:
```bash
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API docs.

## Notes

This project was built as a learning exercise covering FastAPI, async SQLAlchemy, JWT auth, Alembic migrations, and LangChain-based structured extraction — including working through real reliability issues with free-tier LLM inference (provider compatibility, hallucination guardrails, and output format enforcement).
