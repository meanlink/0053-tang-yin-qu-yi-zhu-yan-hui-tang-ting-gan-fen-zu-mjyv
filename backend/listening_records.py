from typing import Literal
from fastapi import HTTPException
from pydantic import BaseModel,Field

class Listen(BaseModel):
    seat:str
    passage:Literal["spoken","sung"]
    clarity:int=Field(ge=0,le=100)
    echo_ms:int=Field(ge=0,le=3000)
    level_db:int=Field(ge=0,le=120)
    media_ref:str=Field(min_length=5,max_length=80)

def upsert(cx,data):
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    seat=cx.execute("SELECT hall FROM seats WHERE code=%s",(data.seat,)).fetchone()
    if not seat:
        raise HTTPException(404,"座席不存在")
    if cx.execute("SELECT 1 FROM residency_blueprints WHERE %s=ANY(members)",(data.seat,)).fetchone():
        raise HTTPException(409,"座席录音正在用于已审签的布置，不能覆盖")
    cx.execute('''
       INSERT INTO listening_slips VALUES(%(seat)s,%(passage)s,%(clarity)s,%(echo_ms)s,%(level_db)s,%(media_ref)s)
       ON CONFLICT(seat,passage) DO UPDATE SET clarity=excluded.clarity,echo_ms=excluded.echo_ms,
       level_db=excluded.level_db,media_ref=excluded.media_ref
    ''',data.model_dump())
    cx.execute("DELETE FROM hearing_groups WHERE hall=%s",(seat["hall"],))
    return {"seat":data.seat,"passage":data.passage}
