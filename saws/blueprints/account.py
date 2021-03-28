from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    g,
)
from flask_login import login_required
from saws.forms import AddAccountForm
from saws.models import db, Account



bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_account():
    account_form = AddAccountForm(request.form)
    if request.method == 'POST':
        if account_form.validate():
            name = request.form.get('name')
            secret_key = request.form.get('secret_key')
            access_key = request.form.get('access_key')
            error = None

            new_account = Account(
                name=name,
                access_key=access_key,
                secret_key=secret_key,
                user_id=g.user.id,
            )
            db.session.add(new_account)
            db.session.commit()
            return redirect(url_for('index.index'))

    return render_template('account/add_account.html', form=account_form)

