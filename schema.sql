CREATE TABLE IF NOT EXISTS osis_users(id BIGSERIAL PRIMARY KEY,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,name TEXT NOT NULL,kelas TEXT NOT NULL DEFAULT '',jabatan TEXT NOT NULL,role TEXT NOT NULL,division TEXT NOT NULL,must_change BOOLEAN NOT NULL DEFAULT true,pwv INT NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS osis_records(id TEXT PRIMARY KEY,kind TEXT NOT NULL,division TEXT NOT NULL,value JSONB NOT NULL,creator BIGINT,created TIMESTAMPTZ DEFAULT now());
CREATE INDEX IF NOT EXISTS osis_kind_idx ON osis_records(kind);
CREATE TABLE IF NOT EXISTS osis_documents(id TEXT PRIMARY KEY,name TEXT NOT NULL,size INT NOT NULL,content BYTEA NOT NULL,created DATE DEFAULT CURRENT_DATE);
CREATE TABLE IF NOT EXISTS osis_settings(id INT PRIMARY KEY,value JSONB NOT NULL);
INSERT INTO osis_settings VALUES(1,'{"school":"Nama sekolah kamu","period":"Periode belum diatur","tagline":"Kelola kegiatan OSIS dalam satu tempat."}') ON CONFLICT DO NOTHING;
CREATE TABLE IF NOT EXISTS osis_attempts(k TEXT PRIMARY KEY,count INT NOT NULL,started TIMESTAMPTZ NOT NULL);
