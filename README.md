# KrushiSarathi 🌾

An AI-powered smart agriculture web platform designed to help farmers make data-driven decisions through crop recommendation, soil testing services, and financial awareness resources.

---

## Overview

KrushiSarathi is a full-stack web application built to bridge the gap between technology and agriculture. The platform assists farmers by providing intelligent crop recommendations based on soil and environmental parameters, enabling soil testing appointment booking, and offering financial awareness modules including loans, schemes, and savings information.

## Features

- 🌱 AI-based crop recommendation using Machine Learning
- 🧪 Soil testing lab appointment booking system
- 🔐 Secure user authentication and session management
- 💰 Financial awareness modules for farmers
- 📊 Database-driven appointment and user management
- 🌐 Responsive web interface

---

## Tech Stack

### Backend
- Python
- Flask
- MySQL

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Random Forest Classifier

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2

---

## Project Architecture

```bash
KrushiSarathi/
│
├── app.py
├── train_crop_model.py
├── init_database.py
├── requirements.txt
├── Crop_data.csv
├── crop_recommendation_model.pkl
├── setup_mysql.sql
├── seed_mysql.sql
│
├── templates/
├── static/
├── screenshots/
```

---

## Core Modules

### AI Crop Recommendation
Predicts suitable crops based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall

### Soil Testing Module
- Find nearby soil testing labs
- Book appointments
- Manage schedules

### Financial Assistance Module
- Agricultural loan awareness
- Government schemes
- Savings guidance

### Authentication
- User signup/login
- Password hashing
- Session management

---

## Installation & Setup

### Clone Repository
```bash
git clone https://github.com/pratik26x/KrushiSarathi.git
cd KrushiSarathi
```

### Create Virtual Environment
```bash
python -m venv .venv
```

### Activate Environment

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Database
```sql
CREATE DATABASE farmers_db;
```

Run:
- setup_mysql.sql
- seed_mysql.sql

### Start Application
```bash
python app.py
```

App runs at:
```bash
http://127.0.0.1:5000
```

---

## Future Enhancements

- Weather API integration
- AI chatbot for farmers
- Multilingual support
- Mobile application
- Admin dashboard
- Real-time agricultural insights

---

## Author

**Pratik Rakhonde**

⭐ If you like this project, consider starring the repository.