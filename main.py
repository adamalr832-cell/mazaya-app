from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mazaya_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazaya.db'
db = SQLAlchemy(app)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(100), nullable=False)
    fill_percentage = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', password_hash=generate_password_hash('Mazaya2026!'))
        db.session.add(admin_user)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        school = request.form.get('school_name')
        fill = int(request.form.get('fill_percentage'))
        phone = request.form.get('phone_number')
        notes = request.form.get('notes')
        new_sub = Submission(school_name=school, fill_percentage=fill, phone_number=phone, notes=notes)
        db.session.add(new_sub)
        db.session.commit()
        return "<h1 style='color: #15803d; text-align: center; margin-top: 50px;'>تم إرسال طلب شركة مزايا بنجاح!</h1>"
    return '''
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>مزايا - بوابة المدارس</title></head>
    <body style="font-family: Arial, sans-serif; background-color: #f0fdf4; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: #15803d; text-align: center;">شركة مزايا للتدوير</h1>
            <form method="POST">
                <label>اسم المدرسة:</label><br><input type="text" name="school_name" required style="width: 100%; padding: 10px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 4px;"><br>
                <label>نسبة امتلاء الحاوية (0-100%):</label><br><input type="number" name="fill_percentage" min="0" max="100" required style="width: 100%; padding: 10px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 4px;"><br>
                <label>رقم هاتف المسؤول:</label><br><input type="text" name="phone_number" required style="width: 100%; padding: 10px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 4px;"><br>
                <label>ملاحظات إضافية:</label><br><textarea name="notes" style="width: 100%; padding: 10px; margin: 10px 0 20px 0; border: 1px solid #ccc; border-radius: 4px;"></textarea><br>
                <button type="submit" style="width: 100%; background-color: #15803d; color: white; padding: 12px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">إرسال الحالة</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return redirect(url_for('admin', token='logged_in'))
        return "خطأ في اسم المستخدم أو كلمة المرور"
    return '''
    <div style="max-width: 300px; margin: 100px auto; padding: 20px; border: 1px solid #ccc;">
        <h2>تسجيل دخول الإدارة</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" required style="width: 100%; margin-bottom: 10px;"><br>
            <input type="password" name="password" placeholder="كلمة المرور" required style="width: 100%; margin-bottom: 10px;"><br>
            <button type="submit" style="width: 100%; background: #15803d; color: white; border: none; padding: 10px;">دخول</button>
        </form>
    </div>
    '''

@app.route('/admin')
def admin():
    token = request.args.get('token')
    if token != 'logged_in':
        return redirect(url_for('login'))
    submissions = Submission.query.order_by(Submission.timestamp.desc()).all()
    html = '''
    <div style="padding: 20px;" dir="rtl">
        <h1 style="color: #15803d;">لوحة تحكم شركة مزايا</h1>
        <table border="1" cellpadding="10" style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #e6f4ea;">
                <th>المدرسة</th><th>نسبة الامتلاء</th><th>رقم الهاتف</th><th>الحالة</th><th>التاريخ</th>
            </tr>
    '''
    for s in submissions:
        bg_color = '#fee2e2' if s.fill_percentage >= 80 else '#ffffff'
        html += f'''
        <tr style="background-color: {bg_color};">
            <td>{s.school_name}</td>
            <td>{s.fill_percentage}%</td>
            <td>{s.phone_number}</td>
            <td>{s.status}</td>
            <td>{s.timestamp.strftime('%Y-%m-%d %H:%M')}</td>
        </tr>
        '''
    html += '</table></div>'
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
