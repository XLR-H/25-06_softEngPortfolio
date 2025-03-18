from werkzeug.security import generate_password_hash

senha = 'admin'
senha_hash = generate_password_hash(senha)
print(senha_hash)