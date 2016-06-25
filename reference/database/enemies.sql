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
