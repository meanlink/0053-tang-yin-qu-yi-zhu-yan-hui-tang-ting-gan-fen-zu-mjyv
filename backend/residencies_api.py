from fastapi import APIRouter,Depends
from core import db,require
from residency_book import Assignment,book,sign
router=APIRouter(prefix="/residencies")
@router.get("")
def residencies(_=Depends(require())):
    with db() as cx:
        return book(cx)
@router.post("/{code}")
def approve(code:str,data:Assignment,user=Depends(require("reviewer"))):
    with db() as cx:
        return sign(cx,code,data,user["email"])
