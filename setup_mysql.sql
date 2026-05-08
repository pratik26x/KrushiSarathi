-- KrushiSarathi — create database and tables for local MySQL
-- Default app credentials: user root, password root, database farmers_db
--
-- Apply schema + demo data in one step (recommended):
--   python init_database.py
--
-- Or CLI only:
--   mysql -u root -proot < setup_mysql.sql
--   mysql -u root -proot < seed_mysql.sql

CREATE DATABASE IF NOT EXISTS farmers_db;
USE farmers_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(512) NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  lab_name VARCHAR(255) NOT NULL,
  contact_person VARCHAR(255) NOT NULL,
  visit_date DATE NOT NULL,
  contact_number VARCHAR(64) NOT NULL,
  CONSTRAINT fk_appt_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_appointments_user ON appointments(user_id);
