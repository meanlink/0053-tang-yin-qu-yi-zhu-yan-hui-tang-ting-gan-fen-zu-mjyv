from pathlib import Path

from fastapi import APIRouter
from seats_api import router as seats
from listening_api import router as listening
from acoustics_api import router as acoustics
from residencies_api import router as residencies
from acoustic_jobs import run_job

router = APIRouter(prefix="/api")
router.include_router(seats)
router.include_router(listening)
router.include_router(acoustics)
router.include_router(residencies)


def seed(connection):
    connection.execute(Path(__file__).with_name("demo.sql").read_text())
