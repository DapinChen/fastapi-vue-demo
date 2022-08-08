from datetime import datetime
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from ..config import Base

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    role = relationship('RoleModel', secondary='user_roles')

    # generate hash password
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    # verify login password
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    name = Column(Enum('Admin', 'Medical', 'Operation', name='role_enum'), unique=True, nullable=False)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class UserRoleModel(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))
