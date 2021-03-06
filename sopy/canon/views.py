from flask import redirect
from flask_wtf import Form
from sopy import db
from sopy.auth.login import group_required, current_user
from sopy.canon import bp
from sopy.canon.forms import CanonItemForm
from sopy.canon.models import CanonItem
from sopy.ext.views import template, redirect_for


@bp.route('/')
@template('canon/index.html')
def index():
    items = CanonItem.query.order_by(CanonItem.title).all()

    return {'items': items}


@bp.route('/<int:id>/')
@template('canon/detail.html')
def detail(id):
    item = CanonItem.query.get_or_404(id)

    return {'item': item}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@template('canon/update.html')
@group_required('approved')
def update(id=None):
    item = CanonItem.query.get_or_404(id) if id is not None else None
    form = CanonItemForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = CanonItem()
            db.session.add(item)

        form.populate_obj(item)
        item.updated_by = current_user
        db.session.commit()

        return redirect(item.detail_url)

    return {'item': item, 'form': form}


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@template('canon/delete.html')
@group_required('approved')
def delete(id):
    item = CanonItem.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()

        return redirect_for('canon.index')

    return {'item': item, 'form': form}
