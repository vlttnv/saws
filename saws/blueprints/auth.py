import random
from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app as app,
)
from werkzeug.security import generate_password_hash
from flask_login import logout_user, current_user, login_user
from saws.models import db, User
from saws.forms import SignupForm, LoginForm
from saws import login_manager


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    signup_form = SignupForm(request.form)
    if request.method == 'POST':
        if signup_form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            error = None

            try:
                u = User.query.filter(User.email == email).first()
                if u:
                    error = 'User {} is already registered.'.format(email)
            except Exception:  # TODO: better error handling
                error = 'Error during registration'

            if error is None:
                new_user = User(
                    email=email,
                    password=generate_password_hash(password),
                )
                db.session.add(new_user)

                # confirmation = None
                # try:
                #     confirmation = UserConfirmation.query.filter_by(podcaster_id=new_user.id).one()
                # except NoResultFound:
                #     confirmation = UserConfirmation()

                # confirmation.id = str(uuid4())
                # confirmation.podcaster_id = new_user.id

                # db.session.add(confirmation)
                db.session.commit()

                # send_confirmation_email(email, new_user.id, confirmation.id)

                login_user(new_user)
                return redirect(url_for('index.index'))

            flash(error, 'danger')
            # return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=signup_form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        if login_form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            error = None
            user = None

            try:
                user = User.query.filter(User.email == email).first()
            except Exception:  # TODO: better error handling
                error = 'Error checking for user'

            if user is None or not user.check_password(password=password):
                error = 'Incorrect email or password'

            # if not user.confirmed:
            #     error = 'Please confirm your email first'

            if error is None:
                remember = True if request.form.get(
                    'remember_me') == 'y' else False
                login_user(user, remember=remember)
                nxt = request.args.get('next')
                return redirect(nxt or url_for('index.index'))

            flash(error, 'danger')

    return render_template('auth/login.html', form=login_form)


@bp.before_app_request
def load_logged_in_user():
    # TODO: fix this, there is a better way
    user_id = session.get('_user_id')

    if user_id is None:
        g.user = None
    else:
        u = User.query.get(user_id)
        g.user = u


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    # TODO: security
    """Redirect unauthorised users to Login page."""
    flash('Please log in to access this page.', 'danger')
    return redirect(url_for('auth.login', next=request.path))
