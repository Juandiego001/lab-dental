from core.app import FRONTEND_APP_BASE_URL, app
from core.app import db, r
from core.models import Distributor, DistributorList, List_, User, UserList
from sqlalchemy import or_, and_, case
from bcrypt import checkpw
from werkzeug.exceptions import HTTPException
from secrets import token_urlsafe

from core.services.distributors import get_distributor_from_user
from core.utils import send_mail


def login(email_or_username: str, password: str):
    '''Login'''

    user = db.session.query(User).filter(
        or_(User.email == email_or_username, User.username == email_or_username)).first()
    if not user or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException('Incorrect username or password')
    return user


def search_users(current_user: User, users_ids: list[int], distributor_id: int, is_main: bool, role: str, full_name: str, username: str, email: str, page: int, per_page: int):
    '''Search users'''

    query = [User.status == 'ACTIVE']
    with_users_ids = None
    if distributor_id:
        query.append(Distributor.id == distributor_id)
    if is_main:
        query.append(List_.is_main == True)
    if role:
        query.append(User.role == role)
    if full_name:
        query.append(User.full_name.ilike(f'%{full_name}%'))
    if username:
        query.append(User.username.ilike(f'%{username}%'))
    if email:
        query.append(User.email.ilike(f'%{email}%'))
    if users_ids:
        query.append(User.id.not_in(users_ids))
        with_users_ids = db.session.query(User)\
            .filter(User.id.in_(users_ids))\
            .all()

    if current_user.role != 'ADMIN':
        distributor: Distributor = get_distributor_from_user(current_user)
        query.append(User.role != 'ADMIN')
        query.append(Distributor.id == distributor.id)

    total = db.session.query(User)\
        .select_from(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(*query)\
        .count()
    
    print('TOTAL: ')
    print(total)

    total += len(with_users_ids) if with_users_ids else 0
    users = db.session.query(User)\
        .select_from(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(*query)\
        .order_by(User.id.desc())\
        .limit(per_page)\
        .offset((page - 1) * per_page)\
        .all()
    
    if not with_users_ids:
        return users, total
    return with_users_ids + users, total


def get_admin_users(search: str, users_ids: list[int] = []):
    '''Get admin users'''

    query = [User.status == 'ACTIVE', User.role == 'ADMIN']
    if search:
        query.append(or_(User.full_name.ilike(f'%{search}%'),
                         User.username.ilike(f'%{search}%'),
                         User.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(User)
                       .filter(or_(and_(*query), User.id.in_(users_ids)))
                       .order_by(User.id.desc()),
                       page=1, per_page=15, count=True)


def get_user_by_id(user_id: int):
    '''Get user by user id'''

    return db.session.query(
        *User.__table__.c,
        case((Distributor.id == 1, None),
             else_=Distributor.id).label('distributor_id'),
        case((Distributor.name == 'Snapon', ''),
             else_=Distributor.name).label('distributor_name'),
    )\
        .select_from(User)\
        .join(UserList)\
        .join(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(and_(User.id == user_id, List_.is_main))\
        .first()


def check_user_exists(user_id: int):
    '''Check if user exists'''

    return db.session.query(User).filter(User.id == user_id).first()


def create_user(current_user: User, user_data: User, distributor_id: int):
    '''Create user and associate it with their distributor list'''

    db.session.add(user_data)
    db.session.flush()

    # Get main list
    if not distributor_id:
        main_list = db.session.query(List_)\
            .join(UserList)\
            .filter(and_(UserList.user_id == current_user.id, List_.is_main))\
            .first()
    else:
        main_list = db.session.query(List_)\
            .join(DistributorList)\
            .filter(and_(DistributorList.distributor_id == distributor_id, List_.is_main))\
            .first()

    # Create users_lists
    user_list = UserList(user_id=user_data.id, list_id=main_list.id)
    db.session.add(user_list)
    db.session.commit()


def update_user(user_id: int, json_load: tuple[User, int]):
    '''Update user'''

    if not check_user_exists(user_id):
        raise HTTPException('User not found')

    user_obj, distributor_id = json_load

    # If there is any distributor id is because it's a change to Snapon distributors or admins role
    distributor_id = distributor_id if distributor_id else 1

    # Delete old user list
    user_list = db.session.query(UserList)\
        .select_from(UserList)\
        .join(List_)\
        .join(User)\
        .filter(and_(List_.is_main, UserList.user_id == user_id))\
        .first()
    db.session.delete(user_list)

    # Insert new user list
    list_distributor = db.session.query(List_)\
        .join(DistributorList)\
        .join(Distributor)\
        .filter(and_(Distributor.id == distributor_id, List_.is_main))\
        .first()
    new_user_list = UserList(user_id=user_id, list_id=list_distributor.id)
    db.session.add(new_user_list)

    db.session.merge(user_obj)
    db.session.commit()


def delete_user(user_id: int):
    '''Delete user'''

    db.session.merge(User(id=user_id, status='INACTIVE'))
    db.session.commit()


def validate_token(token: str):
    '''Validate existing token in redis'''

    return r.keys(f'recover:*{token}')


def send_mail_recover_password(email: str):
    '''
    Send mail to recover the password if the email exists

    :param email: Description
    :type email: str
    '''

    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        return
    if not user.email:
        return

    keys = r.keys(f'recover:{user.id}*')
    # If the recovery link already exists, simply return
    if keys:
        return

    token = token_urlsafe(16)
    link = f'{FRONTEND_APP_BASE_URL}/recover-password/{token}'
    send_mail('Recover Password', [user.email],
              'recover_password.html', {'link': link})
    r.set(f'recover:{user.id}:{token}', user.id, ex=300)


def change_password(token: str, password: str):
    '''
    Docstring for change_password
    '''

    keys = r.keys(f'recover:*{token}')
    if not keys:
        raise Exception('User not found')

    user_id = int(r.get(keys[0]))

    the_user = db.session.query(User).filter(User.id == user_id).first()
    the_user.password = password

    db.session.merge(the_user)
    db.session.commit()

    r.delete(keys[0])
