def seating(cx):
    return cx.execute('''
        SELECT s.*, count(l.passage) AS clips
        FROM seats s LEFT JOIN listening_slips l ON s.code=l.seat GROUP BY s.code
        ORDER BY s.hall,CASE s.section WHEN 'front' THEN 1 WHEN 'mid' THEN 2 ELSE 3 END,s.lane
    ''').fetchall()
