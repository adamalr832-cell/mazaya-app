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
    status = db.Column(db.String(50), default='قيد الانتظار ⏳')

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
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(135deg, rgba(15, 32, 39, 0.85), rgba(44, 83, 100, 0.85)), 
                    url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 15px;
    }
    .card-custom {
        border: none;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        overflow: hidden;
    }
    .hero-container {
        position: relative;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .hero-img {
        width: 100%;
        height: 170px;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .hero-container:hover .hero-img {
        transform: scale(1.03);
    }
    .hero-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
        padding: 15px 20px;
        color: white;
    }
    .form-label {
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .input-group-text {
        background-color: #f1f8f5;
        border: 1px solid #ced4da;
        border-radius: 0 12px 12px 0 !important;
        color: #2e7d32;
        font-size: 16px;
    }
    .form-control, .form-select {
        border-radius: 12px 0 0 12px;
        padding: 12px 15px;
        border: 1px solid #ced4da;
        background-color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .form-control:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 0.25rem rgba(46, 125, 50, 0.2);
        background-color: #fff;
    }
    /* تعديل الحقول التي ليس فيها input-group */
    .single-input {
        border-radius: 12px !important;
    }
    .btn-primary-custom {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        border: none;
        border-radius: 12px;
        padding: 14px;
        font-weight: 700;
        font-size: 16px;
        color: #fff;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
    }
    .btn-primary-custom:hover {
        background: linear-gradient(135deg, #1b5e20 0%, #0d3811 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.6);
        color: #fff;
    }
    .badge-pending {
        background-color: #fff3cd;
        color: #856404;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
    }
    .badge-collected {
        background-color: #d4edda;
        color: #155724;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
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
        <title>شركة مزايا للتدوير | منصة المدارس</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-8 col-lg-7">
                    <div class="card card-custom p-4 p-md-5">
                        
                        <!-- قسم الصورة التعبيرية الحديثة -->
                        <div class="hero-container">
                            <img src="https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?q=80&w=900&auto=format&fit=crop" class="hero-img" alt="إعادة التدوير والبيئة">
                            <div class="hero-overlay">
                                <h5 class="fw-bold mb-0 text-white"><i class="fa-solid fa-recycle text-success me-2"></i> شركة مزايا للتدوير المستدام</h5>
                                <p class="small mb-0 text-light opacity-75">نحو بيئة مدرسية خضراء ونظيفة</p>
                            </div>
                        </div>
                        
                        <div class="text-center mb-4">
                            <h3 class="fw-bold text-success mb-1">تسجيل بيانات الحاويات وإعادة التدوير</h3>
                            <p class="text-muted small">يرجى تعبئة النموذج أدناه بدقة ليتم إرسال الطلب لفريق العمل الميداني</p>
                        </div>

                        <form action="/submit" method="POST">
                            <div class="mb-3">
                                <label class="form-label"><i class="fa-solid fa-school text-success me-1"></i> اسم المدرسة</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="fa-solid fa-building-columns"></i></span>
                                    <input type="text" class="form-control" name="school_name" placeholder="أدخل اسم المدرسة هنا..." required>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label"><i class="fa-solid fa-map-location-dot text-success me-1"></i> موقع المدرسة (تحديد تلقائي)</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="fa-solid fa-location-crosshairs"></i></span>
                                    <input type="text" class="form-control" id="school_location" name="school_location" placeholder="اضغط على زر التحديد في الجانب..." required readonly>
                                    <button type="button" class="btn btn-outline-success fw-bold px-3" style="border-radius: 0 12px 12px 0;" onclick="getLocation()">
                                        <i class="fa-solid fa-location-dot me-1"></i> حدد موقعي
                                    </button>
                                </div>
                                <div id="location-status" class="form-text text-success mt-1 fw-bold" style="font-size: 13px;"></div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label"><i class="fa-solid fa-percent text-success me-1"></i> نسبة امتلاء الحاوية / التدوير</label>
                                    <div class="input-group">
                                        <span class="input-group-text"><i class="fa-solid fa-chart-pie"></i></span>
                                        <input type="text" class="form-control" name="plastic_percentage" placeholder="مثال: 95%" required>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label"><i class="fa-solid fa-phone text-success me-1"></i> رقم هاتف المسؤول</label>
                                    <div class="input-group">
                                        <span class="input-group-text"><i class="fa-solid fa-mobile-screen-button"></i></span>
                                        <input type="text" class="form-control" name="phone" placeholder="أدخل رقم الهاتف..." required>
                                    </div>
                                </div>
                            </div>

                            <div class="mb-4">
                                <label class="form-label"><i class="fa-solid fa-note-sticky text-success me-1"></i> ملاحظات إضافية (اختياري)</label>
                                <textarea class="form-control single-input" name="notes" rows="3" placeholder="أي تفاصيل حول نوع الحاويات أو أوقات الاستلام المناسبة..."></textarea>
                            </div>

                            <button type="submit" class="btn btn-primary-custom w-100">
                                <i class="fa-solid fa-paper-plane me-2"></i> إرسال الطلب للإدارة فوراً
                            </button>
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

                status.textContent = 'جاري تحديد إحداثيات موقع المدرسة بدقة...';
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
        <title>تم إرسال الطلب بنجاح</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container text-center">
            <div class="card card-custom p-5 mx-auto" style="max-width: 520px;">
                <div class="mb-3 text-success" style="font-size: 70px;"><i class="fa-solid fa-circle-check"></i></div>
                <h3 class="fw-bold text-dark mb-3">تم إرسال بياناتك بنجاح!</h3>
                <p class="text-muted mb-4">شكراً لجهودكم البيئية. تم تسجيل بيانات الحاويات وإرسالها مباشرة إلى لوحة تحكم الإدارة لمتابعتها وجمعها.</p>
                <a href="/" class="btn btn-primary-custom w-100">
                    <i class="fa-solid fa-arrow-right me-2"></i> إرسال طلب أو مدرسة أخرى ♻️
                </a>
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
                            <div class="text-success mb-2" style="font-size: 40px;"><i class="fa-solid fa-shield-halved"></i></div>
                            <h3 class="fw-bold text-dark">لوحة التحكم</h3>
                            <p class="text-muted small">تسجيل دخول مسؤولي شركة مزايا</p>
                        </div>
                        {{% if error %}}
                            <div class="alert alert-danger text-center py-2 mb-3" style="font-size: 14px; border-radius: 10px;">{{{{ error }}}}</div>
                        {{% endif %}}
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">اسم المستخدم</label>
                                <input type="text" class="form-control single-input" name="username" required>
                            </div>
                            <div class="mb-4">
                                <label class="form-label">كلمة المرور</label>
                                <input type="password" class="form-control single-input" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary-custom w-100">تسجيل الدخول</button>
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
        location_link = f"<a href='{r.school_location}' target='_blank' class='btn btn-sm btn-outline-success fw-bold'><i class='fa-solid fa-map me-1'></i> الخريطة</a>" if r.school_location.startswith('http') else r.school_location
        
        if r.status == "تم الجمع ✅":
            status_badge = "<span class='badge-collected'>تم الجمع ✅</span>"
            action_btn = f"<a href='/toggle_status/{r.id}' class='btn btn-sm btn-outline-warning fw-bold'><i class='fa-solid fa-rotate-left me-1'></i> إلغاء التأكيد</a>"
        else:
            status_badge = "<span class='badge-pending'>قيد الانتظار ⏳</span>"
            action_btn = f"<a href='/toggle_status/{r.id}' class='btn btn-sm btn-success fw-bold'><i class='fa-solid fa-check me-1'></i> تأكيد الجمع ✔️</a>"

        rows_html += f"<tr><td>{r.id}</td><td class='fw-bold text-dark'>{r.school_name}</td><td>{location_link}</td><td><span class='badge bg-light text-success border fw-bold px-2 py-1'>{r.plastic_percentage}</span></td><td>{r.phone}</td><td>{r.notes or '-'}</td><td>{status_badge}</td><td>{action_btn}</td></tr>"

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
    <body style="display: block; background: #f4f7f6; padding: 0;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 py-3 shadow-sm">
            <div class="container-fluid">
                <a class="navbar-brand fw-bold" href="#"><i class="fa-solid fa-recycle text-success me-2"></i> لوحة تحكم شركة مزايا (إدارة الحاويات)</a>
                <a href="/logout" class="btn btn-outline-light btn-sm fw-bold"><i class="fa-solid fa-right-from-bracket me-1"></i> تسجيل الخروج</a>
            </div>
        </nav>
        <div class="container my-5" style="max-width: 1350px;">
            <div class="card card-custom p-4 shadow-sm" style="background: #ffffff;">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h4 class="fw-bold text-secondary mb-0"><i class="fa-solid fa-list-check text-success me-2"></i> إدارة طلبات وحاويات المدارس الواردة</h4>
                </div>
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
