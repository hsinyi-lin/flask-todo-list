import os
from datetime import timedelta

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from utils.models import db
from views.auth import auth
from views.to_do import to_do

app = Flask(__name__)

bootstrap = Bootstrap(app)

# session settings
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=1)


# path to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(to_do)


@app.errorhandler(404)
def not_found(error):
    return '<h1>Not Found</h1>', 404


@app.errorhandler(405)
def method_not_allowed(error):
    return '<h1>Method Not Allowed</h1>', 405


@app.errorhandler(500)
def internal_server_error(error):
    return '<h1>Internal Server Error</h1>', 500


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
