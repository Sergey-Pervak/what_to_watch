from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

# Подключить БД SQLite.
app = Flask(__name__)
app.config.from_object(Config)
app.json.ensure_ascii = False
# Создать экземпляр SQLAlchemy и в качестве параметра
# передать в него экземпляр приложения Flask.
# Создать экземпляр класса SQLAlchemy и передать
# в качестве параметра экземпляр приложения Flask.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import cli_commands, error_handlers, views
