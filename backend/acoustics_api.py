from fastapi import APIRouter,Depends,HTTPException
from core import db,enqueue,require
from hearing_runs import current_runs,revision
from pydantic import BaseModel,Field
router=APIRouter(prefix="/acoustics")
class Fit(BaseModel):
    hall:str=Field(min_length=2,max_length=50)
    threshold:float=Field(gt=0,le=10)

@router.get("")
def results(_=Depends(require())):
    with db() as cx:
        rows=cx.execute('''
          SELECT g.*,r.revision AS run_revision,r.threshold,r.created_at AS run_created_at,r.finished_at
          FROM hearing_groups g JOIN hearing_runs r ON r.id=g.run_id
          ORDER BY r.id DESC,g.key
        ''').fetchall()
        live=current_runs(cx)
        for row in rows:
            # Only the newest run built from a hall's current listening revision
            # is current; earlier runs stay readable for reference.
            row["current"]=live.get(row["hall"])==row["run_id"]
            row["expired"]=not row["current"]
        return rows

@router.post("")
def estimate(data:Fit,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        cx.execute("SELECT pg_advisory_xact_lock(53019)")
        if not cx.execute("SELECT 1 FROM seats WHERE hall=%s LIMIT 1",(data.hall,)).fetchone():
            raise HTTPException(404,"会堂不存在")
        rev=revision(cx,data.hall)
        job=enqueue(cx,"layout-acoustics",data.model_dump()|{"revision":rev})
        return {"job_id":job,"revision":rev}
