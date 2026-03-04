from core.app import db
from flask_babel import gettext
from core.services import brands
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required
from core.schemas.utils import Message, Pagination
from core.schemas.brands import BrandInUpdate, BrandInCreate, BrandOut, BrandSearch, BrandsOut


bp = APIBlueprint('brands', __name__)


@bp.post('/search')
@bp.input(BrandSearch)
@bp.output(BrandsOut)
@jwt_required()
def search_brands(json_data):
    '''Search brands'''

    try:
        results, total = brands.search_brands(
            brand_id=json_data['brand_id'],
            name=json_data['name'],
            slug=json_data['slug'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:brand_id>')
@bp.output(BrandOut)
@jwt_required()
def get_brand(brand_id):
    '''Get brand'''

    try:
        return brands.get_brand_by_id(brand_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(BrandInCreate, arg_name='brand')
@jwt_required()
def create_brands(brand):
    '''Create brand'''

    try:
        db.session.add(brand)
        db.session.commit()
        return {'message': gettext('brandCreated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.put('/<int:brand_id>')
@bp.input(BrandInUpdate)
@bp.output(Message)
@jwt_required()
def update_brands(brand_id, json_data):
    '''Update brand'''
    try:
        brands.update_brand(brand_id, json_data)
        return {'message': gettext('brandUpdated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.delete('/<int:brand_id>')
@bp.output(Message)
@jwt_required()
def delete_brands(brand_id):
    '''Delete brands'''

    try:
        brands.delete_brand(brand_id)
        return {'message': gettext('brandDeleted')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))
