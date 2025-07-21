from flask_jwt_extended import jwt_required
from core.app import db
from core.services import locations
from apiflask import APIBlueprint, abort
from core.schemas.utils import Message, Pagination
from core.schemas.locations import LocationOut, LocationsOut


bp = APIBlueprint('locations', __name__)


@bp.get('/countries')
@bp.input(Pagination, location='query')
@bp.output(LocationsOut)
@jwt_required()
def get_countries(query_data):
    '''Get countries'''

    try:
        return {'items': locations.get_countries(query_data['search'],
                                                 query_data['page'],
                                                 query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/states/<string:country_id>')
@bp.input(Pagination, location='query')
@bp.output(LocationsOut)
@jwt_required()
def get_states(query_data, country_id):
    '''Get states'''

    try:
        return {'items': locations.get_states(
            country_id,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/cities/<string:state_id>')
@bp.input(Pagination, location='query')
@bp.output(LocationsOut)
@jwt_required()
def get_cities(query_data, state_id):
    '''Get cities'''

    try:
        return {'items': locations.get_cities(
            state_id,
            query_data['search'],
            query_data['page'],
            query_data['per_page'])}
    except Exception as ex:
        abort(500, str(ex))
