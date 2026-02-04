import bcrypt 

class Hash():
    def bcrypt(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
