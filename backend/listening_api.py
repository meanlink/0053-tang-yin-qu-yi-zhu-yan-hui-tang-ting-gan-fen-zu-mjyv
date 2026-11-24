from fastapi import APIRouter,Depends
from core import db,require
from listening_records import Listen,upsert
router=APIRouter(prefix="/listening")
@router.get("")
def listening(_=Depends(require())):
    with db() as cx:
        return cx.execute("SELECT l.*,s.hall,s.section FROM listening_slips l JOIN seats s ON l.seat=s.code ORDER BY s.hall,l.seat,l.passage").fetchall()
@router.post("")
def submit(data:Listen,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        return upsert(cx,data)
