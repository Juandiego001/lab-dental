from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required


bp = APIBlueprint('modules', __name__)


@bp.get('/')
@jwt_required()
def get_modules():
    '''Get modules'''
    pass


@bp.post('/')
@jwt_required()
def create_modules():
    '''Create modules'''
    pass


@bp.put('/')
@jwt_required()
def update_modules():
    '''Update modules'''
    pass


@bp.delete('/')
@jwt_required()
def delete_modules():
    '''Delete modules'''
    pass