from datetime import datetime
from flask import Flask, session, g, render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('websiteconfig')


# database instance
cors = CORS(app)
db: SQLAlchemy = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app=app, db=db, directory='backend/migrations')

# server landing page
@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return {
        'success': False,
        'message': 'Not Found',
    }, 404


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(id=session['user_id']).first() \
        if 'user_id' in session else None


@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}


from backend.views import general, auth
app.register_blueprint(general.mod)
app.register_blueprint(auth.mod)

from backend.database import User, db_session, init_db
from backend import utils

init_db()

app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
