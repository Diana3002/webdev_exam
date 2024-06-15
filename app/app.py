from flask import Flask, render_template, send_from_directory, abort, request
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from models import db, Cover, Book, Category
from sqlalchemy import func

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)
PER_PAGE = 10


from auth import auth_bp, init_login_manager
from books import book_bp

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)


PER_PAGE = 5

init_login_manager(app)


@app.route('/')
def index():
    title = request.args.get('title', None)
    genres = request.args.getlist('genre')
    years = request.args.getlist('year')
    volume_from = request.args.get('volume_from', None)
    volume_to = request.args.get('volume_to', None)
    author = request.args.get('author', None)

    query = Book.query

    if title:
        query = query.filter(func.lower(Book.name).like(f"%{title.lower()}%"))
    if genres:
        query = query.filter(Book.genres.any(Category.name.in_(genres)))
    if years:
        query = query.filter(Book.publisher_year.in_(years))
    if volume_from:
        query = query.filter(Book.size >= int(volume_from))
    if volume_to:
        query = query.filter(Book.size <= int(volume_to))
    if author:
        query = query.filter(func.lower(Book.author).like(f"%{author.lower()}%"))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page)
    books = pagination.items

    all_genres = Category.query.all() 
    all_years = db.session.query(Book.publisher_year).distinct().all()

    genres = [genre.name for genre in all_genres]
    years = [year[0] for year in all_years]

    return render_template('index.html', books=books, pagination=pagination,
                           genres=genres, years=years,
                           title=title, selected_genres=genres,
                           selected_years=years, volume_from=volume_from,
                           volume_to=volume_to, author=author)


@app.route('/media/images/<string:image_id>')
def image(image_id):
    image = Cover.query.get(image_id)

    if image is None:
        abort(404)

    return send_from_directory(app.config['UPLOAD_FOLDER'], image.storage_filename)