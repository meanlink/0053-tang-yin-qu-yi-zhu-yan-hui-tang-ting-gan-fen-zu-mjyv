from fastapi import APIRouter,Depends
from core import db,enqueue,require
from pydantic import BaseModel,Field
router=APIRouter(prefix="/acoustics")
class Fit(BaseModel):
    hall:str=Field(min_length=2,max_length=50)
    threshold:float=Field(gt=0,le=10)
@router.get("")
def results(_=Depends(require())):
    with db() as cx:
        return cx.execute("SELECT * FROM hearing_groups ORDER BY hall,key").fetchall()
@router.post("")
def estimate(data:Fit,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        return {"job_id":enqueue(cx,"layout-acoustics",data.model_dump())}
