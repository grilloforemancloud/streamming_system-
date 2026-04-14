from app import db  # Esta substitui a antiga com ponto
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WebRTCChannel(db.Model):
    __tablename__ = 'webrtc_channels'
    id = db.Column(db.Integer, primary_key=True)
    nome_canal = db.Column(db.String(100), nullable=False)
    url_iframe = db.Column(db.String(255), nullable=False)
    
    cor_fundo = db.Column(db.String(20), default="#ffffff")
    cor_texto = db.Column(db.String(20), default="#000000")
    fonte = db.Column(db.String(50), default="Arial")

    def __repr__(self):
        return f"<Channel {self.nome_canal}>"