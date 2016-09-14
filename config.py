SECRET_KEY = 'you-will-never-know-me'
WTF_CSRF_SECRET_KEY = 'me-neither'
DEBUG=True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
