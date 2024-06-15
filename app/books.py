import os
import bleach

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db, app
from models import Book, Review, Category, Role, Cover, User
from auth import check_rights
from tools import ImageSaver

book_bp = Blueprint('books', __name__, url_prefix='/books')

@book_bp.route('/<int:book_id>')
def show(book_id):
    selected_book = Book.query.get(book_id)
    associated_image = Cover.query.filter(Cover.book_id == book_id).first()
    return render_template('book/show.html', book=selected_book, image=associated_image)

@book_bp.route('/create', methods=['GET', 'POST'])
@login_required
@check_rights('create_book')
def create():
    available_genres = Category.query.all()
    number_of_genres = len(available_genres)

    if request.method == 'POST':
        try:
            new_book = Book(
                name=bleach.clean(request.form.get('book_title')),
                short_desc=bleach.clean(request.form.get('book_short_description')),
                author=bleach.clean(request.form.get('book_author')),
                publisher=bleach.clean(request.form.get('book_publisher')),
                publisher_year=request.form.get('book_publish_year'),
                size=request.form.get('book_volume')
            )
            
            for genre_id in request.form.getlist('book_genres'):
                genre = Category.query.get(genre_id)
                new_book.genres.append(genre)

            db.session.add(new_book)

            file = request.files.get('book_img')
            if file and file.filename:
                ImageSaver(file, new_book).save()

            db.session.commit()

            flash('Книга успешно добавлена.', 'success')
            return redirect(url_for('books.show', book_id=new_book.id))
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'warning')
            return render_template('book/create.html', genres=available_genres, genres_count=number_of_genres, book=new_book)

    return render_template('book/create.html', genres=available_genres, genres_count=number_of_genres, book=None)

@book_bp.route('/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights('update_book')
def edit(book_id):
    all_genres = Category.query.all()
    count_genres = len(all_genres)

    selected_book = Book.query.get(book_id)
    book_image = Cover.query.filter(Cover.book_id == book_id).first()
    if request.method == 'POST':
        try:
            selected_book.name = bleach.clean(request.form.get('book_title'))
            selected_book.short_desc = bleach.clean(request.form.get('book_short_description'))
            selected_book.author = bleach.clean(request.form.get('book_author'))
            selected_book.publisher = bleach.clean(request.form.get('book_publisher'))
            selected_book.publisher_year = request.form.get('book_publish_year')
            selected_book.size = request.form.get('book_volume')

            selected_book.genres = [Category.query.get(genre_id) for genre_id in request.form.getlist('book_genres')]

            db.session.add(selected_book)
            db.session.commit()

            flash('Книга успешно обновлена.', 'success')
            return render_template('book/show.html', book=selected_book, image=book_image)
        except Exception:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'warning')
            return render_template('book/edit.html', genres=all_genres, genres_count=count_genres, book=selected_book, publish_year=selected_book.publisher_year)

    return render_template('book/edit.html', genres=all_genres, genres_count=count_genres, book=selected_book, publish_year=selected_book.publisher_year)

@book_bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
@check_rights('delete_book')
def delete(book_id):
    try:
        book_to_delete = Book.query.get(book_id)
        cover_image = Cover.query.filter(Cover.book_id == book_id).first()

        if cover_image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_image.storage_filename)

        book_to_delete.genres.clear()
        db.session.delete(book_to_delete)
        db.session.commit()

        if cover_image:
            os.remove(image_path)
    except Exception:
        flash('Ошибка при удалении книги.', 'warning')
        return redirect(url_for('index'))

    flash('Книга успешно удалена.', 'success')
    return redirect(url_for('index'))

@book_bp.route('/<int:book_id>/create_review', methods=['POST'])
@login_required
@check_rights('read_book')
def create_review(book_id):
    existing_review = Review.query.filter_by(book_id=book_id, user_id=current_user.id).first()
    print(existing_review,)
    if existing_review:
        flash('Вы уже оставили отзыв.', 'danger')
    else:
        try:
            new_review = Review(
                rating=request.form.get('review-rating'),
                text=bleach.clean(request.form.get('review-text')),
                book_id=book_id,
                user_id=current_user.id
            )
            
            db.session.add(new_review)
            db.session.commit()

            flash('Рецензия отправлена.', 'success')
            return redirect(url_for('books.show', book_id=book_id))
        except Exception:
            db.session.rollback()
            flash('При создании рецензии возникла ошибка. Проверьте корректность введённых данных.', 'warning')
            return redirect(url_for('books.show', book_id=book_id))

    return redirect(url_for('books.show', book_id=book_id))
