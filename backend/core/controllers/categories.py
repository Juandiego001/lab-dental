from flask_jwt_extended import jwt_required
from core.app import db
from core.services import categories
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.categories import CategoryInUpdate, CategoryInCreate, CategoryOut, CategoriesOut


bp = APIBlueprint('categories', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(CategoriesOut)
@jwt_required()
def get_categories(query_data):
    '''Get categories'''

    try:
        results = categories.get_categories(query_data['search'],
                                         query_data['page'],
                                         query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:category_id>')
@bp.output(CategoryOut)
@jwt_required()
def get_category(category_id):
    '''Get category'''

    try:
        return categories.get_category_by_id(category_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(CategoryInCreate, arg_name='category')
@jwt_required()
def create_categories(category):
    '''Create categories'''

    try:
        db.session.add(category)
        db.session.commit()
        return {'message': 'Category registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:category_id>')
@bp.input(CategoryInUpdate)
@bp.output(Message)
@jwt_required()
def update_categories(category_id, json_data):
    '''Update category'''
    try:
        categories.update_category(category_id, json_data)
        return {'message': 'Category updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:category_id>')
@bp.output(Message)
@jwt_required()
def delete_categories(category_id):
    '''Delete categories'''

    try:
        categories.delete_category(category_id)
        return {'message': 'Category deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
