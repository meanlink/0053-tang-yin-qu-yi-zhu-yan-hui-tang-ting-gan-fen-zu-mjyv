from fastapi import APIRouter,Depends
from core import db,require
from seat_book import seating
router=APIRouter(prefix="/seats")
@router.get("")
def seats(_=Depends(require())):
    with db() as cx:
        return seating(cx)
