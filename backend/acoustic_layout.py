from fastapi import HTTPException

def set_design(cx,slot,layout,group):
    if not (slot["hall"]==layout["hall"]==group["hall"]):
        raise HTTPException(409,"座席分组、布置与场次必须属于同一会堂")
    if not 2 <= len(group["members"]) <= layout["max_seats"]:
        raise HTTPException(409,"座席组超出布置人数，或只有一座")
    if group["recommended_panels"]>layout["panel_capacity"]:
        raise HTTPException(409,"当前布置的吸声板额度不足")
    if group["recommended_panels"] and cx.execute("SELECT 1 FROM seats WHERE code=ANY(%s) AND NOT mat_allowed",(group["members"],)).fetchone():
        raise HTTPException(409,"座席毗邻通道，临时吸声板不得布置")
    return group["recommended_panels"]
