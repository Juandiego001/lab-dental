from core.app import db
from core.models import Address, Site
from core.services import sites
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.schemas.utils import Message, Pagination
from core.schemas.sites import SiteInUpdate, SiteInCreate, SiteOut, SitesInstallationsOut, SitesOut


bp = APIBlueprint('sites', __name__)


@bp.get('/')
@bp.input(Pagination, location='query')
@bp.output(SitesOut)
@jwt_required()
def get_sites(query_data):
    '''Get sites'''

    try:
        results, total = sites.get_sites(
            current_user,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])


        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/clients/<string:client_id>')
@bp.input(Pagination, location='query')
@bp.output(SitesInstallationsOut)
@jwt_required()
def get_clients_sites(query_data, client_id):
    '''Get clients sites'''

    try:
        return {'items': sites.get_clients_sites(client_id, query_data['search'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/distributors/<string:distributor_id>')
@bp.input(Pagination, location='query')
@bp.output(SitesInstallationsOut)
@jwt_required()
def get_distributors_sites(query_data, distributor_id):
    '''Get distributors sites'''

    try:
        return {'items': sites.get_distributors_sites(distributor_id, query_data['search'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<int:site_id>')
@bp.output(SiteOut)
@jwt_required()
def get_site(site_id):
    '''Get site'''

    try:
        return sites.get_site_by_id(site_id)
    except Exception as ex:
        abort(500, str(ex))


@bp.post('/')
@bp.input(SiteInCreate, arg_name='site_and_address')
@jwt_required()
def create_sites(site_and_address):
    '''Create sites'''

    try:
        # Se obtienen dirección y sede
        address: Address = site_and_address[0]
        site: Site = site_and_address[1]

        # Se crea objeto de dirección
        db.session.add(address)
        db.session.flush()

        # Se crea objeto de sede
        site.address_id = address.id
        db.session.add(site)
        db.session.commit()
        return {'message': 'Site registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.put('/<int:site_id>')
@bp.input(SiteInUpdate, arg_name='site_and_address')
@bp.output(Message)
@jwt_required()
def update_sites(site_id, site_and_address):
    '''Update site'''

    try:
        address: Address = site_and_address[0]
        site: Site = site_and_address[1]

        db.session.merge(address)
        db.session.merge(site)
        db.session.commit()
        return {'message': 'Site registered successfully'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))


@bp.delete('/<int:site_id>')
@bp.output(Message)
@jwt_required()
def delete_sites(site_id):
    '''Delete sites'''

    try:
        sites.delete_site(site_id)
        return {'message': 'Site deleted successfuly'}
    except Exception as ex:
        print(str(ex))
        abort(500, str(ex))
