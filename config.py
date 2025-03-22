from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/softmarket"  # <postgres> = usuario e <123456> exemplo de senha!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
