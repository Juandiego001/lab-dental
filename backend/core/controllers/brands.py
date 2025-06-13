from core.app import db
from core.services import brands
from apiflask import APIBlueprint, abort
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message, Pagination
from core.schemas.brands import BrandInUpdate, BrandInCreate, BrandOut, BrandsOut


bp = APIBlueprint('brands', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(BrandsOut)
def get_brands(query_data):
    '''Get brands'''

    try:
        results = brands.get_brands(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:brand_id>')
@bp.output(BrandOut)
def get_brand(brand_id):
    '''Get brand'''

    try:
        return brands.get_brand_by_id(brand_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(BrandInCreate, arg_name='brand')
def create_brands(brand):
    '''Create brand'''

    try:
        db.session.add(brand)
        db.session.commit()
        return {'message': 'Brand registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:brand_id>')
@bp.input(BrandInUpdate)
@bp.output(Message)
def update_brands(brand_id, json_data):
    '''Update brand'''
    try:
        brands.update_brand(brand_id, json_data)
        return {'message': 'Brand updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:brand_id>')
@bp.output(Message)
def delete_brands(brand_id):
    '''Delete brands'''

    try:
        brands.delete_brand(brand_id)
        return {'message': 'Brand deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
