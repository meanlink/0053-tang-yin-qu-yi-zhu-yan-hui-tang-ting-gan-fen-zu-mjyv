from fastapi import HTTPException
from pydantic import BaseModel,Field
from acoustic_layout import set_design
from hearing_runs import current_run

class Assignment(BaseModel):
    group:str
    layout:str
    rationale:str=Field(min_length=4,max_length=150)
    # Optional: the calculation the reviewer was looking at. When omitted the
    # group is resolved only if it is unambiguous across retained calculations.
    run:int|None=Field(default=None,ge=1)

def book(cx):
    slots=cx.execute('''
      SELECT s.*,b.layout,b.members,b.panels,b.rationale,b.approved_by,b.frozen_at
      FROM residency_slots s
      LEFT JOIN residency_blueprints b ON s.code=b.code ORDER BY s.event_on,s.code
    ''').fetchall()
    return {"slots":slots,"layouts":cx.execute("SELECT * FROM listening_layouts ORDER BY code").fetchall()}

def _group(cx,assignment,slot):
    if assignment.run is not None:
        return cx.execute(
            "SELECT * FROM hearing_groups WHERE run_id=%s AND key=%s",
            (assignment.run,assignment.group)).fetchone()
    # Without an explicit calculation, accept the key only when exactly one
    # retained calculation contains it. Once a newer grouping exists the same
    # key appears twice, so a reviewer holding an old page must pick the new one.
    runs={row["run_id"] for row in cx.execute(
        "SELECT run_id FROM hearing_groups WHERE key=%s AND hall=%s",
        (assignment.group,slot["hall"])).fetchall()}
    if len(runs)>1:
        raise HTTPException(409,"该分组对应多次计算，请按当前试听确认最新分组")
    if not runs:
        return None
    return cx.execute(
        "SELECT * FROM hearing_groups WHERE run_id=%s AND key=%s",
        (runs.pop(),assignment.group)).fetchone()

def sign(cx,code,assignment,user):
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    slot=cx.execute("SELECT * FROM residency_slots WHERE code=%s",(code,)).fetchone()
    layout=cx.execute("SELECT * FROM listening_layouts WHERE code=%s",(assignment.layout,)).fetchone()
    group=_group(cx,assignment,slot) if slot else None
    if not slot or not layout or not group:
        raise HTTPException(404,"未找到场次、布置或分组")
    # A signed slot executes with the seats and panel count recorded at sign-off.
    # Later listening corrections do not re-open it.
    if cx.execute("SELECT 1 FROM residency_blueprints WHERE code=%s",(code,)).fetchone():
        raise HTTPException(409,"该场次已签核，原座席与吸声板布置不再改动")
    latest=current_run(cx,slot["hall"])
    # Sign-off must name the grouping computed from the hall's latest listening
    # data. A reviewer holding an older page is rejected even when the seats
    # happen to be unchanged.
    if not latest or latest["id"]!=group["run_id"] or group["hall"]!=slot["hall"]:
        raise HTTPException(409,"该分组已过期，请按当前试听重新计算并确认新分组")
    panels=set_design(cx,slot,layout,group)
    cx.execute('''
      INSERT INTO residency_blueprints(code,layout,members,panels,rationale,approved_by)
      VALUES(%s,%s,%s,%s,%s,%s)
    ''',(code,assignment.layout,group["members"],panels,assignment.rationale,user))
    return {"code":code,"panels":panels,"seats":group["members"],"run":group["run_id"]}
