from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'mazaya_secret_key_2026'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazaya.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CompanyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(150), nullable=False)
    school_location = db.Column(db.String(250), nullable=False)
    plastic_percentage = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

COMMON_STYLE = '''
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(135deg, #f0f7f4 0%, #d8e8e1 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .card-custom {
        border: none;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        background: #ffffff;
        overflow: hidden;
    }
    .btn-primary-custom {
        background-color: #2e7d32;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
        color: #fff;
        transition: all 0.3s ease;
    }
    .btn-primary-custom:hover {
        background-color: #1b5e20;
        color: #fff;
    }
    .form-control, .form-select {
        border-radius: 8px;
        padding: 10px 15px;
        border: 1px solid #ced4da;
    }
    .form-control:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 0.2rem rgba(46, 125, 50, 0.25);
    }
</style>
'''

@app.route('/')
def index():
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>شركة مزايا للتدوير</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-6 col-lg-5">
                    <div class="card card-custom p-4 p-md-5">
                        <div class="text-center mb-4">
                            <h2 class="fw-bold text-success">♻️ شركة مزايا للتدوير</h2>
                            <p class="text-muted small">نظام استقبال بيانات وإحصاءات إعادة تدوير الورق للمدارس</p>
                        </div>
                        <form action="/submit" method="POST">
                            <div class="mb-3">
                                <label class="form-label fw-600">اسم المدرسة</label>
                                <input type="text" class="form-control" name="school_name" placeholder="أدخل اسم المدرسة هنا" required>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label fw-600">موقع المدرسة (تحديد تلقائي)</label>
                                <div class="input-group">
                                    <input type="text" class="form-control" id="school_location" name="school_location" placeholder="اضغط على الزر لتحديد موقعك..." required readonly>
                                    <button type="button" class="btn btn-outline-success" onclick="getLocation()">📍 تحديد الموقع</button>
                                </div>
                                <div id="location-status" class="form-text text-success mt-1" style="font-size: 12px;"></div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-600">نسبة استلام العبوية (%100-0)</label>
                                <input type="text" class="form-control" name="plastic_percentage" placeholder="مثال: 95%" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-600">رقم هاتف المسؤول</label>
                                <input type="text" class="form-control" name="phone" placeholder="أدخل رقم الهاتف" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label fw-600">ملاحظات إضافية (اختياري)</label>
                                <textarea class="form-control" name="notes" rows="3" placeholder="أي تفاصيل أو ملاحظات إضافية..."></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary-custom w-100">إرسال الحالة</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function getLocation() {{
                const status = document.getElementById('location-status');
                const locationInput = document.getElementById('school_location');

                if (!navigator.geolocation) {{
                    status.textContent = 'متصفحك لا يدعم تحديد الموقع الجغرافي';
                    status.className = 'form-text text-danger mt-1';
                    return;
                }}

                status.textContent = 'جاري تحديد الموقع...';
                status.className = 'form-text text-warning mt-1';

                navigator.geolocation.getCurrentPosition((position) => {{
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    // وضع إحداثيات خرائط جوجل مباشرة في الحقل
                    locationInput.value = `https://maps.google.com/?q=${{latitude}},${{longitude}}`;
                    status.textContent = 'تم تحديد الموقع بنجاح! ✅';
                    status.className = 'form-text text-success mt-1';
                }}, () => {{
                    status.textContent = 'فشل تحديد الموقع. يرجى السماح للمتصفح بالوصول للموقع.';
                    status.className = 'form-text text-danger mt-1';
                }});
            }}
        </script>
    </body>
    </html>
    ''')

@app.route('/submit', methods=['POST'])
def submit():
    school_name = request.form.get('school_name')
    school_location = request.form.get('school_location')
    plastic_percentage = request.form.get('plastic_percentage')
    phone = request.form.get('phone')
    notes = request.form.get('notes', '')

    new_request = CompanyRequest(
        school_name=school_name,
        school_location=school_location,
        plastic_percentage=plastic_percentage,
        phone=phone,
        notes=notes
    )
    db.session.add(new_request)
    db.session.commit()
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تم الإرسال بنجاح</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container text-center">
            <div class="card card-custom p-5 mx-auto" style="max-width: 500px;">
                <div class="mb-3 text-success" style="font-size: 50px;">✅</div>
                <h3 class="fw-bold text-dark mb-3">تم إرسال طلب شركة مزايا بنجاح</h3>
                <p class="text-muted mb-4">شكراً لك، تم تسجيل بيانات المدرسة مع الموقع الجغرافي بنجاح في النظام.</p>
                <a href="/" class="btn btn-primary-custom">إرسال طلب جديد</a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'Khamis' and password == 'mazaya2026@':
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة'
            
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل دخول المشرف</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-md-5 col-lg-4">
                    <div class="card card-custom p-4 p-md-5">
                        <div class="text-center mb-4">
                            <h3 class="fw-bold text-dark">🔐 لوحة التحكم</h3>
                            <p class="text-muted small">تسجيل دخول المسؤولين</p>
                        </div>
                        {{% if error %}}
                            <div class="alert alert-danger text-small text-center py-2 mb-3" style="font-size: 14px; border-radius: 8px;">{{{{ error }}}}</div>
                        {{% endif %}}
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label fw-600">اسم المستخدم</label>
                                <input type="text" class="form-control" name="username" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label fw-600">كلمة المرور</label>
                                <input type="password" class="form-control" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary-custom w-100">دخول للنظام</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', error=error)

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('login'))
    
    requests_list = CompanyRequest.query.all()
    
    rows_html = ""
    for r in requests_list:
        # جعل الموقع رابطاً قابلاً للنقر لفتح الخريطة مباشرة
        location_link = f"<a href='{r.school_location}' target='_blank' class='btn btn-sm btn-outline-primary'>عرض على الخريطة 🗺️</a>" if r.school_location.startswith('http') else r.school_location
        rows_html += f"<tr><td>{r.id}</td><td class='fw-bold'>{r.school_name}</td><td>{location_link}</td><td><span class='badge bg-success'>{r.plastic_percentage}</span></td><td>{r.phone}</td><td>{r.notes or '-'}</td></tr>"

    if not rows_html:
        rows_html = "<tr><td colspan='6' class='text-center text-muted py-4'>لا توجد طلبات مسجلة حتى الآن</td></tr>"

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة التحكم - شركة مزايا</title>
        {COMMON_STYLE}
    </head>
    <body style="display: block; background: #f8f9fa;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 py-3 shadow-sm">
            <div class="container-fluid">
                <a class="navbar-brand fw-bold" href="#">♻️ لوحة تحكم شركة مزايا</a>
                <a href="/logout" class="btn btn-outline-light btn-sm">تسجيل الخروج</a>
            </div>
        </nav>
        <div class="container my-5">
            <div class="card card-custom p-4">
                <h4 class="mb-4 fw-bold text-secondary">طلبات المدارس الواردة (إعادة تدوير الورق)</h4>
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>#</th>
                                <th>اسم المدرسة</th>
                                <th>موقع المدرسة</th>
                                <th>نسبة الورق</th>
                                <th>رقم الهاتف</th>
                                <th>ملاحظات</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
