from fastapi import HTTPException
from pydantic import BaseModel,Field
from acoustic_layout import set_design

class Assignment(BaseModel):
    group:str
    layout:str
    rationale:str=Field(min_length=4,max_length=150)

def book(cx):
    slots=cx.execute('''
      SELECT s.*,b.layout,b.members,b.panels,b.rationale FROM residency_slots s
      LEFT JOIN residency_blueprints b ON s.code=b.code ORDER BY s.event_on,s.code
    ''').fetchall()
    return {"slots":slots,"layouts":cx.execute("SELECT * FROM listening_layouts ORDER BY code").fetchall()}

def sign(cx,code,assignment,user):
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    slot=cx.execute("SELECT * FROM residency_slots WHERE code=%s",(code,)).fetchone()
    layout=cx.execute("SELECT * FROM listening_layouts WHERE code=%s",(assignment.layout,)).fetchone()
    group=cx.execute("SELECT * FROM hearing_groups WHERE key=%s",(assignment.group,)).fetchone()
    if not slot or not layout or not group:
        raise HTTPException(404,"未找到场次、布置或分组")
    panels=set_design(cx,slot,layout,group)
    cx.execute("INSERT INTO residency_blueprints(code,layout,members,panels,rationale,approved_by) VALUES(%s,%s,%s,%s,%s,%s)",(code,assignment.layout,group["members"],panels,assignment.rationale,user))
    return {"code":code,"panels":panels,"seats":group["members"]}
