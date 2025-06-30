from core.app import db
from core.models import Distributor, DistributorList, List_, User, UserList
from sqlalchemy import or_, and_
from bcrypt import checkpw
from werkzeug.exceptions import HTTPException


def login(email: str, password: str):
    user = db.session.query(User).filter(User.email == email).first()
    if not user or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException('User or password incorrect')
    return user


def get_users(search: str, page: int, per_page: int):
    '''Get users'''

    query = User.status == 'ACTIVE'
    if search:
        query = and_(User.status == 'ACTIVE',
                     or_(User.full_name.ilike(f'%{search}%'),
                         User.username.ilike(f'%{search}%'),
                         User.email.ilike(f'%{search}%')))

    return db.paginate(db.session.query(User).filter(query).order_by(User.id.desc()),
                       page=page, per_page=per_page, count=True)


def get_user_by_id(user_id: int):
    '''Get user by user id'''

    return db.session.query(
        *User.__table__.c,
        Distributor.id.label('distributor_id'),
        Distributor.name.label('distributor_name')
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


def update_user(user_id: int, user_load):
    '''Update user'''

    if not check_user_exists(user_id):
        raise HTTPException('User not found')

    db.session.merge(user_load)
    db.session.commit()


def delete_user(user_id: int):
    '''Delete user'''

    db.session.merge(User(id=user_id, status='INACTIVE'))
    db.session.commit()
