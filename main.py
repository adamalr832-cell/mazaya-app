from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'mazaya_secret_key_2026'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mazaya.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CompanyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(150), nullable=False)
    school_location = db.Column(db.String(250), nullable=False)
    plastic_percentage = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='قيد الانتظار ⏳') # حقل جديد لحالة الجمع

with app.app_context():
    db.create_all()
    if CompanyRequest.query.count() == 0:
        sample = CompanyRequest(
            school_name="مدرسة سهيل بن عمرو (تجريبي)",
            school_location="https://maps.google.com/?q=23.5880,58.3829",
            plastic_percentage="95%",
            phone="96891234567",
            notes="هذا طلب تجريبي للتأكد من عمل النظام",
            status="قيد الانتظار ⏳"
        )
        db.session.add(sample)
        db.session.commit()

COMMON_STYLE = '''
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(rgba(15, 32, 39, 0.75), rgba(44, 83, 100, 0.75)), 
                    url('https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 0;
    }
    .card-custom {
        border: none;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(10px);
        overflow: hidden;
    }
    .hero-img {
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .btn-primary-custom {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-weight: 700;
        color: #fff;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
    }
    .btn-primary-custom:hover {
        background: linear-gradient(135deg, #1b5e20 0%, #0d3811 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.6);
        color: #fff;
    }
    .form-control, .form-select {
        border-radius: 10px;
        padding: 12px 15px;
        border: 1px solid #ced4da;
        background-color: rgba(255, 255, 255, 0.9);
    }
    .form-control:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 0.25rem rgba(46, 125, 50, 0.25);
        background-color: #fff;
    }
    .badge-pending {
        background-color: #fff3cd;
        color: #856404;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 20px;
    }
    .badge-collected {
        background-color: #d4edda;
        color: #155724;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 20px;
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>شركة مزايا للتدوير</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-7 col-lg-6">
                    <div class="card card-custom p-4 p-md-5">
                        <!-- صورة تعبيرية فخمة لإعادة التدوير -->
                        <img src="https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=800&auto=format&fit=crop" class="hero-img" alt="إعادة تدوير الورق والبيئة">
                        
                        <div class="text-center mb-4">
                            <h2 class="fw-bold text-success">شركة مزايا للتدوير</h2>
                            <p class="text-muted small">منصة استقبال بيانات وإحصاءات إعادة تدوير الورق للمدارس</p>
                        </div>
                        <form action="/submit" method="POST">
                            <div class="mb-3">
                                <label class="form-label fw-bold">اسم المدرسة</label>
                                <input type="text" class="form-control" name="school_name" placeholder="أدخل اسم المدرسة هنا" required>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label fw-bold">موقع المدرسة (تحديد تلقائي)</label>
                                <div class="input-group">
                                    <input type="text" class="form-control" id="school_location" name="school_location" placeholder="اضغط على زر التحديد..." required readonly>
                                    <button type="button" class="btn btn-outline-success px-3 fw-bold" onclick="getLocation()">📍 حدد موقعي</button>
                                </div>
                                <div id="location-status" class="form-text text-success mt-1 fw-bold" style="font-size: 13px;"></div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-bold">نسبة استلام العبوية أو تدوير الورق (0 - 100%)</label>
                                <input type="text" class="form-control" name="plastic_percentage" placeholder="مثال: 95%" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label fw-bold">رقم هاتف المسؤول</label>
                                <input type="text" class="form-control" name="phone" placeholder="أدخل رقم الهاتف" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label fw-bold">ملاحظات إضافية (اختياري)</label>
                                <textarea class="form-control" name="notes" rows="3" placeholder="أي تفاصيل حول الحاويات أو الملاحظات..."></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary-custom w-100">إرسال الطلب للإدارة 🚀</button>
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

                status.textContent = 'جاري تحديد الموقع بدقة...';
                status.className = 'form-text text-warning mt-1';

                navigator.geolocation.getCurrentPosition((position) => {{
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
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
        notes=notes,
        status="قيد الانتظار ⏳"
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
                <div class="mb-3 text-success" style="font-size: 60px;">🎉</div>
                <h3 class="fw-bold text-dark mb-3">تم إرسال طلبك بنجاح!</h3>
                <p class="text-muted mb-4">شكراً لك، تم حفظ بيانات المدرسة والحاويات وموقعها وإرسالها مباشرة للإدارة.</p>
                <a href="/" class="btn btn-primary-custom w-100">إرسال طلب جديد ♻️</a>
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
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-5 col-lg-4">
                    <div class="card card-custom p-4 p-md-5">
                        <div class="text-center mb-4">
                            <h3 class="fw-bold text-dark">🔐 لوحة التحكم</h3>
                            <p class="text-muted small">تسجيل دخول المسؤولين</p>
                        </div>
                        {{% if error %}}
                            <div class="alert alert-danger text-center py-2 mb-3" style="font-size: 14px; border-radius: 10px;">{{{{ error }}}}</div>
                        {{% endif %}}
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label fw-bold">اسم المستخدم</label>
                                <input type="text" class="form-control" name="username" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label fw-bold">كلمة المرور</label>
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
        location_link = f"<a href='{r.school_location}' target='_blank' class='btn btn-sm btn-outline-success fw-bold'>عرض على الخريطة 🗺️</a>" if r.school_location.startswith('http') else r.school_location
        
        # تصميم الحالة مع زر لتحديثها إلى "تم الجمع ✅"
        if r.status == "تم الجمع ✅":
            status_badge = "<span class='badge-collected'>تم الجمع ✅</span>"
            action_btn = f"<a href='/toggle_status/{r.id}' class='btn btn-sm btn-outline-warning'>إرجاع قيد الانتظار ⏳</a>"
        else:
            status_badge = "<span class='badge-pending'>قيد الانتظار ⏳</span>"
            action_btn = f"<a href='/toggle_status/{r.id}' class='btn btn-sm btn-success fw-bold'>تأكيد الجمع (تم الجمع) ✔️</a>"

        rows_html += f"<tr><td>{r.id}</td><td class='fw-bold'>{r.school_name}</td><td>{location_link}</td><td><span class='badge bg-light text-dark border'>{r.plastic_percentage}</span></td><td>{r.phone}</td><td>{r.notes or '-'}</td><td>{status_badge}</td><td>{action_btn}</td></tr>"

    if not rows_html:
        rows_html = "<tr><td colspan='8' class='text-center text-muted py-4'>لا توجد طلبات مسجلة حتى الآن</td></tr>"

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة التحكم - شركة مزايا</title>
        {COMMON_STYLE}
    </head>
    <body style="display: block; background: #f8f9fa; padding: 0;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 py-3 shadow-sm">
            <div class="container-fluid">
                <a class="navbar-brand fw-bold" href="#">♻️ لوحة تحكم شركة مزايا (إدارة الحاويات)</a>
                <a href="/logout" class="btn btn-outline-light btn-sm">تسجيل الخروج</a>
            </div>
        </nav>
        <div class="container my-5" style="max-width: 1300px;">
            <div class="card card-custom p-4 shadow-sm" style="background: #ffffff;">
                <h4 class="mb-4 fw-bold text-secondary">إدارة طلبات وحاويات المدارس الواردة</h4>
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-light">
                            <tr>
                                <th>#</th>
                                <th>اسم المدرسة</th>
                                <th>موقع المدرسة</th>
                                <th>النسبة</th>
                                <th>الهاتف</th>
                                <th>ملاحظات</th>
                                <th>الحالة</th>
                                <th>إجراءات الإدارة</th>
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

@app.route('/toggle_status/<int:req_id>')
def toggle_status(req_id):
    if not session.get('admin_logged'):
        return redirect(url_for('login'))
    
    req_item = CompanyRequest.query.get_or_404(req_id)
    if req_item.status == "تم الجمع ✅":
        req_item.status = "قيد الانتظار ⏳"
    else:
        req_item.status = "تم الجمع ✅"
    
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin_logged', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
