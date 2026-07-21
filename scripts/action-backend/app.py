"""AI Starter Kit — Action Tools backend (provided; teams WIRE it, not build it).

A tiny FastAPI REST API exposing three *action* operations a student-services agent
can perform. State is in-memory (resets on restart) — that is intentional for a workshop.

Endpoints:
    GET  /health
    POST /it-tickets            create an IT support ticket
    GET  /it-tickets            list all created IT tickets
    GET  /it-tickets/{id}
    POST /course-holds          place a registration hold on a course
    GET  /course-holds/{id}
    POST /advising-slots        book an academic advising slot
    GET  /advising-slots/{id}
    GET  /                      list all created records (debug)

Auth (optional): if ACTION_API_KEY is set in the environment, every mutating request
must send a matching `x-api-key` header. Leave it unset for open local workshops.

Run:
    uvicorn app:app --host 0.0.0.0 --port 8080     # base URL -> ACTION_API_URL
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

API_KEY = os.environ.get("ACTION_API_KEY", "").strip()

app = FastAPI(
    title="Northfield University — Action Tools API",
    description="Provided backend for the Advanced: Action Tools activity.",
    version="1.0.0",
)

# In-memory stores (reset on restart — fine for a workshop).
_it_tickets: dict[str, dict] = {}
_course_holds: dict[str, dict] = {}
_advising_slots: dict[str, dict] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _check_key(x_api_key: str | None) -> None:
    """Enforce the optional shared-secret header when ACTION_API_KEY is configured."""
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing x-api-key header.")


# --------------------------------------------------------------------------- #
# Request / response models
# --------------------------------------------------------------------------- #
class ITTicketRequest(BaseModel):
    student_id: str = Field(..., examples=["s1029384"])
    category: Literal["wifi", "account", "hardware", "software", "other"] = "other"
    summary: str = Field(..., examples=["Cannot connect to eduroam in dorm"])
    priority: Literal["low", "normal", "high", "urgent"] = "normal"


class CourseHoldRequest(BaseModel):
    student_id: str = Field(..., examples=["s1029384"])
    course_code: str = Field(..., examples=["CS101"])
    reason: str = Field(..., examples=["Awaiting prerequisite verification"])


class AdvisingSlotRequest(BaseModel):
    student_id: str = Field(..., examples=["s1029384"])
    advisor: str = Field(..., examples=["Dr. Lee"])
    iso_datetime: str = Field(..., examples=["2026-06-10T15:00:00Z"])
    topic: str = Field("General advising", examples=["Course planning for fall"])


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "time": _now(), "auth_required": bool(API_KEY)}


@app.post("/it-tickets", status_code=201)
def create_it_ticket(req: ITTicketRequest, x_api_key: str | None = Header(default=None)) -> dict:
    _check_key(x_api_key)
    ticket_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "ticket_id": ticket_id,
        "status": "open",
        "created_at": _now(),
        **req.model_dump(),
    }
    _it_tickets[ticket_id] = record
    return record


@app.get("/it-tickets/{ticket_id}")
def get_it_ticket(ticket_id: str) -> dict:
    if ticket_id not in _it_tickets:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return _it_tickets[ticket_id]


@app.get("/it-tickets")
def list_it_tickets() -> dict:
    return {"items": list(_it_tickets.values())}


@app.post("/course-holds", status_code=201)
def create_course_hold(req: CourseHoldRequest, x_api_key: str | None = Header(default=None)) -> dict:
    _check_key(x_api_key)
    hold_id = f"HOLD-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "hold_id": hold_id,
        "status": "active",
        "created_at": _now(),
        **req.model_dump(),
    }
    _course_holds[hold_id] = record
    return record


@app.get("/course-holds/{hold_id}")
def get_course_hold(hold_id: str) -> dict:
    if hold_id not in _course_holds:
        raise HTTPException(status_code=404, detail="Hold not found.")
    return _course_holds[hold_id]


@app.post("/advising-slots", status_code=201)
def book_advising_slot(req: AdvisingSlotRequest, x_api_key: str | None = Header(default=None)) -> dict:
    _check_key(x_api_key)
    booking_id = f"ADV-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "booking_id": booking_id,
        "status": "confirmed",
        "created_at": _now(),
        **req.model_dump(),
    }
    _advising_slots[booking_id] = record
    return record


@app.get("/advising-slots/{booking_id}")
def get_advising_slot(booking_id: str) -> dict:
    if booking_id not in _advising_slots:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return _advising_slots[booking_id]


@app.get("/")
def list_all() -> dict:
    return {
        "it_tickets": list(_it_tickets.values()),
        "course_holds": list(_course_holds.values()),
        "advising_slots": list(_advising_slots.values()),
    }
