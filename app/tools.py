import hashlib
import uuid
import os

from werkzeug.utils import secure_filename

from models import Cover
from app import db, app

class ImageSaver:
    def __init__(self, file, book):
        self.file = file
        self.book = book

    def save(self):
        existing_image = self.__get_image_by_md5()
        if existing_image:
            return self.__add_image_to_db(existing_image)
        
        new_image = self.__create_new_image()
        self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_image.storage_filename))
        
        db.session.add(new_image)
        db.session.commit()
        return new_image

    def __get_image_by_md5(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Cover.query.filter_by(md5_hash=self.md5_hash).first()

    def __add_image_to_db(self, existing_image):
        self.img = Cover(
            id=str(uuid.uuid4()),
            file_name=secure_filename(self.file.filename),
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash,
            book_id=self.book.id
        )
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __create_new_image(self):
        return Cover(
            id=str(uuid.uuid4()),
            file_name=secure_filename(self.file.filename),
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash,
            book_id=self.book.id
        )
