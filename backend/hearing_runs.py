"""Listening-data revisions and which calculation currently represents a hall."""

def revision(cx, hall):
    row = cx.execute(
        "SELECT revision FROM listening_revisions WHERE hall=%s", (hall,)
    ).fetchone()
    return row["revision"] if row else 0


def bump(cx, hall):
    """Open a new revision after a hall's listening data actually changed."""
    return cx.execute(
        """INSERT INTO listening_revisions(hall,revision) VALUES(%s,1)
           ON CONFLICT(hall) DO UPDATE
           SET revision=listening_revisions.revision+1,updated_at=now()
           RETURNING revision""",
        (hall,),
    ).fetchone()["revision"]


def current_runs(cx):
    """Latest complete run per hall that was built from that hall's current revision.

    Runs of an older revision stay stored for reference but are expired, so they
    can neither replace the current grouping nor unlock sign-off. Among runs of
    the same revision only the newest one is current.
    """
    rows = cx.execute("""
      SELECT DISTINCT ON (r.hall) r.id, r.hall, r.revision, COALESCE(v.revision,0) AS live
      FROM hearing_runs r LEFT JOIN listening_revisions v ON v.hall=r.hall
      WHERE r.revision=COALESCE(v.revision,0)
      ORDER BY r.hall, r.id DESC
    """).fetchall()
    return {row["hall"]: row["id"] for row in rows}


def current_run(cx, hall):
    run_id = current_runs(cx).get(hall)
    if run_id is None:
        return None
    return cx.execute("SELECT * FROM hearing_runs WHERE id=%s", (run_id,)).fetchone()
