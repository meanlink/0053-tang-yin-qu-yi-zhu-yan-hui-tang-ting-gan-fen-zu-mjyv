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
CREATE TABLE IF NOT EXISTS hearing_groups (
 key text PRIMARY KEY, hall text NOT NULL, members text[] NOT NULL,
 max_distance real NOT NULL CHECK(max_distance>=0), recommended_panels int NOT NULL CHECK(recommended_panels>=0),
 medians jsonb NOT NULL, trail jsonb NOT NULL
);
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
