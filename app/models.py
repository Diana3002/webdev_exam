import os
from typing import Optional, Union, List
from datetime import datetime
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, MetaData
from user_policy import UsersPolicy
import markdown

ADMIN_ROLE_ID = 1
MODERATOR_ROLE_ID = 2
USER_ROLE_ID = 3

RATING_BOOK = {
    5: 'Отлично',
    4: 'Хорошо',
    3: 'Удовлетворительно',
    2: 'Неудовлетворительно',
    1: 'Плохо',
    0: 'Ужасно',
}

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    @property
    def is_admin(self):
        return self.role_id == ADMIN_ROLE_ID

    @property
    def is_moderator(self):
        return self.role_id == MODERATOR_ROLE_ID

    @property
    def is_user(self):
        return self.role_id == USER_ROLE_ID

    def can(self, action, book_id=None):
        policy = UsersPolicy(book_id)
        method = getattr(policy, action)
        if method is not None:
            return method()
        return False

    def __repr__(self):
        return f'<User {self.login}>'

class Role(db.Model):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

books_category = db.Table(
    'books_category',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False)
)

class Book(db.Model):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    publisher_year: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher: Mapped[str] = mapped_column(String(255), nullable=False)
    short_desc: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    image = relationship('Cover', cascade="all, delete, delete-orphan")
    reviews = relationship('Review', cascade="all, delete, delete-orphan")
    genres = relationship('Category', secondary=books_category, cascade="all, delete")

    @property
    def score(self):
        total_rating = sum(review.rating for review in self.reviews)
        try:
            return round(total_rating / len(self.reviews), 2)
        except ZeroDivisionError:
            return 0.0

    @property
    def reviews_count(self):
        return len(self.reviews)

    @property
    def formatted_description(self):
        return markdown.markdown(self.short_desc)

    def __repr__(self):
        return f'<Book {self.name}>'

class Review(db.Model):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("book.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    book = relationship('Book')
    user = relationship('User')

    @property
    def rating_word(self):
        return RATING_BOOK.get(self.rating)

    @property
    def formatted_text(self):
        return markdown.markdown(self.text)

    def __repr__(self):
        return f'<Review {self.id}>'

class Cover(db.Model):
    __tablename__ = "cover"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    file_name: Mapped[str] = mapped_column(String(100))
    mime_type: Mapped[str] = mapped_column(String(100))
    md5_hash: Mapped[str] = mapped_column(String(100), unique=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('book.id'), nullable=False)

    book = relationship('Book')

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return f"{self.id}{ext}"

    @property
    def url(self):
        return url_for('cover', cover_id=self.id)

    def __repr__(self):
        return f'<Cover {self.file_name}>'

class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
