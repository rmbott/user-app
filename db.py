import os
from dotenv import load_dotenv
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column   
from werkzeug.security import generate_password_hash
load_dotenv()

user = os.getenv("NUSER")
pw = os.getenv("PW")
Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80))
    full_name: Mapped[Optional[str]] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    disabled: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.full_name!r})"
    
    def __init__(self, username:str, password:str, full_name:str, email:str, disabled:bool) -> None:
        self.username = username
        self.hashed_password = generate_password_hash(password)
        self.full_name = full_name
        self.email = email
        self.disabled = disabled

    def getAttributes(self) -> dict:
        return {self.username: {'username': self.username, 'full_name': self.full_name, 'email': self.email, 'hashed_password': self.hashed_password, 'disabled': self.disabled}}


engine = create_engine(f'postgresql://{user}:{pw}@localhost/pcdb')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create a test user as a proof of concept for database permissions.
# Refactor to user CRUD later.
# pword = "password123"
# print(generate_password_hash(pword))
# user = User('test_user', pword, 'Carl Doe', 'carl@aol.com', False)
# session.add(user)
# session.commit()

# Get the test user from the database as a proof of concept for database access.
# Refactor to user CRUD later.
def get_user_from_db() -> dict:
    user = session.get(User, 1)
    attr = user.getAttributes()
    return attr