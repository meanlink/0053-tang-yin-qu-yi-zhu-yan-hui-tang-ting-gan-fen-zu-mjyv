-- Every change to a hall's listening data opens a new revision. A grouping is
-- only usable for sign-off when it was computed from the current revision.
CREATE TABLE IF NOT EXISTS seats (
 code text PRIMARY KEY, hall text NOT NULL, section text NOT NULL CHECK(section IN ('front','mid','rear')),
 lane int NOT NULL CHECK(lane BETWEEN 1 AND 8), mat_allowed boolean NOT NULL
);
CREATE TABLE IF NOT EXISTS listening_slips (
 seat text REFERENCES seats(code), passage text CHECK(passage IN ('spoken','sung')),
 clarity smallint NOT NULL CHECK(clarity BETWEEN 0 AND 100),
 echo_ms int NOT NULL CHECK(echo_ms BETWEEN 0 AND 3000),
 level_db int NOT NULL CHECK(level_db BETWEEN 0 AND 120),
 media_ref text NOT NULL, PRIMARY KEY(seat,passage)
);

CREATE TABLE IF NOT EXISTS listening_revisions (
 hall text PRIMARY KEY,
 revision bigint NOT NULL DEFAULT 1 CHECK(revision>0),
 updated_at timestamptz NOT NULL DEFAULT now()
);

-- A run records which revision a calculation was based on. Runs are never
-- deleted or overwritten, so an obsolete result stays readable for reference.
CREATE TABLE IF NOT EXISTS hearing_runs (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 job_id bigint UNIQUE REFERENCES app_jobs(id),
 hall text NOT NULL,
 revision bigint NOT NULL CHECK(revision>=0),
 threshold real NOT NULL CHECK(threshold>0),
 created_at timestamptz NOT NULL DEFAULT now(),
 finished_at timestamptz NOT NULL DEFAULT now()
);

-- Early databases stored derived groups without run provenance, so they cannot
-- be told apart from current groups. They are rebuilt by the next calculation.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables
             WHERE table_schema='public' AND table_name='hearing_groups')
     AND NOT EXISTS (SELECT 1 FROM information_schema.columns
             WHERE table_schema='public' AND table_name='hearing_groups'
               AND column_name='run_id') THEN
    DROP TABLE hearing_groups;
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS hearing_groups (
 run_id bigint NOT NULL REFERENCES hearing_runs(id) ON DELETE CASCADE,
 key text NOT NULL,
 hall text NOT NULL, members text[] NOT NULL,
 max_distance real NOT NULL CHECK(max_distance>=0), recommended_panels int NOT NULL CHECK(recommended_panels>=0),
 medians jsonb NOT NULL, trail jsonb NOT NULL,
 PRIMARY KEY(run_id,key)
);
CREATE INDEX IF NOT EXISTS hearing_groups_hall ON hearing_groups(hall);

CREATE TABLE IF NOT EXISTS listening_layouts (
 code text PRIMARY KEY, hall text NOT NULL, title text NOT NULL,
 panel_capacity int NOT NULL CHECK(panel_capacity>=0), max_seats int NOT NULL CHECK(max_seats>=2)
);
CREATE TABLE IF NOT EXISTS residency_slots (
 code text PRIMARY KEY, hall text NOT NULL, producer text NOT NULL, event_on date NOT NULL
);
CREATE TABLE IF NOT EXISTS residency_blueprints (
 code text PRIMARY KEY REFERENCES residency_slots(code), layout text NOT NULL REFERENCES listening_layouts(code),
 members text[] NOT NULL, panels int NOT NULL CHECK(panels>=0), rationale text NOT NULL,
 approved_by text NOT NULL, frozen_at timestamptz NOT NULL DEFAULT now()
);
