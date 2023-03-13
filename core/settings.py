from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
