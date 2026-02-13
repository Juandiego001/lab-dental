from flask import jsonify
from core import get_user_permissions
from core.app import db
from core.services import users
from apiflask import APIBlueprint, abort
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, current_user
from core.schemas.users import EmailIn, PasswordIn, TokenIn, UserInLogIn, UserInUpdate, UserInCreate, UserOut, UserSearch, UsersExistingIn, UsersOut, ProfileIn, ProfileOut


bp = APIBlueprint('users', __name__)


@bp.post('/search')
@bp.input(UserSearch)
@bp.output(UsersOut)
@jwt_required()
def get_users(json_data):
    '''Search users'''

    try:
        results, total = users.search_users(
            current_user=current_user,
            users_ids=json_data['users_ids'],
            distributor_id=json_data['distributor_id'],
            is_main=json_data['is_main'],
            role=json_data['role'],
            full_name=json_data['full_name'],
            username=json_data['username'],
            email=json_data['email'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:user_id>')
@bp.output(UserOut)
@jwt_required()
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
        response = jsonify(access_token=access_token,
                           message=f'Welcome {user_data['full_name']}')
        set_access_cookies(response, access_token)
        return response
    except HTTPException as ex:
        abort(404, ex.description)
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
@bp.input(ProfileIn, arg_name='user_data')
@bp.output(Message)
@jwt_required()
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
@jwt_required()
def update_users(user_id, json_data):
    '''Update user'''
    try:
        users.update_user(user_id, json_data)
        return {'message': 'User updated successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.post('/admins')
@bp.input(UsersExistingIn)
@bp.output(UsersOut)
@jwt_required()
def get_admin_users(json_data):
    '''Get admin users'''

    try:
        if current_user.role != 'ADMIN':
            return {'items': [], 'total': 0}

        results = users.get_admin_users(
            json_data['search'] if 'search' in json_data else '',
            json_data['users_ids'] if 'users_ids' in json_data else []
        )
        return {'items': results, 'total': results.total}
    except Exception as ex:
        abort(500, str(ex))


@bp.delete('/<int:user_id>')
@bp.output(Message)
@jwt_required()
def delete_users(user_id):
    '''Delete users'''

    try:
        users.delete_user(user_id)
        return {'message': 'User deleted successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.get('/token')
@bp.input(TokenIn, location='query')
@bp.output(Message)
def validate_token(query_data):
    try:
        if not users.validate_token(query_data['token']):
            raise Exception('Token is invalid')
        return {'message': 'Token validated'}
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/password')
@bp.input(EmailIn)
@bp.output(Message)
def send_mail_recover_password(json_data):
    '''
    Send mail to recover password

    :param json_data: Description
    '''

    try:
        return {'message': 'A recovery link has been sent. Please check your email'}
    finally:
        try:
            users.send_mail_recover_password(json_data['email'])
        except:
            pass


@bp.patch('/password')
@bp.input(PasswordIn)
@bp.output(Message)
def change_password(json_data):
    try:
        users.change_password(json_data['token'], json_data['password'])
        return {'message': 'The password has been successfully updated'}
    except Exception as ex:
        abort(500, str(ex))
