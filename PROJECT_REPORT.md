# KrushiSarathi — Technical Project Report  
## Web Platform for Farmer Financial Inclusion, Soil Testing, and AI-Based Crop Recommendation  

| Field | Detail |
|-------|--------|
| **Project title** | KrushiSarathi |
| **Domain** | Agriculture, financial inclusion, Human–Computer Interaction (HCI) |
| **Implementation stack** | Python 3, Flask, Jinja2, MySQL, scikit-learn, HTML5, CSS3, JavaScript |
| **Document version** | 2.0 (detailed) |
| **Companion docs** | `FRONTEND.md` (UI/animation), `train_crop_model.py` (ML pipeline) |

---

# Chapter 1 Introduction

## 1.1 Problem Statement

### 1.1.1 Background and context  

Agriculture remains a cornerstone of rural economies. Farmers must repeatedly make decisions that depend on **soil condition**, **weather**, **market-linked crop choice**, and access to **credit and government programs**. In practice, information arrives through **disjoint channels**: extension workers, word of mouth, printed notices, mobile messages, and generic websites. Digital literacy and connectivity vary widely, so interfaces must be **simple**, **scannable**, and **task-oriented**—core concerns of Human–Computer Interaction (HCI).

**Financial inclusion** in this context means helping users **discover** loans, savings concepts, and government **schemes** relevant to farming, even when the prototype does not connect to live banking APIs. **Agronomic support** includes raising awareness of **soil testing** and offering a **structured path** (information → find lab → book appointment) plus **algorithmic crop suggestions** from measurable inputs.

### 1.1.2 Core problems addressed  

1. **Fragmentation:** Financial and agronomic information is not presented in one **coherent** navigation model (single home with clear sections: About, Facilities, Finance, Contact).  
2. **Lack of personalization for actions:** Booking a soil-test appointment should be tied to an **identity** (session/user id) so records are auditable and user-specific.  
3. **Opaque crop choice:** Farmers may not know which crop fits **current N–P–K, pH, humidity, temperature, and rainfall** patterns; a **data-driven** suggestion can support planning (with the caveat that real agronomy needs local expertise).  
4. **Usability gap:** Many agricultural portals are **text-heavy** or **admin-centric**; this project emphasizes **visual hierarchy**, **cards**, **animations**, and **progressive disclosure** appropriate to a course or demonstration setting.

### 1.1.3 Problem statement (concise)  

The project addresses the need for a **unified, user-facing web application**—“**KrushiSarathi**”—that combines (a) **information and navigation** for financial assistance themes, (b) **soil testing** content and **lab search** with **database-backed appointment booking** for registered users, and (c) **machine-learning-based crop recommendation** from soil and climate parameters, implemented with **Flask**, **MySQL**, and a **Random Forest** model trained on `Crop_data.csv`.

### 1.1.4 Stakeholders (typical)  

| Stakeholder | Interest |
|-------------|----------|
| **Farmers / end users** | Easy navigation, trust cues, clear forms, understandable outputs. |
| **Students / developers** | Learnable codebase, reproducible model training. |
| **Instructors / evaluators** | Clear documentation, testability, UX justification. |
| **Future maintainers** | Separation of concerns, scripts for retraining, schema documentation. |

---

## 1.2 Objectives

### 1.2.1 General objectives  

- **G1:** Design an information architecture that maps **user goals** (learn, explore, recommend, book) to **pages and flows**.  
- **G2:** Implement a **full-stack prototype** deployable on a developer machine (localhost).  
- **G3:** Integrate **supervised learning** into a form-based workflow with **visible, textual** results.  
- **G4:** Document **design decisions**, **limitations**, and **future work** for academic or portfolio use.

### 1.2.2 Specific objectives  

| ID | Objective | Measurable indicator |
|----|-----------|----------------------|
| **O1** | Home page with sections and links to all major features | All facility/finance links resolve to correct routes |
| **O2** | User registration with **unique email** and **hashed** password | Duplicate email rejected; login verifies hash |
| **O3** | Session-based **login state** on home (welcome / sign-in) | `session` keys set and cleared on logout |
| **O4** | Crop recommendation from **7 numeric fields** | POST returns rendered result with crop label |
| **O5** | Persist soil-lab **appointments** for logged-in users | Row in `appointments` with correct `user_id` |
| **O6** | Lab discovery UI with **filter** by city + state | JS list filters; empty state message when no match |
| **O7** | Regenerate ML artifact from CSV | `train_crop_model.py` writes `.pkl`; hold-out accuracy printed |
| **O8** | Frontend polish (CSS per page, motion) | DotLottie + scroll/coin + soil page animations as in `FRONTEND.md` |

---

## 1.3 Scope

### 1.3.1 Functional scope (included)  

- **Marketing / landing:** Hero, about, facility cards, finance cards, footer, optional translation hook.  
- **Authentication:** Signup, login (shared template with toggle), logout.  
- **Content pages:** Data analysis, soil testing intro, crop recommendation intro, loans, loan details, schemes, savings.  
- **Crop pipeline:** `recommendationForm.html` → POST → `RandomForestClassifier.predict` → `recommendationResult.html`.  
- **Soil pipeline:** `soilTesting.html` → link to `test.html` → select lab → `fetch` POST JSON → `confirm_appointment` → MySQL insert.  
- **ML training script:** Stratified split metric + full-data fit + `joblib.dump`.  

### 1.3.2 Non-functional scope (included at prototype level)  

- **Usability:** Consistent nav patterns, anchor links, `scroll-behavior: smooth` on `html`.  
- **Performance:** Small dataset and single model load at startup; acceptable for demo.  
- **Maintainability:** Separate templates and CSS files; training isolated in `train_crop_model.py`.

### 1.3.3 Out of scope  

| Area | Reason / note |
|------|----------------|
| Live **banking / scheme APIs** | Would require legal integration and keys |
| **Mobile native apps** | Web-only prototype |
| **IoT / real-time soil sensors** | No hardware pipeline |
| **Production DevOps** | No Docker/K8s/nginx in repo |
| **Automated regression tests** | Manual test matrix in Chapter 4 |
| **Internationalization (i18n)** | Only partial Google Translate experiment |
| **Role-based admin portal** | No admin user model |

### 1.3.4 Assumptions and constraints  

- **Assumption:** MySQL server runs locally with database `farmers_db` and credentials matching `app.py` (`localhost`, `root`/`root` in source—**must be changed** for any shared deployment).  
- **Assumption:** `crop_recommendation_model.pkl` exists beside `app.py` before server start (or training script run first).  
- **Constraint:** Model is trained on **tabular synthetic-style** data; **field validation** in forms is HTML5 `required` / `step` only—not agronomic plausibility bounds.  
- **Constraint:** Flask `debug=True`—suitable for **development only**.

---

# Chapter 2 Design

## 2.1 System Architecture

### 2.1.1 Architectural style  

The application uses a **classical web architecture**: **thin client** (browser), **application server** (Flask), **database server** (MySQL), plus **file-based ML artifact** (pickle). This is a variant of **three-tier** architecture where the presentation tier is **HTML generated server-side** rather than a SPA consuming JSON for every screen.

### 2.1.2 Logical layers  

**Presentation layer**  

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| Structure | HTML5 + Jinja2 | Sections, forms, semantic markup |
| Style | CSS (per-page files) | Layout, typography, responsive rules, animations |
| Client logic | Vanilla JS | Scroll effects, signup toggle, `fetch` API |
| Rich media | DotLottie (CDN) | Vector animations from remote JSON |

**Application layer**  

| Component | Responsibility |
|-----------|----------------|
| `app.py` | URL routing, request dispatch, session, flash |
| View functions | Render templates or return `jsonify` |
| Werkzeug | Password hashing |
| `joblib` | Load classifier at import time |

**Data / intelligence layer**  

| Store | Role |
|-------|------|
| MySQL `farmers_db` | Users, appointments |
| `Crop_data.csv` | Source for offline training |
| `crop_recommendation_model.pkl` | Serialized `RandomForestClassifier` |

### 2.1.3 Deployment view (development)  

```
┌─────────────────┐     HTTP :5001      ┌──────────────────────────────┐
│  Web browser    │ ◄──────────────────►│  Flask (app.py)              │
└─────────────────┘                     │  - Jinja rendering           │
        │                               │  - Session cookies           │
        │ HTTPS (CDN)                   │  - joblib model in memory    │
        ▼                               └───────────┬────────────────┘
  unpkg, cdnjs, lottie.host                           │
                                                      │ mysql.connector
                                                      ▼
                                          ┌──────────────────────────────┐
                                          │  MySQL (farmers_db)          │
                                          └──────────────────────────────┘
```

### 2.1.4 Component diagram (modules)  

- **`app.py`**: Monolithic Flask app (all routes in one file).  
- **`templates/`**: One-to-one mapping with major user journeys.  
- **`static/css/`**: `style.css` (home), `signup.css`, `recommendationForm.css`, `test.css`, `soilTesting.css`, etc.  
- **`static/js/`**: `script.js`, `signup.js`.  
- **`train_crop_model.py`**: Offline batch training—**not** invoked by Flask at runtime.

### 2.1.5 Sequence: user login (high level)  

1. Client GET `/login` → server returns `signup.html` (login mode).  
2. Client POST email + password → server `SELECT * FROM users WHERE email=%s`.  
3. If row exists, `check_password_hash(stored, submitted)` → on success set `session['logged_in']`, `session['username']`, `session['user_id']`.  
4. Response: render `index.html` with session visible in template.

### 2.1.6 Sequence: crop recommendation  

1. Client GET `/recommendationForm` → form HTML.  
2. Client POST seven fields → server parses floats, builds `[[N,P,K,temp,humidity,ph,rainfall]]`.  
3. `model.predict(...)[0]` → string label (e.g. `rice`).  
4. Server renders `recommendationResult.html` with `predicted_crop` in context.

### 2.1.7 Sequence: appointment booking  

1. Client on `/test` selects lab → JS stores `labName`, `contactPerson`, `visitDate`, `contactNumber`.  
2. `fetch('/confirm_appointment', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON })`.  
3. Server: if no `user_id` in session → `{"status":"error","message":"..."}`.  
4. Else `INSERT INTO appointments (...)` → `{"status":"success"}`.  
5. Client on success redirects to home via `window.location`.

### 2.1.8 Route reference (complete list from `app.py`)  

| Route | Methods | View / behavior |
|-------|---------|-----------------|
| `/` | GET | `home` → `index.html` |
| `/dashboard` | GET | Placeholder string |
| `/dataAnalysis` | GET | `dataAnalysis.html` |
| `/soilTesting` | GET | `soilTesting.html` |
| `/test` | GET | `test.html` (lab search) |
| `/cropRecommendation` | GET | `cropRecommendation.html` |
| `/recommendationForm` | GET | *Overridden* — see note below |
| `/recommendationForm` | GET, POST | `get_crop_recommendation` — form display + POST handler |
| `/recommendationResult` | GET | `recommendationResult.html` (no prediction if opened alone) |
| `/loans` | GET | `loans.html` |
| `/loanDetails` | GET | `loanDetails.html` |
| `/schemes` | GET | `schemes.html` |
| `/savings` | GET | `savings.html` |
| `/signup` | GET, POST | Registration |
| `/login` | GET, POST | Authentication |
| `/logout` | GET | Session clear + home |
| `/confirm_appointment` | POST | JSON API |

**Note:** `/recommendationForm` is registered twice; Flask uses the **last** registration for GET/POST, so `get_crop_recommendation` handles both. The first `recommendationForm()` function is redundant.

---

## 2.2 Database Design

### 2.2.1 Conceptual model (ER-level)  

- **USER** — independent entity; identified by `id`.  
- **APPOINTMENT** — weak association to USER; each appointment belongs to exactly one user (`user_id` FK).  
- No many-to-many tables in current scope.

### 2.2.2 Logical schema — `users`  

| Column | Type (suggested) | Constraints | Description |
|--------|------------------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Internal id |
| `username` | VARCHAR(255) | NOT NULL | Shown in navbar welcome |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | Login key |
| `password` | VARCHAR(255) | NOT NULL | Werkzeug hash string |

**Integrity:** `UNIQUE(email)` enforces one account per email; signup catches `IntegrityError`.

### 2.2.3 Logical schema — `appointments`  

| Column | Type (suggested) | Constraints | Description |
|--------|------------------|-------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Optional row id |
| `user_id` | INT | NOT NULL, FK → users(id) | Owner |
| `lab_name` | VARCHAR(255) | NOT NULL | From client JSON `labName` |
| `contact_person` | VARCHAR(255) | NOT NULL | `contactPerson` |
| `visit_date` | DATE | NOT NULL | Parsed from `visitDate` (YYYY-MM-DD) |
| `contact_number` | VARCHAR(64) | NOT NULL | `contactNumber` |

### 2.2.4 Physical DDL (MySQL)  

```sql
CREATE DATABASE IF NOT EXISTS farmers_db;
USE farmers_db;

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
  CONSTRAINT fk_appt_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_appointments_user ON appointments(user_id);
```

`ON DELETE CASCADE` is optional but keeps orphan rows from accumulating if a user is removed during testing.

### 2.2.5 Mapping application tuples to columns  

Login code uses `cursor.execute("SELECT * FROM users WHERE email=%s", (email,))` and `user[3]` for password hash → implies column order **(id, username, email, password)** as in DDL above.

---

# Chapter 3 Implementation

## 3.1 Frontend Development

### 3.1.1 Rendering model  

Flask **server-side rendering**: the response body is **HTML** after Jinja evaluation. No React/Vue router; navigation is **full page** loads (except same-page anchors). Static files are served from `/static/...` via Flask’s static handler and `url_for('static', ...)`.

### 3.1.2 Template inventory  

| Template | Purpose |
|----------|---------|
| `index.html` | Landing: nav, hero, DotLottie, about, facilities, finance, horizontal CTA, footer |
| `signup.html` | Dual-mode login/register UI |
| `dataAnalysis.html` | Data analysis facility page |
| `soilTesting.html` | Soil service narrative + link to lab booking |
| `test.html` | Lab search + confirmation modal + `fetch` |
| `cropRecommendation.html` | Intro + link to form |
| `recommendationForm.html` | Seven numeric inputs, POST to `get_crop_recommendation` |
| `recommendationResult.html` | Displays `predicted_crop` |
| `loans.html`, `loanDetails.html`, `schemes.html`, `savings.html` | Financial content |

### 3.1.3 Form fields — crop recommendation  

| HTML `name` | Model feature | Type |
|-------------|---------------|------|
| `nitrogen` | N | number |
| `phosphorous` | P | number |
| `potassium` | K | number |
| `temperature` | temperature | number |
| `humidity` | humidity | number |
| `ph` | ph | number |
| `rainfall` | rainfall | number |

Order in `input_data` **must** match training feature order in `train_crop_model.py`.

### 3.1.4 Client-side modules  

- **`signup.js`:** Toggles CSS class on `.wrapper` to switch register vs login panels (`register-link` / `login-link` click).  
- **`script.js`:** On scroll, reads `.Benefits-section` position, computes progress in [0,1], sets `.coin-container` **inline** `transform` and `opacity`.  
- **`test.html` inline script:** Array of lab objects `{ name, city, state, contactPerson, visitDate, contactNumber }`; `filter` on city (case-insensitive) and state; list item click opens modal; confirm calls `confirmAppointmentBackend()`.

### 3.1.5 Styling and UX choices  

- **Visual hierarchy:** Large hero headline, section titles, card grids for facilities and finance.  
- **Affordances:** Buttons and “Explore” links clearly labeled; facility images reinforce meaning.  
- **Feedback:** Flask `flash` for auth errors/success; appointment flow uses `alert` on API error.  
- **Motion:** DotLottie for engagement; scroll-linked coin for **dynamic** feedback; soil page uses `data-animate` + CSS keyframes for **reveal on scroll** (see `FRONTEND.md`).

### 3.1.6 External dependencies (CDN)  

Boxicons, Remix Icon, Font Awesome 6, Google Translate loader (partial), `@dotlottie/player-component` from unpkg, Lottie JSON from lottie.host.

---

## 3.2 Backend Development

### 3.2.1 Application bootstrap  

- `Flask(__name__)`; `secret_key` set in source (**should use env var** in production).  
- **Eager** MySQL connection at module level—simple but **blocks** if DB down at import.  
- **Eager** `joblib.load('crop_recommendation_model.pkl')`—failure prevents app start (fail-fast for ML).  

### 3.2.2 Authentication implementation  

- **Signup:** `generate_password_hash(password)` → `INSERT INTO users (username, email, password) VALUES (...)`.  
- **Login:** Select by email only, then `check_password_hash(user[3], password)`.  
- **Session keys:** `logged_in` (bool), `username` (str), `user_id` (int).  
- **Logout:** `session.pop` for keys; render home.

### 3.2.3 Machine learning stack  

| Item | Detail |
|------|--------|
| Algorithm | `sklearn.ensemble.RandomForestClassifier` |
| Hyperparameters | `n_estimators=100`, `random_state=42`, defaults otherwise (e.g. `max_features='sqrt'`, `criterion='gini'`) |
| Training data | `Crop_data.csv`, ~2200 rows, **22** crop classes |
| Training script | `train_crop_model.py`: stratified 80/20 split for **reported accuracy**, then fit on **all** rows for deployment artifact |
| Serialization | `joblib.dump` / `joblib.load` |
| Inference | `model.predict([[...]])[0]` returns numpy str_ / string label |

### 3.2.4 REST-style JSON endpoint  

**`POST /confirm_appointment`**  

- **Content-Type:** `application/json`  
- **Expected body keys:** `labName`, `contactPerson`, `visitDate` (ISO date string), `contactNumber`  
- **Success:** `200`, `{"status":"success"}`  
- **Auth failure:** `200` with `{"status":"error","message":"Please log in..."}` (client shows alert)  
- **DB error:** `200` with `{"status":"error","message": "<mysql message>"}`  

*Note: HTTP 401/403 could be used in a refactored API.*

### 3.2.5 Error handling patterns  

- **MySQL IntegrityError** on duplicate email → user-friendly flash + redirect.  
- **Generic mysql.connector.Error** on appointment insert → JSON error payload.  
- **No** global Flask error handler in source; **debug** exposes tracebacks when enabled.

### 3.2.6 Server run configuration  

`app.run(debug=True, port=5001)` — development server, **not** production-grade.

---

## 3.3 Integration

### 3.3.1 End-to-end data flow — recommendation  

```
Browser form POST
    → Werkzeug parses form
    → Float conversion in get_crop_recommendation
    → NumPy/sklearn predict path
    → Jinja renders recommendationResult.html with predicted_crop
```

### 3.3.2 End-to-end data flow — appointment  

```
Browser JS builds object matching backend keys
    → fetch POST JSON
    → Flask request.get_json()
    → datetime.strptime(..., '%Y-%m-%d').date()
    → Parameterized INSERT
    → jsonify response
    → JS navigates on success
```

### 3.3.3 Session integration  

Templates use `{% if session.logged_in %}` for conditional navbar. **Most routes do not enforce** login decorators; only appointment API checks `user_id`. Extending with `@login_required` would harden the app.

### 3.3.4 Static and template URL generation  

`url_for('static', filename='css/style.css')` ensures correct paths regardless of app root. `url_for('home')`, `url_for('loans')`, etc., centralize route names.

### 3.3.5 Model retraining workflow  

1. Edit or replace `Crop_data.csv`.  
2. Run `python train_crop_model.py`.  
3. Restart Flask process to reload `crop_recommendation_model.pkl` (module-level load).

---

# Chapter 4 Testing

## 4.1 Test Cases

### 4.1.1 Authentication  

| ID | Description | Preconditions | Steps | Expected |
|----|-------------|---------------|-------|----------|
| TC-A1 | Valid registration | DB up, new email | Fill signup, submit | Success flash; redirect toward login |
| TC-A2 | Duplicate email | Email exists | Register same email | Error flash; IntegrityError handled |
| TC-A3 | Valid login | User exists | Correct email/password | Session populated; welcome on home |
| TC-A4 | Wrong password | User exists | Wrong password | Error flash; redirect signup |
| TC-A5 | Logout | Logged in | Visit logout | Session cleared; home without welcome |
| TC-A6 | SQL injection attempt (sanity) | — | Enter quotes in email field | Parameterized query; no syntax execution |

### 4.1.2 Crop recommendation  

| ID | Description | Steps | Expected |
|----|-------------|-------|----------|
| TC-M1 | Typical rice-like row | Enter values similar to first CSV rice row | Predicted label reasonable (e.g. rice) |
| TC-M2 | Required fields | Submit empty form | Browser/HTML5 validation prevents submit |
| TC-M3 | Decimal values | Use `step="any"` floats | Accepts and predicts |
| TC-M4 | Missing model file | Remove/rename pkl, start app | Import error at startup (fail-fast) |

### 4.1.3 Appointments and labs  

| ID | Description | Steps | Expected |
|----|-------------|-------|----------|
| TC-S1 | Search match | City/state matching JS data | Labs listed |
| TC-S2 | No match | Random city | “No labs found” message |
| TC-S3 | Confirm without login | Guest user confirms | Error JSON; alert |
| TC-S4 | Confirm logged in | Login, book | Success; DB row; redirect home |
| TC-S5 | Malformed JSON | Manual API test with bad body | Server error / exception (observe behavior) |

### 4.1.4 Navigation and UI  

| ID | Description | Expected |
|----|-------------|----------|
| TC-N1 | Each facility “Explore” | Correct template 200 OK |
| TC-N2 | Finance links | loans/schemes/savings load |
| TC-N3 | Anchor links from home | Smooth scroll to section ids |
| TC-N4 | Soil flow | soilTesting → test page reachable |

### 4.1.5 Training script  

| ID | Description | Expected |
|----|-------------|----------|
| TC-T1 | Run `train_crop_model.py` | Accuracy printed; pkl written |
| TC-T2 | Corrupt CSV | Script exits with missing-column message |

---

## 4.2 Results

### 4.2.1 Model evaluation (offline)  

- **Method:** 80% train / 20% test, **stratified** by `crop`, `random_state=42`.  
- **Metric:** Accuracy on hold-out set.  
- **Observed (representative):** ~**99.55%** on bundled data—expected because classes are well separated in the synthetic dataset.  
- **Limitation:** No separate **real-world** validation set; **precision/recall per crop** not reported in app.

### 4.2.2 Functional testing summary  

- **Auth:** Hashing and session behavior align with design when MySQL schema matches code assumptions.  
- **ML:** Prediction latency negligible for single-row inference on localhost.  
- **Appointments:** JSON contract matches between `test.html` and `confirm_appointment`.  

### 4.2.3 Known defects / technical debt  

| Item | Severity | Note |
|------|----------|------|
| Duplicate `/recommendationForm` route | Low | Dead first handler |
| `debug=True` | High if exposed | Disable in production |
| Hard-coded DB password | High | Use environment configuration |
| Stray `` ` `` in `index.html` | Medium | Can break DOM/layout |
| No CSRF tokens on forms | Medium | Acceptable only for local demo |
| `GET /recommendationResult` without POST | Low | Empty/missing prediction context |

### 4.2.4 Compatibility notes  

- **scikit-learn version:** Pickle may warn if train and load versions differ; retrain with target environment to avoid risk.

---

# Chapter 5 Conclusion

## 5.1 Summary  

KrushiSarathi successfully **integrates** three concerns in one prototype: **user-centered presentation** (structure, visuals, motion), **classical web backend** patterns (sessions, relational data, parameterized SQL), and **practical ML deployment** (pickle load, single predict call). The crop module demonstrates the full path from **dataset** → **training script** → **artifact** → **user form** → **interpretable output** (crop name). The soil-testing module combines **educational content**, **client-side search**, and **server persistence** for a concrete “book appointment” story.

The project is appropriate as a **learning artifact**: dependencies are mainstream, the architecture is easy to explain in a report or viva, and limitations are clear enough to discuss professionally (security, validation, generalization).

## 5.2 Future Enhancements  

### 5.2.1 Security and operations  

- Environment-based **secrets** (`SECRET_KEY`, `DATABASE_URL`).  
- **HTTPS**, **secure cookies**, **CSRF** protection (`Flask-WTF`).  
- **Rate limiting** on login and appointment endpoints.  
- **Production WSGI** server (gunicorn, waitress) behind reverse proxy.

### 5.2.2 Software engineering  

- **Blueprints** per domain (auth, agronomy, finance).  
- **SQLAlchemy** ORM + migrations (Alembic).  
- **pytest** + Flask test client + factory fixtures for users.  
- **Linting** (ruff/flake8) and **typing** for core modules.

### 5.2.3 Machine learning  

- **Probability outputs** (`predict_proba`) and top-3 crops in UI.  
- **Feature importance** or SHAP for explainability (farmer trust).  
- **Plausibility checks** on inputs (ranges by region).  
- **Separate** train/validation/test and **document** metrics per class.

### 5.2.4 Product features  

- **Admin dashboard** for appointments; export CSV.  
- **Email/SMS** confirmations.  
- **Lab directory** from database with CRUD.  
- **Multilingual** content files instead of machine translation only.  
- **Progressive Web App** offline shell for low connectivity.

---

# Chapter 6 References

1. Flask Project. *Flask Documentation.* https://flask.palletsprojects.com/  
2. Pallets. *Jinja2 Documentation.* https://jinja.palletsprojects.com/  
3. Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html  
4. scikit-learn Developers. *RandomForestClassifier.* https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html  
5. Oracle. *MySQL Connector/Python Developer Guide.* https://dev.mysql.com/doc/connector-python/en/  
6. Pallets. *Werkzeug — Security.* https://werkzeug.palletsprojects.com/  
7. Joblib Development Team. *Joblib: running Python functions as pipeline jobs.* https://joblib.readthedocs.io/  
8. The Pandas Development Team. *pandas documentation.* https://pandas.pydata.org/docs/  
9. MDN Web Docs. *Fetch API, CSS animations, Custom elements.* https://developer.mozilla.org/  
10. Nielsen, J. (1994). *Usability Heuristics.* Nielsen Norman Group (evolution of heuristic evaluation).  
11. Norman, D. A. *The Design of Everyday Things* (revised)—principles relevant to affordances and feedback.  
12. LottieFiles / DotLottie community resources. https://lottiefiles.com/  

*(Add: your institution’s project guidelines, course slides, and the **exact provenance** of `Crop_data.csv` if known—e.g. Kaggle “Crop Recommendation Dataset”.)*

---

# Chapter 7 Appendices

## Appendix A — Crop classes (22 labels in dataset)  

Examples present in `Crop_data.csv`: rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee. *(Verify with `df['crop'].unique()` if the file changes.)*

## Appendix B — Sample training command log  

```
Hold-out accuracy (20% stratified): 0.9955
Saved model (2200 samples, 22 classes) -> ...\crop_recommendation_model.pkl
```

## Appendix C — Dependencies (pip)  

```
flask
mysql-connector-python
werkzeug
joblib
numpy
pandas
scikit-learn
```

Install example: `pip install flask mysql-connector-python werkzeug joblib numpy pandas scikit-learn`

## Appendix D — Environment variables (recommended future)  

| Variable | Purpose |
|----------|---------|
| `FLASK_SECRET_KEY` | Session signing |
| `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` | DB connection |

## Appendix E — Glossary  

| Term | Meaning |
|------|---------|
| **SSR** | Server-side rendering |
| **PK** | Primary key |
| **FK** | Foreign key |
| **RF** | Random Forest |
| **HCI** | Human–Computer Interaction |
| **JSON** | JavaScript Object Notation |
| **API** | Application Programming Interface |

## Appendix F — Full file inventory  

| Path | Role |
|------|------|
| `app.py` | Flask application |
| `train_crop_model.py` | Train and save `.pkl` |
| `Crop_data.csv` | ML training data |
| `crop_recommendation_model.pkl` | Trained classifier |
| `templates/*.html` | Views |
| `static/css/*.css` | Styles |
| `static/js/*.js` | Client scripts |
| `FRONTEND.md` | Animation/rendering documentation |
| `PROJECT_REPORT.md` | This report |

---

# Chapter 8 Annexure — Progress Sheet

### 8.1 Milestone tracking  

| # | Phase | Planned deliverables | Done (Y/N) | Evidence (link / note) |
|---|--------|----------------------|------------|-------------------------|
| 1 | Initiation | Problem statement, objectives, scope | | |
| 2 | Requirements | User stories, non-functional reqs | | |
| 3 | Design | Architecture diagram, ER schema, wireframes | | |
| 4 | Iteration 1 | Flask shell, home page, static pages | | |
| 5 | Iteration 2 | MySQL + signup/login | | |
| 6 | Iteration 3 | Crop form + model integration | | |
| 7 | Iteration 4 | Soil pages + lab search + appointment API | | |
| 8 | Iteration 5 | CSS polish, Lottie, scroll animations | | |
| 9 | ML ops | `train_crop_model.py`, documented accuracy | | |
| 10 | QA | Manual test pass (Chapter 4) | | |
| 11 | Documentation | Report, `FRONTEND.md`, demo script | | |
| 12 | Closure | Presentation / submission | | |

### 8.2 Weekly log (template)  

| Week | Dates | Goals | Achieved | Blockers |
|------|-------|-------|----------|----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

### 8.3 Sign-off  

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Student | | | |
| Project guide | | | |
| External examiner (if any) | | | |

---

*End of detailed report.*
