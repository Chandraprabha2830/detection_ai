# AI-Driven Clone Website & Fake App Detection Engine
**MCA Project | Chandraprabha M – 927624MCA005**  
*Under the guidance of Mrs. S. Kayathri, MCA, B.Ed., PGDAN, (Ph.D)*

---

## Project Overview

A full-stack Flask web application that uses **Machine Learning** (Scikit-learn Random Forest) to detect:
- **Phishing / Clone Websites** via URL feature analysis
- **Fake Android Apps** via APK permission and API behavior analysis

### Key Features
- User registration & login with session management
- URL phishing detection with 15 extracted features
- APK scanning for dangerous permissions and suspicious APIs
- Real-time risk score with visual progress bar
- Email alert notification when a threat is detected
- PDF security report generation per detection
- Admin dashboard with statistics and log management
- REST API endpoint for URL checking

---

## Project Structure

```
ai_detection_project/
│
├── app.py                  ← Main Flask application
├── train_model.py          ← Train & save ML models
├── schema.sql              ← MySQL database schema
├── requirements.txt        ← Python dependencies
│
├── models/
│   ├── database.py         ← SQLAlchemy models (User, DetectionLog)
│   ├── url_model.pkl       ← (generated after training)
│   ├── url_scaler.pkl      ← (generated after training)
│   ├── apk_model.pkl       ← (generated after training)
│   └── apk_scaler.pkl      ← (generated after training)
│
├── utils/
│   ├── url_analyzer.py     ← Extract 15 features from URL
│   ├── apk_analyzer.py     ← Extract features from APK file
│   ├── ml_model.py         ← ML prediction logic
│   ├── report_generator.py ← PDF report generation (ReportLab)
│   └── email_alert.py      ← SMTP email alert sender
│
├── templates/
│   ├── base.html           ← Base layout with navbar
│   ├── login.html          ← Login page
│   ├── register.html       ← Registration page
│   ├── index.html          ← Home / dashboard
│   ├── url_check.html      ← URL scanner page
│   ├── apk_check.html      ← APK scanner page
│   ├── history.html        ← User scan history
│   ├── admin_dashboard.html
│   ├── admin_logs.html
│   └── admin_users.html
│
└── static/
    ├── css/style.css       ← Custom dark theme CSS
    ├── js/main.js          ← Frontend JavaScript
    └── uploads/            ← APK uploads folder
```

---

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database
```bash
mysql -u root -p < schema.sql
```

### 3. Configure Environment
Edit `app.py` line for DB URI:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/ai_detection_db'
```

For email alerts, set environment variables:
```bash
export SMTP_USER="your_email@gmail.com"
export SMTP_PASS="your_app_password"
```

### 4. Train the ML Models
```bash
python train_model.py
```

### 5. Run the Application
```bash
python app.py
```

Open browser: **http://localhost:5000**

---

## Default Admin Login
- **Email:** admin@aidetection.com
- **Password:** admin123  
> ⚠️ Change this password immediately after first login!

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Backend | Python 3.x, Flask 3.0 |
| Database | MySQL 8.0, SQLAlchemy ORM |
| Machine Learning | Scikit-learn (Random Forest), NumPy |
| Reports | ReportLab (PDF generation) |
| Email | SMTP via Python smtplib |

---

## ML Features Used

### URL Detection (15 features)
1. URL length
2. Special character count
3. Dot count in domain
4. Hyphen count
5. HTTPS presence
6. IP address as domain
7. Subdomain count
8. Suspicious keyword count
9. Suspicious TLD detection
10. Path depth
11. Query string presence
12. URL entropy (randomness)
13. Encoded characters
14. Redirect parameter presence
15. Domain length

### APK Detection (9 features)
1. File size
2. Valid ZIP structure
3. Manifest presence
4. DEX file presence
5. Dangerous permission count
6. Total permission count
7. Suspicious API call count
8. Minimum SDK version
9. Target SDK version

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/check-url` | JSON URL check |
| GET | `/api/stats` | Detection statistics |

**Example API call:**
```bash
curl -X POST http://localhost:5000/api/check-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://login-paypal-verify.xyz/account"}'
```

---

*AI-Driven Clone Website & Fake App Detection Engine | MCA 2024-25*
