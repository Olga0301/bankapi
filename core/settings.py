from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY ='ndfu8c75873498cyng8r5tc88r9r84n'
EXPIRE_JWT_TOKEN = 10
TOKEN_TYPE = 'Bearer'
ALGORITHM = 'HS256'
