-- CHARACTERS  ================================================
CREATE TABLE characters (
 uid SMALLINT PRIMARY KEY,
 name VARCHAR(30) NOT NULL
 category_id SMALLINT DEFAULT 0;
);

CREATE TABLE character_categories (
  uid SMALLINT PRIMARY KEY,
  name VARCHAR(20) UNIQUE
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
