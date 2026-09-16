from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'mazaya_secret_key_2026'

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazaya.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# جدول تخزين طلبات الشركات والمدارس
class CompanyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(150), nullable=False)
    plastic_percentage = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

# إنشاء قاعدة البيانات وتجهيز حساب المسؤول تلقائياً
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    school_name = request.form.get('school_name')
    plastic_percentage = request.form.get('plastic_percentage')
    phone = request.form.get('phone')
    notes = request.form.get('notes', '')

    new_request = CompanyRequest(
        school_name=school_name,
        plastic_percentage=plastic_percentage,
        phone=phone,
        notes=notes
    )
    db.session.add(new_request)
    db.session.commit()
    
    return "تم إرسال طلب شركة مزايا بنجاح"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # بيانات الدخول الجديدة المعتمدة
        if username == 'Khamis' and password == 'mazaya2026@':
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('خطأ في اسم المستخدم أو كلمة المرور')
            
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('login'))
    
    requests_list = CompanyRequest.query.all()
    return render_template('admin.html', requests=requests_list)

@app.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
