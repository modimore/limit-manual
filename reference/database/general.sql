-- GENERAL DESCRIPTIONS  ======================================
CREATE SEQUENCE description_format_seq;
CREATE TABLE description_formats (
	uid SMALLINT PRIMARY KEY DEFAULT nextval('description_format_seq'),
	format_string VARCHAR(80) NOT NULL,
	num_slots INTEGER DEFAULT 0
);
ALTER SEQUENCE description_format_seq OWNED BY description_format.uid;

CREATE TABLE description_fillers (
	referent_type VARCHAR(10),
	referent_id SMALLINT,
	place SMALLINT,
	content VARCHAR(30),
	PRIMARY KEY (referent_type, referent_id, place)
);
-- ============================================================
