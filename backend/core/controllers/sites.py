from core.app import db
from core.models import Address, Site
from core.services import sites
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.schemas.utils import Message
from core.schemas.sites import SiteInUpdate, SiteInCreate, SiteOut, SiteSearch, SitesInstallationsOut, SitesOut
from flask_babel import gettext


bp = APIBlueprint('sites', __name__)


@bp.post('/search')
@bp.input(SiteSearch)
@bp.output(SitesOut)
@jwt_required()
def search_sites(json_data):
    '''Search sites'''

    try:
        results, total = sites.search_sites(
            current_user=current_user,
            site_id=json_data['site_id'],
            distributor_id=json_data['distributor_id'],
            client_id=json_data['client_id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:site_id>')
@bp.output(SiteOut)
@jwt_required()
def get_site(site_id):
    '''Get site'''

    try:
        return sites.get_site_by_id(site_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(SiteInCreate, arg_name='site_and_address')
@jwt_required()
def create_sites(site_and_address):
    '''Create sites'''

    try:
        address: Address = site_and_address[0]
        site: Site = site_and_address[1]
        sites.create_site(current_user, site, address)
        return {'message': gettext('siteCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


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
        return {'message': gettext('siteUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:site_id>')
@bp.output(Message)
@jwt_required()
def delete_sites(site_id):
    '''Delete sites'''

    try:
        sites.delete_site(site_id)
        return {'message': gettext('siteDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
