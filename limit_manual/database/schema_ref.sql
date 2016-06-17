# ITEMS  =====================================================
CREATE TABLE items (
	uid INTEGER NOT NULL,
	name VARCHAR(20),
	item_type VARCHAR(20),
	descr_id INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY(descr_id) REFERENCES description_format (uid)
);

CREATE TABLE weapons (
	uid INTEGER NOT NULL,
	name VARCHAR(20),
	growth_rate INTEGER,
	linked_slots INTEGER,
	single_slots INTEGER,
	attack INTEGER,
	hit_pct INTEGER,
	magic_bonus INTEGER,
	element VARCHAR(16), wielder VARCHAR(10),
	PRIMARY KEY (uid),
	FOREIGN KEY(uid) REFERENCES item (uid)
);

CREATE TABLE armor (
	uid INTEGER NOT NULL,
	name VARCHAR(20),
	growth_rate INTEGER,
	linked_slots INTEGER,
	single_slots INTEGER,
	defense INTEGER,
	magic_defense INTEGER,
	defense_pct INTEGER,
	magic_defense_pct INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY(uid) REFERENCES item (uid)
);
# ============================================================

# CHARACTERS  ================================================
CREATE TABLE character (
	uid INTEGER NOT NULL,
	name VARCHAR(30),
	PRIMARY KEY (uid)
);

CREATE TABLE character_intro (
	uid INTEGER NOT NULL,
	full_name VARCHAR(18),
	job VARCHAR(33),
	age INTEGER,
	weapon VARCHAR(40),
	height INTEGER,
	birthdate VARCHAR(6),
	birthplace VARCHAR(13),
	blood_type VARCHAR(3),
	description VARCHAR(365),
	PRIMARY KEY (uid),
	FOREIGN KEY(uid) REFERENCES character (uid)
);
# ============================================================

# GENERAL DESCRIPTIONS  ======================================
CREATE TABLE description_format (
	uid INTEGER NOT NULL,
	format_string VARCHAR(80) NOT NULL,
	num_slots INTEGER,
	PRIMARY KEY (uid)
);

CREATE TABLE description_filler (
	referent_type VARCHAR(10) NOT NULL,
	referent_id INTEGER NOT NULL,
	place INTEGER NOT NULL,
	content VARCHAR(20),
	PRIMARY KEY (referent_type, referent_id, place)
);
# ============================================================

# ABILITIES ==================================================
CREATE TABLE abilities (
	uid INTEGER NOT NULL,
	name VARCHAR(20) NOT NULL,
	description_id INTEGER,
	category VARCHAR(20),
	has_notes BOOLEAN, # plan to remove?
	has_info BOOLEAN, # plan to remove?
	PRIMARY KEY (uid),
	UNIQUE (name),
	FOREIGN KEY(description_id) REFERENCES description_format (uid),
	CHECK (has_notes IN (0,1)),
	CHECK (has_info IN (0,1))
);

# table dropped -- statement kept for reference
-- CREATE TABLE ability_info (
-- 	uid INTEGER NOT NULL,
-- 	hit_formula VARCHAR(8),
-- 	accuracy INTEGER,
-- 	element VARCHAR(16),
-- 	friendly BOOLEAN,
-- 	split BOOLEAN,
-- 	target_all BOOLEAN,
--  target_random BOOLEAN,
--  num_attacks INTEGER,
-- 	has_statuses BOOLEAN,
-- 	has_damage BOOLEAN,
-- 	PRIMARY KEY (uid),
-- 	FOREIGN KEY (uid) REFERENCES ability(uid),
--  CHECK (friendly IN (0,1)),
--  CHECK (target_all IN (0,1)),
--  CHECK (target_random IN (0,1)),
-- 	CHECK (split IN (0, 1)),
--  CHECK (has_statuses IN (0,1)),
-- 	CHECK (has_damage IN (0, 1))
-- );

CREATE TABLE ability_property_map (
	ability_id INTEGER NOT NULL,
	type VARCHAR(16),
	value VARCHAR(16),
	PRIMARY KEY (ability_id, type, value)
);

CREATE TABLE ability_property_set (
	ability_id INTEGER NOT NULL,
	type VARCHAR(16),
	PRIMARY KEY(ability_id, type)
);

CREATE TABLE ability_notes (
	ability_id INTEGER NOT NULL,
	note_id INTEGER NOT NULL,
	note_text VARCHAR(80),
	PRIMARY KEY (ability_id, note_id),
	FOREIGN KEY(ability_id) REFERENCES ability (uid)
)

CREATE TABLE ability_damage (
	ability_id INTEGER NOT NULL,
	formula VARCHAR(12),
	power INTEGER,
	long_range BOOLEAN,
	piercing BOOLEAN,
	PRIMARY KEY (ability_id),
	FOREIGN KEY(ability_id) REFERENCES ability (uid),
	CHECK (long_range IN (0, 1)),
	CHECK (piercing IN (0, 1))
);

CREATE TABLE ability_status_info (
	ability_id INTEGER NOT NULL,
	mode VARCHAR(8),
	chance INTEGER,
	PRIMARY KEY (ability_id),
	FOREIGN KEY(ability_id) REFERENCES ability (uid)
);

CREATE TABLE ability_status_list (
	ability_id INTEGER NOT NULL,
	status VARCHAR(25) NOT NULL,
	PRIMARY KEY (ability_id, status),
	FOREIGN KEY(ability_id) REFERENCES ability (uid)
);

# MAGIC
CREATE TABLE magic_info (
	ability_id INTEGER NOT NULL,
	mp_cost INTEGER,
	spell_type VARCHAR(8),
	reflectable BOOLEAN,
	PRIMARY KEY (ability_id),
	FOREIGN KEY(ability_id) REFERENCES ability (uid),
	CHECK (reflectable IN (0, 1))
);

# SUMMONS
CREATE TABLE summon_info (
	ability_id INTEGER NOT NULL,
	mp_cost INTEGER,
	possible_attacks INTEGER,
	PRIMARY KEY (ability_id),
	FOREIGN KEY(ability_id) REFERENCES ability (uid)
);

CREATE TABLE summon_attacks (
	summon_id INTEGER NOT NULL,
	attack_id INTEGER NOT NULL,
	PRIMARY KEY (summon_id, attack_id),
	FOREIGN KEY(summon_id) REFERENCES ability (uid),
	FOREIGN KEY(attack_id) REFERENCES ability (uid)
);

# ENEMY SKILLS
CREATE TABLE enemy_skill_info (
  ability_id INTEGER NOT NULL,
  mp_cost INTEGER,
  reflectable BOOLEAN,
  missable BOOLEAN,
  manip_only BOOLEAN,
  PRIMARY KEY (ability_id),
  FOREIGN  KEY (ability_id) REFERENCES ability (uid),
  CHECK (reflectable in (0,1)),
  CHECK (missable in (0,1)),
  CHECK (manip_only in (0,1))
);

CREATE TABLE enemy_skill_users (
  ability_id INTEGER NOT NULL,
  enemy_name VARCHAR(30) NOT NULL,
  PRIMARY KEY (ability_id, enemy_name)
);
# ============================================================

# ENEMIES  ===================================================
CREATE TABLE enemies (
	base_id INTEGER NOT NULL,
	name VARCHAR(30),
	description VARCHAR(200),
	image VARCHAR(50),
	PRIMARY KEY (base_id)
);

CREATE TABLE enemy_versions (
	base_id INTEGER NOT NULL,
	ver_id INTEGER NOT NULL,
	ver_name VARCHAR(40),
	level INTEGER,
	hp INTEGER,
	mp INTEGER,
	attack INTEGER,
	defense INTEGER,
	magic_attack INTEGER,
	magic_defense INTEGER,
	defense_pct INTEGER,
	magic_defense_pct INTEGER,
	dexterity INTEGER,
	luck INTEGER,
	exp INTEGER,
	ap INTEGER,
	gil INTEGER,
	PRIMARY KEY (ver_id),
	FOREIGN KEY(base_id) REFERENCES enemies (base_id)
);

CREATE TABLE enemy_status_immunities (
	enemy_ver_id INTEGER NOT NULL,
	status VARCHAR(25) NOT NULL,
	PRIMARY KEY (enemy_ver_id, status),
	FOREIGN KEY(enemy_ver_id) REFERENCES enemy_versions (ver_id)
);

CREATE TABLE enemy_elemental_modifiers (
	enemy_ver_id INTEGER NOT NULL,
	element VARCHAR(11) NOT NULL,
	modifier INTEGER,
	PRIMARY KEY (enemy_ver_id, element),
	FOREIGN KEY(enemy_ver_id) REFERENCES enemy_versions (ver_id)
);

CREATE TABLE enemy_action (
	enemy_id INTEGER NOT NULL,
	action VARCHAR(20),
	name_hidden BOOLEAN,
	manipulate BOOLEAN,
	PRIMARY KEY (enemy_id),
	FOREIGN KEY(enemy_id) REFERENCES enemy_base (uid),
	CHECK (name_hidden IN (0, 1)),
	CHECK (manipulate IN (0, 1))
);

CREATE TABLE formations (
	uid INTEGER NOT NULL,
	attack_type INTEGER,
	PRIMARY KEY (uid)
);

CREATE TABLE formation_locations (
	formation_id INTEGER NOT NULL,
	loc VARCHAR(40),
	sub_loc VARCHAR(40),
	PRIMARY KEY(formation_id,loc,sub_loc),
	FOREIGN KEY(formation_id) REFERENCES formations (uid)
);

CREATE TABLE formation_enemies (
	formation_id INTEGER NOT NULL,
	row_num INTEGER NOT NULL,
	position INTEGER NOT NULL,
	enemy_ver_id INTEGER,
	PRIMARY KEY (formation_id, row_num, position),
	FOREIGN KEY(formation_id) REFERENCES formations (uid)
	FOREIGN KEY(enemy_ver_id) REFERENCES enemy_versions (ver_id)
);
# ============================================================
