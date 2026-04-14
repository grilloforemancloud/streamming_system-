from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Aqui vamos buscar pelo NOME "teste"
    user = User.query.filter_by(nome='teste').first()
    
    # Se você usou "teste" no e-mail, use esta linha em vez da de cima:
    # user = User.query.filter_by(email='teste@teste.com').first()

    if user:
        user.is_admin = True
        db.session.commit()
        print(f"Sucesso! O usuário {user.nome} agora é ADMIN.")
    else:
        print("Usuário 'teste' não foi encontrado no banco.")

exit()