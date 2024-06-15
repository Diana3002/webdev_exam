from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort, current_app
from flask_login import login_required, current_user
from mysql_db import MySQL
import markdown
import os
from werkzeug.utils import secure_filename
import hashlib
from functools import wraps
from flask_paginate import Pagination, get_page_parameter
import math

app = Flask(__name__)
application = app
app.debug = True

db = MySQL(app)

from auth import bp_auth, init_login_manager

app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.register_blueprint(bp_auth)

init_login_manager(app)

app.config.from_pyfile('config.py')


#ну вроде готово
@app.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page

    cursor = db.connection().cursor(named_tuple=True)

    query = '''
        SELECT 
            book_des.id, 
            book_des.name AS title, 
            book_des.description AS description, 
            book_des.year AS year, 
            book_des.publishing AS publishing, 
            book_des.author AS author, 
            book_des.volume AS volume, 
            COUNT(reviews.id) AS review_count,
            AVG(reviews.grade) AS average_grade,
            GROUP_CONCAT(genre.name SEPARATOR ', ') AS genres
        FROM book_des 
        LEFT JOIN reviews ON book_des.id = reviews.book 
        LEFT JOIN book_genre ON book_des.id = book_genre.book_id
        LEFT JOIN genre ON book_genre.genre_id = genre.id
        GROUP BY book_des.id 
        ORDER BY book_des.year DESC
        LIMIT %s, %s
    '''
    cursor.execute(query, (offset, per_page))
    books = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) AS total FROM book_des')
    total_books = cursor.fetchone().total
    total_pages = math.ceil(total_books / per_page)

    cursor.close()

    return render_template('index.html', books=books, current_page=page, total_pages=total_pages)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_all_genres():
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute('SELECT id, name FROM genre')
    genres = cursor.fetchall()
    cursor.close()
    return genres

@app.route('/add_book', methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        genre_id = request.form['genre']
        year = request.form['year']
        author = request.form['author']
        volume = request.form['volume']
        description = request.form['description']
        publishing = request.form['publishing']
        
        cover = request.files['cover']
        if cover and allowed_file(cover.filename):
            filename = secure_filename(cover.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cover.save(file_path)
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            cursor = db.connection().cursor()

            # Вставка информации о обложке книги
            query = '''
                INSERT INTO book_cov (filename, mime_type, md5_hash)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(query, (filename, cover.mimetype, file_hash))
            cover_id = cursor.lastrowid

            # Вставка информации о книге
            query = '''
                INSERT INTO book_des (name, description, year, publishing, author, volume, cover)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (name, description, year, publishing, author, volume, cover_id))
            book_id = cursor.lastrowid

            # Проверка наличия записи о жанре книги
            query_check_genre = '''
                SELECT * FROM book_genre
                WHERE book_id = %s AND genre_id = %s
            '''
            cursor.execute(query_check_genre, (book_id, genre_id))
            existing_genre = cursor.fetchone()

            if existing_genre:
                # Если запись уже существует, можно выполнить обновление или другие действия
                flash('Книга уже имеет указанный жанр', 'warning')
            else:
                # Если записи нет, вставляем новую запись о жанре книги
                query_insert_genre = '''
                    INSERT INTO book_genre (book_id, genre_id)
                    VALUES (%s, %s)
                '''
                cursor.execute(query_insert_genre, (book_id, genre_id))
            
            db.connection().commit()
            cursor.close()
            
            flash('Книга успешно добавлена', 'success')
            return redirect(url_for('add_book'))
    
    genres = get_all_genres() 
    return render_template('add_book.html', genres=genres)


def admin_or_moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and (current_user.role == 1 or current_user.role == 2):
            return f(*args, **kwargs)
        else:
            flash("У вас нет прав для доступа к этой странице.", "danger")
            return redirect(url_for("index"))
    return decorated_function

@app.route('/edit_book/<int:book_id>', methods=["GET", "POST"])
@login_required
@admin_or_moderator_required
def edit_book(book_id):
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute('SELECT * FROM book_des WHERE id = %s', (book_id,))
    book = cursor.fetchone()

    if not book:
        flash("Книга не найдена.", "danger")
        return redirect(url_for("add_book"))

    if request.method == 'POST':
        name = request.form['name']
        genre_id = request.form['genre']
        year = request.form['year']
        author = request.form['author']
        volume = request.form['volume']
        description = request.form['description']
        publishing = request.form['publishing']

        query = '''
            UPDATE book_des SET name = %s, description = %s, year = %s, publishing = %s, author = %s, volume = %s
            WHERE id = %s
        '''
        cursor.execute(query, (name, description, year, publishing, author, volume, book_id))

        query = '''
            UPDATE book_genre SET genre_id = %s WHERE book_id = %s
        '''
        cursor.execute(query, (genre_id, book_id))

        db.connection().commit()
        cursor.close()
        flash('Книга успешно обновлена', 'success')
        return redirect(url_for('add_book'))

    genres = get_all_genres()
    return render_template('edit_book.html', book=book, genres=genres)



from flask import jsonify, current_app, flash
import os

@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        return jsonify(success=False, message="Недостаточно прав"), 403

    try:
        cursor = db.connection().cursor()

        # Получение информации о книге для удаления обложки
        query_cover_id = 'SELECT cover FROM book_des WHERE id = %s'
        cursor.execute(query_cover_id, (book_id,))
        cover_id = cursor.fetchone()

        if not cover_id or not cover_id[0]:
            cursor.close()
            return jsonify(success=False, message="Обложка не найдена"), 404

        # Удаление записей о жанрах книги из таблицы book_genre
        delete_genre_query = 'DELETE FROM book_genre WHERE book_id = %s'
        cursor.execute(delete_genre_query, (book_id,))

        # Удаление книги из таблицы book_des
        delete_book_query = 'DELETE FROM book_des WHERE id = %s'
        cursor.execute(delete_book_query, (book_id,))

        # Получение имени файла обложки из таблицы book_cov
        query_cover_filename = 'SELECT filename FROM book_cov WHERE id = %s'
        cursor.execute(query_cover_filename, (cover_id[0],))  # cover_id[0] - это идентификатор обложки
        cover_filename = cursor.fetchone()

        
        
        if not cover_filename or not cover_filename[0]:
            cursor.close()
            return jsonify(success=False, message="Файл обложки не найден в базе данных"), 404

        # Формируем путь к файлу обложки
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_filename[0])

        # Удаляем файл обложки, если он существует
        if os.path.exists(file_path):
            os.remove(file_path)

        delete_cover_query = 'DELETE FROM book_cov WHERE id = %s'
        cursor.execute(delete_cover_query, (cover_id[0],))

        db.connection().commit()
        cursor.close()

        flash('Книга успешно удалена.', 'success')
        return jsonify(success=True)

    except Exception as e:
        print(f"Ошибка при удалении книги: {e}")
        db.connection().rollback()
        cursor.close()
        return jsonify(success=False, message="Ошибка сервера при удалении книги"), 500
    
@app.route('/book/<int:book_id>')
def view_book(book_id):
    try:
        cursor = db.connection().cursor(named_tuple=True)

        # Получение информации о книге
        query = '''
        SELECT book_des.id, book_des.name AS title, book_des.description AS description, book_des.year AS year, 
               book_des.publishing AS publishing, book_des.author AS author, book_des.volume AS volume, 
               book_cov.filename AS cover_filename
        FROM book_des 
        LEFT JOIN book_cov ON book_des.cover = book_cov.id 
        WHERE book_des.id = %s
        '''
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()

        if not book:
            abort(404)

        # Преобразование описания в формат Markdown
        book_description_md = markdown.markdown(book.description)

        # Получение обзоров
        query_reviews = '''
        SELECT reviews.id, reviews.grade, reviews.text, users.login AS user
        FROM reviews
        JOIN users ON reviews.user = users.id
        WHERE reviews.book = %s
        '''
        cursor.execute(query_reviews, (book_id,))
        reviews = cursor.fetchall()

        # Получение жанров
        query_genres = '''
        SELECT genre.name
        FROM genre
        JOIN book_genre ON genre.id = book_genre.genre_id
        WHERE book_genre.book_id = %s
        '''
        cursor.execute(query_genres, (book_id,))
        genres = [genre.name for genre in cursor.fetchall()]

        # Проверка, написал ли пользователь уже рецензию на эту книгу
        user_review = None
        if current_user.is_authenticated:
            query_user_review = '''
            SELECT id, grade, text
            FROM reviews
            WHERE book = %s AND user = %s
            '''
            cursor.execute(query_user_review, (book_id, current_user.id))
            user_review = cursor.fetchone()

        cursor.close()

        # Создаем словарь с данными книги
        book_dict = {
            'id': book.id,
            'title': book.title,
            'description': book_description_md,
            'year': book.year,
            'publishing': book.publishing,
            'author': book.author,
            'volume': book.volume,
            'cover_filename': book.cover_filename,
            'genres': ', '.join(genres)
        }

        return render_template('view_book.html', book=book_dict, reviews=reviews, user_review=user_review)

    except Exception as e:
        print(f"Ошибка при просмотре книги: {e}")
        abort(500)

@app.route('/book/<int:book_id>/add_review', methods=['POST'])
@login_required
def add_review(book_id):
    try:
        cursor = db.connection().cursor()

        # Проверяем, что пользователь аутентифицирован
        if not current_user.is_authenticated:
            flash("Требуется аутентификация", 'danger')
            return redirect(url_for('login'))  # Перенаправляем на страницу логина

        # Проверяем, что книга существует
        query_check_book = 'SELECT id FROM book_des WHERE id = %s'
        cursor.execute(query_check_book, (book_id,))
        book = cursor.fetchone()

        if not book:
            flash("Книга не найдена", 'danger')
            return redirect(url_for('index'))

        # Получаем данные из POST-запроса
        grade = request.form.get('grade')
        text = request.form.get('text')

        # Проверяем, написал ли пользователь уже рецензию на эту книгу
        query_check_review = 'SELECT id FROM reviews WHERE book = %s AND user = %s'
        cursor.execute(query_check_review, (book_id, current_user.id))
        existing_review = cursor.fetchone()

        if existing_review:
            flash("Рецензия уже была добавлена", 'warning')
            return redirect(url_for('view_book', book_id=book_id))

        # Добавляем рецензию
        query_add_review = '''
        INSERT INTO reviews (book, user, grade, text)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query_add_review, (book_id, current_user.id, grade, text))
        db.connection().commit()

        cursor.close()

        flash('Рецензия успешно добавлена.', 'success')

        # Загружаем данные для отображения страницы книги с обновленной информацией
        return redirect(url_for('view_book', book_id=book_id))

    except Exception as e:
        print(f"Ошибка при добавлении рецензии: {e}")
        db.connection().rollback()
        cursor.close()
        flash("Ошибка сервера при добавлении рецензии", 'danger')
        return redirect(url_for('view_book', book_id=book_id))


@app.route('/book/<int:book_id>/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(book_id, review_id):
    cursor = db.connection().cursor(named_tuple=True)

    if request.method == 'POST':
        # Проверяем, что рецензия принадлежит текущему пользователю
        query_check_review = '''
        SELECT id
        FROM reviews
        WHERE id = %s AND user = %s
        '''
        cursor.execute(query_check_review, (review_id, current_user.id))
        review = cursor.fetchone()

        if not review:
            flash('Рецензия не найдена или у вас нет прав на удаление.', 'danger')
            return redirect(url_for('view_book', book_id=book_id))

        # Удаляем рецензию
        query_delete_review = '''
        DELETE FROM reviews
        WHERE id = %s
        '''
        cursor.execute(query_delete_review, (review_id,))
        db.connection().commit()

        cursor.close()

        flash('Рецензия успешно удалена.', 'success')
        return redirect(url_for('view_book', book_id=book_id))

    cursor.close()

    return redirect(url_for('view_book', book_id=book_id))

def get_roles():
    cursor = db.connection().cursor(named_tuple=True)
    query = 'SELECT * FROM role'
    cursor.execute(query)
    roles = cursor.fetchall()
    cursor.close()
    return roles