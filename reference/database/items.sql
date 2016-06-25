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
