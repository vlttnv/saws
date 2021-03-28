
from flask import (
    Blueprint, config,
    render_template,
    g,
    redirect,
)
from flask.helpers import url_for
from flask_login import login_required
from saws.blueprints.utils.utils_ec2 import get_ec2_info



bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
@login_required
def index():
    if not g.user.account:
        return redirect(url_for('account.add_account'))
    return render_template('index.html')
