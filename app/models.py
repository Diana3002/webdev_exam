import os
from typing import Optional, Union, List
from datetime import datetime
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
        return ADMIN_ROLE_ID == self.role_id

    @property
    def is_moderator(self):
        return MODERATOR_ROLE_ID == self.role_id

    @property
    def is_user(self):
        return USER_ROLE_ID == self.role_id

    def can(self, action, book_id = None):
        user_policy = UsersPolicy(book_id)
        method = getattr(user_policy, action)
        if method is not None: return method()
        else: return False
    



    def __repr__(self):
        return '<User {}>'.format(self.username) 
    
class Role(db.Model):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return '<role %r>' % self.name


books_category = db.Table('books_category',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False)
)

class Book(db.Model):
    __tablename__ = 'book'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    publisher_year: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher: Mapped[str] = mapped_column(String(255), nullable=False)
    short_desc: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    image = db.relationship('Cover', cascade="all, delete, delete-orphan")
    reviews = db.relationship('Review', cascade="all, delete, delete-orphan")
    genres = db.relationship('Category', secondary=books_category, cascade="all, delete")

    @property
    def score(self):    
        sum = 0
        reviews = Review.query.filter(Review.book_id == self.id).all()

        for review in reviews:
            sum += review.rating

        try:
            return round(sum / len(self.reviews), 2)
        except ZeroDivisionError:
            return 0.0

    @property
    def reviews_count(self):
        reviews = Review.query.filter(Review.book_id == self.id).all()
        return len(reviews)

    @property
    def formatted_description(self):
        return markdown.markdown(self.short_desc)

    def __repr__(self):
        return '<Book %r>' % self.name
    
class Review(db.Model):
    __tablename__ = 'review'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    book_id: Mapped[Optional[int]] = mapped_column(ForeignKey("book.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column( default=datetime.now(), nullable=False,)

    book = db.relationship('Book')
    user = db.relationship('User')
    @property
    def rating_word(self):
        return RATING_BOOK.get(self.rating)
    
    @property
    def formatted_text(self):
        return markdown.markdown(self.text)

    def __repr__(self):
        return '<Review %r>' % self.id


class Cover(db.Model):
    __tablename__ = "cover"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    file_name: Mapped[str] = mapped_column(String(100))
    mime_type: Mapped[str] = mapped_column(String(100))
    md5_hash: Mapped[str] = mapped_column(String(100), unique=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('book.id'), nullable=False)

    book = db.relationship('Book')

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    def __repr__(self):
        return '<Cover %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('cover', cover_id=self.id)


class Category(db.Model):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return '<category %r>' % self.name







