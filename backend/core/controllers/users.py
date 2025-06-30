from flask import jsonify
from core import get_user_permissions
from core.app import db
from core.services import users
from apiflask import APIBlueprint, abort
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message, Pagination
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, current_user
from core.schemas.users import UserInLogIn, UserInUpdate, UserInCreate, UserOut, UsersOut, ProfileIn, ProfileOut


bp = APIBlueprint('users', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(UsersOut)
def get_users(query_data):
    '''Get users'''

    try:
        results = users.get_users(query_data['search'],
                                  query_data['page'],
                                  query_data['per_page'])
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:user_id>')
@bp.output(UserOut)
def get_user(user_id):
    '''Get user'''

    try:
        return users.get_user_by_id(user_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/login')
@bp.input(UserInLogIn, arg_name='user')
def login_users(user):
    '''Users Log In'''

    try:
        user = users.login(user['email'], user['password'])
        user_data = ProfileOut().dump(user)
        access_token = create_access_token(
            identity=str(user.id), additional_claims=user_data)
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response
    except HTTPException as ex:
        abort(404, str(ex))
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.post('/')
@bp.input(UserInCreate)
@jwt_required()
def create_users(json_data):
    '''Create users'''

    try:
        user_data, distributor_id = json_data
        users.create_user(current_user, user_data, distributor_id)
        return {'message': 'User created successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.get('/profile')
@bp.output(ProfileOut)
@jwt_required(optional=True)
def get_profile():
    '''
    Obtiene los datos del perfil de usuario
    '''
    try:
        if not get_jwt_identity():
            return {}
        user_id = int(get_jwt_identity())
        user_detail = users.get_user_by_id(user_id)
        user_profile = ProfileOut().dump(user_detail)
        user_profile['abilities'] = [
            {'subject': ability[0], 'action': ability[1]} for ability in get_user_permissions(user_id)]
        return user_profile
    except Exception as ex:
        abort(500, str(ex))


@bp.put('/profile')
@jwt_required()
@bp.input(ProfileIn, arg_name='user_data')
@bp.output(Message)
def update_profile(user_data):
    '''
    Actualización del perfil de usuario
    :param user_data:
    '''
    try:
        db.session.merge(user_data)
        db.session.commit()
        response = jsonify({'message': 'User updated successfully'})
        return response
    except Exception as ex:
        abort(500, str(ex))


@bp.put('/<int:user_id>')
@bp.input(UserInUpdate)
@bp.output(Message)
def update_users(user_id, json_data):
    '''Update user'''
    try:
        users.update_user(user_id, json_data)
        return {'message': 'User updated successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:user_id>')
@bp.output(Message)
def delete_users(user_id):
    '''Delete users'''

    try:
        users.delete_user(user_id)
        return {'message': 'User deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
