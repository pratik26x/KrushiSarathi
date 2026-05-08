-- KrushiSarathi — demo seed data (users + sample appointments)
-- Passwords (werkzeug scrypt hashes):
--   ravi@krushisarathi.local  / priya@krushisarathi.local  →  farmer123
--   amit@example.in  →  demo2026
--
-- WARNING: Clears existing rows in appointments and users.

USE farmers_db;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE appointments;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO users (username, email, password) VALUES
('Ravi Kumar', 'ravi@krushisarathi.local', 'scrypt:32768:8:1$WshuElBTPTjsTWuc$180cd884c209c9e1d147656a1f636fd1e9c1e232a80e3260413ff097565b85c541b8899c8ac015344f540c73650261038345fcef90adf705247b4421a6e25912'),
('Priya Sharma', 'priya@krushisarathi.local', 'scrypt:32768:8:1$WshuElBTPTjsTWuc$180cd884c209c9e1d147656a1f636fd1e9c1e232a80e3260413ff097565b85c541b8899c8ac015344f540c73650261038345fcef90adf705247b4421a6e25912'),
('Amit Patel', 'amit@example.in', 'scrypt:32768:8:1$E3A3mCHBzGzMBwSU$a2b1ed6c9db1a2d2889a7db642cc098e3ae91e54c8f8e4dd558f35e054a2431427e5ce6ff42fc3a3f0208918e1b5e6beb2d3b6df1c4560bde2647ea63eaec14b');

INSERT INTO appointments (user_id, lab_name, contact_person, visit_date, contact_number)
SELECT id, 'KrushiSarathi Soil Unit #1 — Pune', 'Amit K.', '2026-06-12', '+91 9876512345'
FROM users WHERE email = 'ravi@krushisarathi.local' LIMIT 1;

INSERT INTO appointments (user_id, lab_name, contact_person, visit_date, contact_number)
SELECT id, 'Agro Soil Diagnostics #1 — Bengaluru', 'Sneha R.', '2026-07-01', '+91 9876598765'
FROM users WHERE email = 'priya@krushisarathi.local' LIMIT 1;

INSERT INTO appointments (user_id, lab_name, contact_person, visit_date, contact_number)
SELECT id, 'Bhoomi Testing Centre #2 — Ahmedabad', 'Ravi S.', '2026-05-20', '+91 9876500001'
FROM users WHERE email = 'amit@example.in' LIMIT 1;

INSERT INTO appointments (user_id, lab_name, contact_person, visit_date, contact_number)
SELECT id, 'Precision Agri Lab #1 — Nagpur', 'Kiran P.', '2026-08-15', '+91 9876522222'
FROM users WHERE email = 'ravi@krushisarathi.local' LIMIT 1;
