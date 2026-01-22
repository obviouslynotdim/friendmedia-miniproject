from portfo import db
from sqlalchemy import Integer, String, ForeignKey
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    fullname: Mapped[str] = mapped_column(String(50), nullable=True)
    avatar: Mapped[str] = mapped_column(String(50), default='default.png')

    # Relationship with FriendProfile
    friend_profiles: Mapped[List['FriendProfile']] = relationship('FriendProfile', back_populates='user')

    def __repr__(self):
        return f'<User: {self.username}>'

class FriendProfile(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[str] = mapped_column(String(200), nullable=True)
    img: Mapped[str] = mapped_column(String(50), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))  # Foreign key to User

    user: Mapped[User] = relationship('User', back_populates='friend_profiles')  # Back reference to User

    def __repr__(self):
        return f'<FriendProfile: {self.fullname}>'
