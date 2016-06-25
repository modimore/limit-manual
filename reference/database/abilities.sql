--  ABILITIES =================================================
CREATE SEQUENCE ability_id_seq;
CREATE TABLE abilities (
	uid SMALLINT PRIMARY KEY DEFAULT nextval('ability_id_seq'),
	name VARCHAR(20) UNIQUE NOT NULL,
	description_id SMALLINT REFERENCES description_formats (uid),
	category VARCHAR(20),
	has_notes BOOLEAN, --  plan to remove?
	has_info BOOLEAN --  plan to remove?
);
ALTER SEQUENCE ability_id_seq OWNED BY abilities.uid;

-- table dropped - statement kept for reference
-- CREATE TABLE ability_info (
-- 	 uid INTEGER NOT NULL,
-- 	 hit_formula VARCHAR(8),
-- 	 accuracy INTEGER,
-- 	 element VARCHAR(16),
-- 	 friendly BOOLEAN,
-- 	 split BOOLEAN,
-- 	 target_all BOOLEAN,
-- 	 target_random BOOLEAN,
-- 	 num_attacks INTEGER,
-- 	 has_statuses BOOLEAN,
-- 	 has_damage BOOLEAN,
-- 	 PRIMARY KEY (uid),
-- 	 FOREIGN KEY (uid) REFERENCES abilities(uid)
-- );

CREATE TABLE ability_property_map (
	ability_id SMALLINT NOT NULL REFERENCES abilities (uid),
	type VARCHAR(16),
	value VARCHAR(16),
	PRIMARY KEY (ability_id, type, value)
);

CREATE TABLE ability_property_set (
	ability_id SMALLINT NOT NULL REFERENCES abilities (uid),
	type VARCHAR(16),
	PRIMARY KEY(ability_id, type)
);

CREATE TABLE ability_notes (
	ability_id SMALLINT NOT NULL REFERENCES abilities (uid),
	note_id SMALLINT NOT NULL,
	note_text TEXT,
	PRIMARY KEY (ability_id, note_id)
);

CREATE TABLE ability_damage (
	ability_id SMALLINT PRIMARY KEY REFERENCES abilities (uid),
	formula VARCHAR(12),
	power SMALLINT,
	long_range BOOLEAN,
	piercing BOOLEAN
);

CREATE TABLE ability_status_info (
	ability_id SMALLINT PRIMARY KEY REFERENCES abilities (uid),
	mode VARCHAR(8),
	chance SMALLINT
);

CREATE TABLE ability_status_list (
	ability_id SMALLINT NOT NULL REFERENCES abilities (uid),
	status VARCHAR(25) NOT NULL,
	PRIMARY KEY (ability_id, status)
);

--  MAGIC
CREATE TABLE magic_info (
	ability_id SMALLINT PRIMARY KEY REFERENCES abilities (uid),
	mp_cost SMALLINT,
	spell_type VARCHAR(8),
	reflectable BOOLEAN
);

--  SUMMONS
CREATE TABLE summon_info (
	ability_id SMALLINT PRIMARY KEY REFERENCES abilities (uid),
	mp_cost SMALLINT,
	possible_attacks SMALLINT
);

CREATE TABLE summon_attacks (
	summon_id SMALLINT NOT NULL REFERENCES abilities (uid),
	attack_id SMALLINT NOT NULL REFERENCES abilities (uid),
	PRIMARY KEY (summon_id, attack_id)
);

--  ENEMY SKILLS
CREATE TABLE enemy_skill_info (
  ability_id SMALLINT PRIMARY KEY REFERENCES abilities (uid),
  mp_cost SMALLINT,
  reflectable BOOLEAN,
  missable BOOLEAN,
  manip_only BOOLEAN
);

CREATE TABLE enemy_skill_users (
  ability_id SMALLINT NOT NULL REFERENCES abilities (uid),
  enemy_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (ability_id, enemy_name)
);
--  ===========================================================
