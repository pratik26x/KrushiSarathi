# KrushiSarathi — Technical Project Report
## KrushiSarathi — Web Platform for Farmer Financial Inclusion and Agronomy Support

**Project:** KrushiSarathi  
**Stack:** Python Flask, MySQL, scikit-learn, HTML/CSS/JavaScript  
**Document version:** 1.0  

---

# Chapter 1 Introduction

## 1.1 Problem Statement

Smallholder and rural farmers often face fragmented access to information and services. Financial products (loans, government schemes, savings options), agronomic guidance (soil testing, crop choice), and digital tools are spread across different channels, with limited personalization. Many farmers lack a single, approachable interface that combines:

- Awareness of **financial inclusion** options relevant to agriculture.  
- **Soil testing** awareness and a practical path to engage with testing services.  
- **Data-driven crop recommendations** based on soil nutrients and weather-related parameters.  
- **Authentication** so personalized actions (e.g. booking appointments) can be tied to a user account.

The problem addressed by this project is to **design and implement a web application** that unifies these needs in one platform—**KrushiSarathi**—suitable for a Human–Computer Interaction (HCI) or capstone context, emphasizing clear navigation, informative content, and simple workflows.

## 1.2 Objectives

1. **Primary objective:** Deliver a working **web application** that presents farm-related **financial assistance** information and **facility** pages (data analysis, soil testing, crop recommendation).  
2. **User management:** Implement **registration and login** with **password hashing** and **session-based** state.  
3. **Machine learning:** Provide **crop recommendation** from user-supplied **N, P, K, temperature, humidity, pH, and rainfall** using a **trained Random Forest** model persisted as a **joblib** file.  
4. **Soil testing workflow:** Offer informational content, a **lab search** interface with sample lab data, and **appointment booking** persisted in a **MySQL** database for **logged-in** users.  
5. **Usability:** Use a **responsive, visually structured** frontend with animations and icons to support engagement and clarity (UX alignment).  
6. **Maintainability:** Provide a **training script** to regenerate the ML model from `Crop_data.csv` when data or hyperparameters change.

## 1.3 Scope

**In scope:**

- Server-rendered pages via **Flask** and **Jinja2** templates.  
- **MySQL** persistence for **users** and **appointments**.  
- **Crop recommendation** inference using **pre-trained** `crop_recommendation_model.pkl`.  
- Static informational pages for **loans, schemes, savings, data analysis**, and marketing **home** content.  
- Client-side **lab filtering** (hard-coded list) and **JSON API** for appointment confirmation.  
- Documentation of architecture (e.g. `FRONTEND.md`) and model training (`train_crop_model.py`).

**Out of scope (not implemented or partial):**

- **Payment gateways**, live credit scoring, or real-time integration with government scheme APIs.  
- **Real-time** soil sensor data or IoT integration.  
- **Production-grade** security hardening (e.g. environment-based secrets, HTTPS enforcement, rate limiting).  
- **Automated** test suite in CI; **admin dashboard** for appointments.  
- **Multi-language** UI beyond optional Google Translate hook (widget partially disabled in template).

---

# Chapter 2 Design

## 2.1 System Architecture

The system follows a **three-tier** style architecture adapted to a small Flask deployment.

### 2.1.1 Presentation layer

- **Templates:** `templates/*.html` — HTML with **Jinja2** (`url_for`, `session`, `flash`).  
- **Static assets:** `static/css/*`, `static/js/*`, `static/images/*`.  
- **External CDNs:** Icon fonts (Boxicons, Remix Icon, Font Awesome), **DotLottie** player for Lottie animations, optional Google Translate script.

### 2.1.2 Application layer

- **Framework:** **Flask** (`app.py`).  
- **Responsibilities:** Route handling, form processing, session management, JSON API for appointments, loading **joblib** model at startup, **MySQL** access via `mysql.connector`.

### 2.1.3 Data / ML layer

- **MySQL database** `farmers_db`: relational storage for users and appointments.  
- **Crop_data.csv:** Tabular dataset (N, P, K, temperature, humidity, ph, rainfall, crop) used to train the classifier.  
- **crop_recommendation_model.pkl:** Serialized **scikit-learn** `RandomForestClassifier` (100 trees, `random_state=42`), produced by `train_crop_model.py`.

### 2.1.4 Logical flow (simplified)

```
[Browser] --HTTP--> [Flask app.py]
                         |
         +---------------+---------------+
         |               |               |
   [Jinja templates]  [MySQL]     [joblib model]
         |               |               |
   [Static CSS/JS]   users,        predict(crop)
                     appointments
```

### 2.1.5 Key routes (summary)

| Route | Method | Purpose |
|--------|--------|---------|
| `/` | GET | Home |
| `/signup`, `/login` | GET, POST | Registration, authentication |
| `/logout` | GET | Clear session |
| `/recommendationForm` | GET, POST | Form + crop prediction |
| `/confirm_appointment` | POST | JSON appointment API |
| `/soilTesting`, `/test` | GET | Soil info + lab search |
| `/loans`, `/schemes`, `/savings`, etc. | GET | Information pages |

## 2.2 Database Design

The application expects a MySQL schema compatible with the SQL used in code. **DDL is not shipped in the repository**; the following is the **intended logical design**.

### 2.2.1 Entity: `users`

Stores registered accounts. Passwords are stored as **Werkzeug hashes** (not plaintext).

| Attribute | Description |
|-----------|-------------|
| `id` (PK) | Surrogate primary key |
| `username` | Display name |
| `email` | Unique login identifier |
| `password` | Hashed password |

**Usage:** `INSERT` on signup; `SELECT` by email on login; `user[0]` = id, `user[1]` = username, `user[3]` = hash per current code.

### 2.2.2 Entity: `appointments`

Stores soil-lab appointment bookings linked to users.

| Attribute | Description |
|-----------|-------------|
| `id` (PK) | Optional surrogate key (if added) |
| `user_id` (FK) | References `users.id` |
| `lab_name` | Name of selected lab |
| `contact_person` | Contact name from lab record |
| `visit_date` | Date of visit |
| `contact_number` | Phone string |

### 2.2.3 Example DDL (MySQL)

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  lab_name VARCHAR(255) NOT NULL,
  contact_person VARCHAR(255) NOT NULL,
  visit_date DATE NOT NULL,
  contact_number VARCHAR(64) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

# Chapter 3 Implementation

## 3.1 Frontend Development

- **Paradigm:** **Server-side rendering**; each URL returns full HTML.  
- **Structure:** One primary template per feature area (`index.html`, `signup.html`, `recommendationForm.html`, `test.html`, etc.).  
- **Styling:** Dedicated **CSS files** per page under `static/css/` for layout, typography, and responsive rules.  
- **JavaScript:**  
  - `signup.js` toggles login vs register panels.  
  - `script.js` implements **scroll-linked** transform/opacity for the **coin** graphic on the home page.  
  - `test.html` embeds **lab list** as a JavaScript array and uses **`fetch`** to POST JSON to `/confirm_appointment`.  
- **Animations:** **DotLottie** web component for hero and finance-section Lottie JSON; **CSS** transitions and keyframes; **scroll-triggered** classes on `soilTesting.html` (see `FRONTEND.md`).  
- **Accessibility / UX:** Clear sectioning (About, Facilities, Finance, Contact), anchor navigation, visual cards for facilities and financial themes.

## 3.2 Backend Development

- **Runtime:** Python 3 with **Flask**.  
- **Security:** `generate_password_hash` / `check_password_hash`; **Flask `session`** for `logged_in`, `username`, `user_id`.  
- **Database:** `mysql.connector` with a **global** connection and cursor (simple pattern; pooling not used).  
- **ML:** `joblib.load('crop_recommendation_model.pkl')` at import time; **`predict`** on POST to recommendation form.  
- **API:** `confirm_appointment` validates session, parses JSON keys `labName`, `contactPerson`, `visitDate`, `contactNumber`, inserts row, returns `jsonify` status.  
- **Training utility:** `train_crop_model.py` reads `Crop_data.csv`, stratified train/test split for **accuracy report**, fits **RandomForestClassifier** on full data, dumps **`crop_recommendation_model.pkl`**.

## 3.3 Integration

- **Form POST → Flask → Jinja result:** Recommendation form submits to `get_crop_recommendation`; response renders `recommendationResult.html` with `predicted_crop`.  
- **Session gate:** Appointment **fetch** requires `user_id` in session; otherwise JSON error.  
- **Static pipeline:** `url_for('static', filename='...')` resolves CSS/JS/images under `/static/`.  
- **Model lifecycle:** After CSV updates, run `python train_crop_model.py`; restart Flask to reload pickle if loader caches at startup only.

---

# Chapter 4 Testing

## 4.1 Test Cases

The following **manual** test cases align with implemented behavior. Automated pytest/Flask test client scripts are **not** part of the repository as delivered.

| ID | Module | Precondition | Steps | Expected result |
|----|--------|--------------|-------|-----------------|
| TC-01 | Auth | MySQL `users` exists | Register with new email | Success flash; redirect to login |
| TC-02 | Auth | Email exists | Register duplicate email | Error flash; stay on signup |
| TC-03 | Auth | User exists | Login with correct password | Session set; home shows welcome |
| TC-04 | Auth | — | Login wrong password | Error flash; redirect signup |
| TC-05 | ML | Model file present | Submit valid numeric form | Result page shows crop string |
| TC-06 | ML | — | Submit extreme but numeric values | Prediction returns (no crash) |
| TC-07 | Appointment | Not logged in | Confirm appointment from `/test` | Alert / JSON error message |
| TC-08 | Appointment | Logged in | Confirm with valid JSON | Success; redirect home |
| TC-09 | Navigation | — | Click facility/finance links | Correct template loads |
| TC-10 | Lab search | — | City/state match in JS list | Labs listed; no match shows message |

## 4.2 Results

- **Model training (`train_crop_model.py`):** On the bundled `Crop_data.csv`, a **20% stratified hold-out** run reported approximately **99.55% accuracy** (exact value may vary slightly with library versions). This indicates strong separability in the synthetic dataset; **real-field generalization** is not validated here.  
- **Functional smoke:** With MySQL tables created and credentials matching `app.py`, **signup/login**, **crop form**, and **appointment** flows operate as designed in manual checks.  
- **Known limitations:** `debug=True` in production is unsafe; **sklearn version** mismatch can warn on unpickling; **duplicate route** registration for `/recommendationForm` in `app.py` leaves redundant handler (second wins).

---

# Chapter 5 Conclusion

## 5.1 Summary

KrushiSarathi demonstrates an **integrated user-centered web platform** combining **information architecture** (financial and agronomy sections), **authenticated personalization** (appointments), and **machine learning** (crop recommendation from soil and climate features). The stack is **accessible to students and small teams**: Flask, Jinja, MySQL, and scikit-learn, with a documented frontend animation strategy. The project shows how **human-centered layout** and **progressive disclosure** (sections, cards, dedicated flows) can wrap technical backends for non-expert users.

## 5.2 Future Enhancements

1. **Security:** Move DB credentials and `SECRET_KEY` to **environment variables**; disable Flask debug in deployment; add **HTTPS** and **CSRF** protection on forms.  
2. **Backend structure:** **Connection pooling**, **blueprints**, and **ORM** (e.g. SQLAlchemy) for maintainability.  
3. **ML:** Model **versioning**, **confidence scores** or top-k crops, **input validation** ranges, retraining pipeline.  
4. **Features:** **Admin** view for appointments, **email/SMS** notifications, **real lab APIs**, **dashboard** analytics.  
5. **Quality:** **Automated tests** (pytest), **linting**, CI pipeline, accessibility audit (WCAG).  
6. **UX:** Replace hard-coded lab list with **database or API**; fix stray markup in `index.html`; complete or remove Google Translate integration.

---

# Chapter 6 References

1. Flask Documentation. https://flask.palletsprojects.com/  
2. Jinja2 Documentation. https://jinja.palletsprojects.com/  
3. scikit-learn: RandomForestClassifier. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html  
4. MySQL Connector/Python. https://dev.mysql.com/doc/connector-python/en/  
5. Werkzeug Security — Password Hashing. https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security  
6. Joblib persistence. https://joblib.readthedocs.io/  
7. Lottie / DotLottie ecosystem. https://lottiefiles.com/ (community resources)  
8. Nielsen, J., & Molich, R. (1990). Heuristic evaluation of user interfaces. *Proc. CHI* (HCI heuristics context).  

*(Add course textbook, institution guidelines, and dataset source if Crop_data.csv is from a specific repository, e.g. Kaggle.)*

---

# Chapter 7 Appendices

## Appendix A — Feature list for crop model

`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall` → target `crop` (22 classes in dataset).

## Appendix B — Running the application

1. Install Python dependencies: `flask`, `mysql-connector-python`, `werkzeug`, `joblib`, `numpy`, `pandas`, `scikit-learn`.  
2. Create MySQL database `farmers_db` and tables per Chapter 2.  
3. Ensure `crop_recommendation_model.pkl` exists (run `train_crop_model.py` if needed).  
4. Run: `python app.py` → open `http://127.0.0.1:5001`.

## Appendix C — File inventory (core)

- `app.py` — Application entry.  
- `templates/` — HTML views.  
- `static/` — CSS, JS, images.  
- `Crop_data.csv` — Training data.  
- `train_crop_model.py` — Training script.  
- `crop_recommendation_model.pkl` — Serialized model.  
- `FRONTEND.md` — Frontend and animation notes.

---

# Chapter 8 Annexure — Progress Sheet

Use this table to record weekly or milestone progress. **Edit dates and status to match your project plan.**

| Week / Milestone | Planned activities | Completed (Y/N) | Remarks / evidence |
|------------------|-------------------|-----------------|---------------------|
| 1 | Requirements, problem statement, literature | | |
| 2 | UI wireframes, database schema design | | |
| 3 | Flask setup, home + static pages | | |
| 4 | Auth (signup/login), MySQL integration | | |
| 5 | Crop recommendation form + model integration | | |
| 6 | Soil testing pages + lab search + appointment API | | |
| 7 | Styling, animations, UI/UX refinements | | |
| 8 | Testing, documentation, report / demo | | |

**Sign-off (optional)**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Student | | | |
| Guide / Instructor | | | |

---

*End of report.*
