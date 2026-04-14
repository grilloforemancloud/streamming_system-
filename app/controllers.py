from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, WebRTCChannel, db  # Importação absoluta (sem ponto)

webrtc_bp = Blueprint('webrtc', __name__)

@webrtc_bp.route('/')
def index():
    return redirect(url_for('webrtc.login'))

@webrtc_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            session['user_id'] = user.id
            return redirect(url_for('webrtc.dashboard'))
        flash('E-mail ou senha incorretos', 'danger')
    return render_template('login.html')

@webrtc_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado', 'danger')
        else:
            novo = User(nome=nome, email=email)
            novo.set_password(senha)
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for('webrtc.login'))
    return render_template('register.html')

@webrtc_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('webrtc.login'))
    user = User.query.get(session['user_id'])
    canais = WebRTCChannel.query.all()
    return render_template('dashboard.html', user=user, canais=canais)

@webrtc_bp.route('/admin/add', methods=['POST'])
def add_canal():
    user = User.query.get(session.get('user_id'))
    if not user or not user.is_admin:
        return "Acesso negado", 403
    
    novo = WebRTCChannel(
        nome_canal=request.form.get('nome_canal'),
        url_iframe=request.form.get('url_iframe'),
        cor_fundo=request.form.get('cor_fundo'),
        fonte=request.form.get('fonte')
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('webrtc.dashboard'))

@webrtc_bp.route('/canal/<int:id>')
def ver_canal(id):
    if 'user_id' not in session:
        return redirect(url_for('webrtc.login'))
    canal = WebRTCChannel.query.get_or_404(id)
    return render_template('viewer.html', canal=canal)

@webrtc_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('webrtc.login'))