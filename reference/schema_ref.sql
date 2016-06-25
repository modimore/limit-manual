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

-- ITEMS  =====================================================
CREATE TABLE items (
	uid SMALLINT PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	item_type VARCHAR(20),
	descr_id SMALLINT REFERENCES description_format (uid),
);

CREATE TABLE weapons (
	uid SMALLINT PRIMARY KEY REFERENCES items,
	name VARCHAR(20) NOT NULL,
	growth_rate SMALLINT,
	linked_slots SMALLINT,
	single_slots SMALLINT,
	attack SMALLINT,
	hit_pct SMALLINT,
	magic_bonus SMALLINT,
	element VARCHAR(16),
  wielder VARCHAR(10)
);

CREATE TABLE armor (
	uid SMALLINT PRIMARY KEY REFERENCES items,
	name VARCHAR(20) NOT NULL,
	growth_rate SMALLINT,
	linked_slots SMALLINT,
	single_slots SMALLINT,
	defense SMALLINT,
	magic_defense SMALLINT,
	defense_pct SMALLINT,
	magic_defense_pct SMALLINT
);
-- ============================================================

-- CHARACTERS  ================================================
CREATE TABLE characters (
 uid SMALLINT PRIMARY KEY,
 name VARCHAR(30) NOT NULL
);

CREATE TABLE character_intros (
 uid SMALLINT PRIMARY KEY REFERENCES character (uid),
 full_name VARCHAR(18) NOT NULL,
 job VARCHAR(33),
 age SMALLINT,
 weapon VARCHAR(40),
 height SMALLINT,
 birthdate VARCHAR(6),
 birthplace VARCHAR(13),
 blood_type VARCHAR(2),
 description TEXT
);
-- ============================================================

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

-- ENEMIES  ===================================================
CREATE SEQUENCE enemy_base_id_seq;
CREATE TABLE enemies (
	base_id SMALLINT PRIMARY KEY DEFAULT nextval('enemy_base_id_seq'),
	name VARCHAR(30),
	description TEXT,
	image VARCHAR(50)
);
ALTER SEQUENCE enemy_base_id_seq OWNED BY enemies.base_id;

CREATE SEQUENCE enemy_ver_id_seq;
CREATE TABLE enemy_versions (
	base_id SMALLINT NOT NULL REFERENCES enemies (base_id),
	ver_id SMALLINT PRIMARY KEY DEFAULT nextval('enemy_ver_id_seq'),
	ver_name VARCHAR(40),
	level SMALLINT,
	hp SMALLINT,
	mp SMALLINT,
	attack SMALLINT,
	defense SMALLINT,
	magic_attack SMALLINT,
	magic_defense SMALLINT,
	defense_pct SMALLINT,
	magic_defense_pct SMALLINT,
	dexterity SMALLINT,
	luck SMALLINT,
	exp SMALLINT,
	ap SMALLINT,
	gil SMALLINT
);
ALTER SEQUENCE enemy_ver_id_seq OWNED BY enemy_versions.ver_id;

CREATE TABLE enemy_status_immunities (
	enemy_ver_id SMALLINT NOT NULL REFERENCES enemy_versions (ver_id),
	status VARCHAR(25) NOT NULL,
	PRIMARY KEY (enemy_ver_id, status)
);

CREATE TABLE enemy_elemental_modifiers (
	enemy_ver_id SMALLINT NOT NULL REFERENCES enemy_versions (ver_id),
	element VARCHAR(11) NOT NULL,
	modifier SMALLINT,
	PRIMARY KEY (enemy_ver_id, element)
);

CREATE TABLE enemy_actions (
	enemy_ver_id SMALLINT NOT NULL REFERENCES enemy_versions (ver_id),
	action VARCHAR(20),
	name_hidden BOOLEAN,
	manipulate BOOLEAN,
	PRIMARY KEY (enemy_id, action)
);

CREATE TABLE enemy_items (
  enemy_ver_id SMALLINT NOT NULL REFERENCES enemy_versions (ver_id),
  item_slot_id SMALLINT NOT NULL DEFAULT 0,
  item_name VARCHAR(20) NOT NULL,
  get_method CHAR(1) NOT NULL,
  get_chance SMALLINT,
  PRIMARY KEY (enemy_ver_id, item_slot_id)
);

CREATE TABLE formations (
	uid SMALLINT PRIMARY KEY,
	attack_type SMALLINT
);

CREATE TABLE formation_locations (
	formation_id SMALLINT NOT NULL REFERENCES formations (uid),
	loc VARCHAR(40),
	sub_loc VARCHAR(40),
	PRIMARY KEY(formation_id,loc,sub_loc)
);

CREATE TABLE formation_enemies (
	formation_id SMALLINT NOT NULL REFERENCES formations(uid),
	row_num SMALLINT NOT NULL,
	position SMALLINT NOT NULL,
	enemy_ver_id SMALLINT REFERENCES enemy_versions (ver_id),
	PRIMARY KEY (formation_id, row_num, position)
);
-- ============================================================
