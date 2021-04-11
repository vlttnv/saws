from flask.helpers import flash
from saws.forms import CreateSecurityGroupForm
from flask import (
    Blueprint,
    render_template,
    g,
    request,
    redirect,
    url_for,
    abort,
)
from flask_login import login_required
from saws.blueprints.utils.utils_networking import (
    add_sg_port,
    delete_security_group,
    delete_sg_port,
    describe_security_group,
    get_sgs,
    create_security_group,
)

bp = Blueprint("networking", __name__, url_prefix="/networking")


@bp.route("/security_groups", methods=["GET"])
@login_required
def security_groups():
    sgs = get_sgs(g.user.account)
    return render_template("networking/security_groups.html", sgs=sgs["SecurityGroups"])


@bp.route("/security_groups/<sg_id>", methods=["GET"])
@login_required
def security_group(sg_id):
    sg = describe_security_group(g.user.account, sg_id)
    if not sg:
        abort(404)

    return render_template("networking/security_group_edit.html", sg=sg)


@bp.route("/security_groups/create", methods=["GET", "POST"])
@login_required
def sg_create():
    sg_form = CreateSecurityGroupForm(request.form)
    if request.method == "POST":
        if sg_form.validate():
            name = request.form.get("name")
            description = request.form.get("description")
            sg = {
                "name": name,
                "description": description,
            }

            sg_id = create_security_group(g.user.account, sg)

            if not sg_id:
                abort(500)

            return redirect(url_for("networking.security_group", sg_id=sg_id))

    return render_template("networking/security_group_create.html")


@bp.route("/security_groups/<sg_id>/delete", methods=["GET"])
@login_required
def sg_delete(sg_id):
    delete_security_group(g.user.account, sg_id)

    flash(f"Delete security group {sg_id}", "success")
    return redirect(url_for("networking.security_groups"))


@bp.route("/security_groups/<sg_id>/add_port", methods=["POST"])
@login_required
def add_port(sg_id):
    protocol = request.form.get("protocol")
    port = request.form.get("port")

    if protocol == "no":
        flash("Please choose a protocol from the dropdown", "danger")
        return redirect(url_for("networking.security_group", sg_id=sg_id))

    try:
        port_from = int(port.split('-')[0])
        port_to = int(port.split('-')[-1])
    except Exception:
        flash("Please enter a valid port or port range", "danger")
        return redirect(url_for("networking.security_group", sg_id=sg_id))

    add_sg_port(g.user.account, port_from, port_to, protocol, sg_id)
    return redirect(url_for("networking.security_group", sg_id=sg_id))


@bp.route("/security_groups/<sg_id>/delete_port", methods=["GET"])
@login_required
def delete_port(sg_id):
    protocol = request.args.get("protocol")
    port = request.args.get("port")

    port_from = int(port.split('-')[0])
    port_to = int(port.split('-')[-1])

    delete_sg_port(g.user.account, port_from, port_to, protocol, sg_id)

    flash(f"{protocol} port {port} was removed.", "success")
    return redirect(url_for("networking.security_group", sg_id=sg_id))