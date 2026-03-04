from flask_jwt_extended import jwt_required
from core.services import locations
from apiflask import APIBlueprint, abort
from core.schemas.locations import LocationSearch, LocationsOut
from flask_babel import gettext


bp = APIBlueprint('locations', __name__)


@bp.post('/countries/search')
@bp.input(LocationSearch)
@bp.output(LocationsOut)
@jwt_required()
def search_countries(json_data):
    '''Search countries'''

    try:
        results, total = locations.search_countries(
            country_id=json_data['id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/states/<string:country_id>/search')
@bp.input(LocationSearch)
@bp.output(LocationsOut)
@jwt_required()
def search_states(json_data, country_id):
    '''Search states'''

    try:
        results, total = locations.search_states(
            country_id=country_id,
            state_id=json_data['id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/cities/<string:state_id>/search')
@bp.input(LocationSearch)
@bp.output(LocationsOut)
@jwt_required()
def get_cities(json_data, state_id):
    '''Get cities'''

    try:
        results, total = locations.search_cities(
            state_id=state_id,
            city_id=json_data['id'],
            name=json_data['name'],
            page=json_data['page'],
            per_page=json_data['per_page'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))
