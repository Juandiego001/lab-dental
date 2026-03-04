from flask_jwt_extended import jwt_required
from core.app import db
from core.services import categories
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message
from core.schemas.categories import CategoryInUpdate, CategoryInCreate, CategoryOut, CategoriesOut, CategorySearch
from flask_babel import gettext


bp = APIBlueprint('categories', __name__)


@bp.post('/search')
@bp.input(CategorySearch)
@bp.output(CategoriesOut)
@jwt_required()
def categories_brands(json_data):
    '''Search categories'''

    try:
        results, total = categories.search_categories(
            category_id=json_data['category_id'],
            name=json_data['name'],
            slug=json_data['slug'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:category_id>')
@bp.output(CategoryOut)
@jwt_required()
def get_category(category_id):
    '''Get category'''

    try:
        return categories.get_category_by_id(category_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(CategoryInCreate, arg_name='category')
@jwt_required()
def create_categories(category):
    '''Create categories'''

    try:
        db.session.add(category)
        db.session.commit()
        return {'message': gettext('categoryCreated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.put('/<int:category_id>')
@bp.input(CategoryInUpdate)
@bp.output(Message)
@jwt_required()
def update_categories(category_id, json_data):
    '''Update category'''
    try:
        categories.update_category(category_id, json_data)
        return {'message': gettext('categoryUpdated')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))


@bp.delete('/<int:category_id>')
@bp.output(Message)
@jwt_required()
def delete_categories(category_id):
    '''Delete categories'''

    try:
        categories.delete_category(category_id)
        return {'message': gettext('categoryDeleted')}
    except Exception as ex:
        print(gettext('abortException'))
        abort(500, gettext('abortException'))
