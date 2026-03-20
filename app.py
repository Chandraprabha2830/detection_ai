from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from utils.url_analyzer import analyze_url
from utils.ml_model import predict_url
from utils.report_generator import generate_report
from utils.email_alert import send_alert_email
from models.database import db, DetectionLog, User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

app.secret_key = 'ai_detection_secret_key_2025'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_detection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ─── RULE BASED FAKE URL DETECTION ─────────────────────────

def detect_fake_url(url):

    suspicious_keywords = [
        "login", "verify", "update", "banking",
        "secure", "account", "free", "bonus"
    ]

    suspicious_domains = [
        ".xyz", ".tk", ".ml", ".ga", ".cf"
    ]

    score = 0

    for word in suspicious_keywords:
        if word in url.lower():
            score += 1

    for domain in suspicious_domains:
        if domain in url.lower():
            score += 1

    if score >= 2:
        return "FAKE"
    else:
        return "GENUINE"


# ─── LOGIN REQUIRED ───────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── ADMIN REQUIRED ───────────────────────────────────────

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Admin access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── REGISTER ─────────────────────────────────────────────

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('login'))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ─── LOGIN ────────────────────────────────────────────────

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email'].lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin

            if user.is_admin:
                return redirect(url_for('admin_dashboard'))

            return redirect(url_for('index'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')


# ─── LOGOUT ───────────────────────────────────────────────

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# ─── HOME PAGE ────────────────────────────────────────────

@app.route('/')
@login_required
def index():

    return render_template('index.html')


# ─── URL CHECK ────────────────────────────────────────────

@app.route('/url-check', methods=['GET','POST'])
@login_required
def url_check():

    result = None

    if request.method == 'POST':

        url = request.form['url']

        features = analyze_url(url)

        prediction = predict_url(features)

        risk_score = prediction['risk_score']
        ml_label = prediction['label']
        reasons = prediction['reasons']

        rule_label = detect_fake_url(url)

        if ml_label == "FAKE" or rule_label == "FAKE":
            label = "FAKE"
        else:
            label = "GENUINE"

        log = DetectionLog(
            user_id=session['user_id'],
            input_type='url',
            input_data=url,
            result=label,
            risk_score=risk_score,
            details=str(reasons),
            timestamp=datetime.utcnow()
        )

        db.session.add(log)
        db.session.commit()

        # EMAIL ALERT
        if label == "FAKE":

            user = User.query.get(session['user_id'])

            print("USER EMAIL:", user.email)

            send_alert_email(user.email, url, risk_score)

            send_alert_email("prabhachanra2@gmail.com", url, risk_score)

        result = {
            'url': url,
            'label': label,
            'risk_score': risk_score,
            'reasons': reasons,
            'features': features
        }

    return render_template('url_check.html', result=result)


# ─── HISTORY ──────────────────────────────────────────────

@app.route('/history')
@login_required
def history():

    logs = DetectionLog.query.filter_by(user_id=session['user_id']) \
        .order_by(DetectionLog.timestamp.desc()).all()

    return render_template('history.html', logs=logs)


# ─── DOWNLOAD REPORT ──────────────────────────────────────

@app.route('/report/<int:log_id>')
@login_required
def download_report(log_id):

    log = DetectionLog.query.get_or_404(log_id)

    if log.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Access denied', 'danger')
        return redirect(url_for('history'))

    pdf_path = generate_report(log)

    from flask import send_file
    return send_file(pdf_path, as_attachment=True)


# ─── ADMIN DASHBOARD ──────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():

    total = DetectionLog.query.count()

    fake = DetectionLog.query.filter_by(result='FAKE').count()

    genuine = DetectionLog.query.filter_by(result='GENUINE').count()

    users = User.query.count()

    recent = DetectionLog.query.order_by(
        DetectionLog.timestamp.desc()
    ).limit(20).all()

    return render_template(
        'admin_dashboard.html',
        total=total,
        fake=fake,
        genuine=genuine,
        users=users,
        recent=recent
    )


# ─── ADMIN LOGS ───────────────────────────────────────────

@app.route('/admin/logs')
@admin_required
def admin_logs():

    logs = DetectionLog.query.order_by(
        DetectionLog.timestamp.desc()
    ).all()

    return render_template('admin_logs.html', logs=logs)


# ─── ADMIN USERS ──────────────────────────────────────────

@app.route('/admin/users')
@admin_required
def admin_users():

    users = User.query.all()

    return render_template('admin_users.html', users=users)


# ─── DELETE LOG ───────────────────────────────────────────

@app.route('/admin/delete-log/<int:log_id>', methods=['POST'])
@admin_required
def delete_log(log_id):

    log = DetectionLog.query.get_or_404(log_id)

    db.session.delete(log)

    db.session.commit()

    flash('Log deleted successfully', 'success')

    return redirect(url_for('admin_logs'))


# ─── RUN SERVER ───────────────────────────────────────────

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(email='prabhachanra2@gmail.com').first()

        if not admin:

            admin = User(
                username='admin',
                email='prabhachanra@gmail.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )

            db.session.add(admin)

            db.session.commit()

            print("Admin created")

    app.run(debug=True)