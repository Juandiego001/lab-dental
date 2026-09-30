from flask import jsonify, request
from core import get_user_permissions
from core.app import db
from core.services import users
from apiflask import APIBlueprint, abort
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, current_user, unset_jwt_cookies
from core.schemas.users import EmailIn, PasswordIn, TokenIn, UserInLogIn, UserInUpdate, UserInCreate, UserOut, UserSearch, UsersExistingIn, UsersOut, ProfileIn, ProfileOut, TokenPasswordIn, PhotoIn
from flask_babel import gettext, force_locale
from datetime import timedelta


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
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:user_id>')
@bp.output(UserOut)
@jwt_required()
def get_user(user_id):
    '''Get user'''

    try:
        return users.get_user_by_id(user_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/login')
@bp.input(UserInLogIn, arg_name='user')
def login_users(user):
    '''Users Log In'''

    try:
        user = users.login(user['email'], user['password'])
        user_data = ProfileOut().dump(user)
        access_token = create_access_token(
            identity=str(user.id), additional_claims=user_data, expires_delta=timedelta(days=1))
        with force_locale(user_data['language']):
            response = jsonify(access_token=access_token,
                               message=f'{gettext('welcome')} {user_data['fullName']}')
        set_access_cookies(response, access_token)
        return response
    except HTTPException as ex:
        abort(404, gettext('wrongUsernamePassword'))
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@jwt_required()
@bp.input(UserInCreate)
@bp.output(Message)
def create_users(json_data):
    '''Create users'''

    try:
        user_data, distributor_id = json_data
        users.create_user(current_user, user_data, distributor_id)
        return {'message': gettext('userCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


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
        user_profile['full_name'] = user_profile.pop('fullName')
        user_profile['photo'] = user_profile.pop('photo')
        user_profile['abilities'] = [
            {'subject': ability[0], 'action': ability[1]} for ability in get_user_permissions(user_id)]
        return user_profile
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.patch('/profile')
@jwt_required()
@bp.input(ProfileIn, arg_name='user_data')
@bp.output(Message)
def update_profile(user_data: dict):
    '''
    Actualización del perfil de usuario
    :param user_data:
    '''
    try:
        user = users.update_profile(
            current_user=current_user, user_data=user_data)
        user_data = ProfileOut().dump(user)
        access_token = create_access_token(
            identity=str(user.id), additional_claims=user_data)

        with force_locale(user_data['language']):
            response = jsonify(access_token=access_token,
                               message=gettext('profileUpdated'))
        set_access_cookies(response, access_token)
        return response
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:user_id>')
@jwt_required()
@bp.input(UserInUpdate)
@bp.output(Message)
def update_users(user_id, json_data):
    '''Update user'''
    try:
        users.update_user(user_id, json_data)
        return {'message': gettext('userUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/admins')
@jwt_required()
@bp.input(UsersExistingIn)
@bp.output(UsersOut)
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
        abort(500, gettext('abortException'))


@bp.delete('/<int:user_id>')
@jwt_required()
@bp.output(Message)
def delete_users(user_id):
    '''Delete users'''

    try:
        users.delete_user(user_id)
        return {'message': gettext('userDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/token')
@bp.input(TokenIn, location='query')
@bp.output(Message)
def validate_token(query_data):
    try:
        if not users.validate_token(query_data['token']):
            raise HTTPException('Token is invalid')
        return {'message': gettext('tokenValid')}
    except HTTPException as ex:
        abort(404, gettext('tokenInvalid'))
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/password')
@jwt_required()
@bp.input(PasswordIn, arg_name='user_data')
@bp.output(Message)
def change_password(user_data):
    '''
    Actualización de la contraseña del usuario
    :param user_data:
    '''
    try:
        db.session.merge(user_data)
        db.session.commit()
        return {'message': gettext('passwordUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/password')
@bp.input(EmailIn)
@bp.output(Message)
def send_mail_recover_password(json_data):
    '''
    Send mail to recover password

    :param json_data: Description
    '''

    try:
        return {'message': gettext('recoveryLinkSent')}
    finally:
        try:
            users.send_mail_recover_password(json_data['email'])
        except Exception as ex:
            pass


@bp.patch('/password')
@bp.input(TokenPasswordIn)
@bp.output(Message)
def change_password_by_token(json_data):
    try:
        users.change_password(json_data['token'], json_data['password'])
        return {'message': gettext('passwordUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/logout')
@bp.output(Message)
def logout():
    '''
    Cerrar sessión de usuario
    '''
    try:
        token = request.cookies.get('access_token_cookie')
        response = jsonify({'message': gettext('sessionEnded')})
        unset_jwt_cookies(response)
        # if token:
        #     jwt_payload = decode_token(token)
        #     ex = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')) * 60
        #     sub, jti = jwt_payload['sub'], jwt_payload['jti']
        #     redis.set(f'sac:blocklist:{sub}:{jti}', '', ex=ex)
        return response
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/photo')
@jwt_required()
@bp.input(PhotoIn, location='form_and_files')
@bp.output(Message)
def upload_user_photo(form_and_files_data: dict):
    '''Upload user photo'''

    try:
        users.upload_user_photo(
            current_user,
            form_and_files_data
        )
        return {'message': gettext('photoUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/photo')
@jwt_required()
@bp.output(Message)
def delete_user_photo():
    '''Delete user photo'''

    try:
        users.delete_user_photo(current_user)
        return {'message': gettext('photoUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))
