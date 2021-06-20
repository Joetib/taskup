from datetime import datetime
from flask import Flask, session, g, render_template
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object('websiteconfig')



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


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


app.add_url_rule('/docs/', endpoint='docs.index', build_only=True)
app.add_url_rule('/docs/<path:page>/', endpoint='docs.show',
                 build_only=True)
app.add_url_rule('/docs/<version>/.latex/Flask.pdf', endpoint='docs.pdf',
                 build_only=True)

from backend.views import general
app.register_blueprint(general.mod)

from backend.database import User, db_session, init_db
from backend import utils

ma = Marshmallow(app)


init_db()


app.jinja_env.filters['datetimeformat'] = utils.format_datetime
app.jinja_env.filters['dateformat'] = utils.format_date
app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
