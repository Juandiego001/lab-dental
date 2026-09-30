from flask import stream_with_context
from flask_babel import gettext
from werkzeug.exceptions import HTTPException
from core.services import distributors
from apiflask import APIBlueprint, abort
from flask_jwt_extended import jwt_required, current_user
from core.schemas.clients import ClientsOut
from core.schemas.utils import Message, Pagination
from core.schemas.distributors import (
    ContactInCreate, ContactOut, DistributorInCreate, DistributorInUpdate, DistributorOut, DistributorSearch, DistributorsOut, ContactSearch, ContactsOut,
    ContactIn, AlignerInCreate, AlignerFileIn, AlignersValidationsOut, AlignersMultipleIn, AlignerAliasIn
)


bp = APIBlueprint('distributors', __name__)


@bp.post('/search')
@bp.input(DistributorSearch)
@bp.output(DistributorsOut)
@jwt_required()
def search_distributors(json_data):
    '''Search distributors'''

    try:
        results, total = distributors.search_distributors(
            current_user=current_user,
            distributors_ids=json_data['distributors_ids'],
            name=json_data['name'],
            bp=json_data['bp'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:distributor_id>')
@bp.output(DistributorOut)
@jwt_required()
def get_distributor(distributor_id):
    '''Get distributor'''

    try:
        return distributors.get_distributor_by_id(distributor_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:distributor_id>/clients')
@bp.input(Pagination, location='query')
@bp.output(ClientsOut)
@jwt_required()
def get_clients_by_distributor(distributor_id, query_data):
    '''Get clients of a distributor'''

    try:
        return distributors.get_clients_by_distributor_id(distributor_id,
                                                          query_data['search'])
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/')
@bp.input(DistributorInCreate, arg_name='distributor')
@jwt_required()
def create_distributors(distributor: dict):
    '''Create distributors'''

    try:
        distributors.create_distributor(distributor)
        return {'message': gettext('distributorCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:distributor_id>')
@bp.input(DistributorInUpdate)
@bp.output(Message)
@jwt_required()
def update_distributors(distributor_id, json_data):
    '''Update distributor'''
    try:
        distributors.update_distributor(distributor_id, json_data)
        return {'message': gettext('distributorUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:distributor_id>')
@bp.output(Message)
@jwt_required()
def delete_distributors(distributor_id):
    '''Delete distributors'''

    try:
        distributors.delete_distributor(distributor_id)
        return {'message': gettext('distributorDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/contacts/search')
@bp.input(ContactSearch)
@bp.output(ContactsOut)
@jwt_required()
def search_contacts(json_data: dict):
    '''Search contacts'''

    try:
        results, total = distributors.search_contacts(
            distributor_id=json_data['distributor_id'],
            contacts_ids=json_data['contacts_ids'],
            full_name=json_data['full_name'],
            email=json_data['email'],
            phone=json_data['phone'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by'])
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/contacts/<int:contact_id>')
@bp.output(ContactOut)
@jwt_required()
def get_contact(contact_id: int):
    '''Get contact by id'''

    try:
        return distributors.get_contact_by_id(contact_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/contacts')
@bp.input(ContactInCreate)
@bp.output(Message)
@jwt_required()
def create_contacts(json_data: dict):
    '''Create contacts'''

    try:
        distributors.create_contacts(json_data)
        return {'message': gettext('contactCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/contacts/<int:contact_id>')
@bp.input(ContactIn)
@bp.output(Message)
@jwt_required()
def update_contacts(contact_id: int, json_data: dict):
    '''Update contacts'''

    try:
        distributors.update_contacts(
            contact_id=contact_id,
            data=json_data
        )
        return {'message': gettext('contactUpdated')}
    except HTTPException as ex:
        abort(400, str(ex))
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/contacts/<int:contact_id>')
@bp.output(Message)
@jwt_required()
def delete_contact(contact_id: int):
    '''Delete contact by id'''

    try:
        distributors.delete_contact_by_id(contact_id)
        return {'message': gettext('contactDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/aligners/<int:distributor_id>')
@jwt_required()
def get_all_aligners(distributor_id: int):
    '''Stream all aligners of a distributor with raw vehicles data'''
    try:
        return stream_with_context(distributors.stream_all_aligners(distributor_id))
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/aligners')
@bp.input(AlignerInCreate)
@bp.output(Message)
@jwt_required()
def associate_aligner_to_distributor(json_data: dict):
    '''Associate aligner to distributor'''

    try:
        distributors.associate_aligner_to_distributor(
            serial=json_data['serial'],
            distributor_id=json_data['distributor_id'],
        )
        return {'message': gettext('alignerAssociatedSuccessfully')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/aligners/file/<int:distributor_id>')
@bp.input(AlignerFileIn, location='form_and_files')
@bp.output(AlignersValidationsOut)
@jwt_required()
def validate_aligners_file(distributor_id: int, form_and_files_data: dict):
    '''Validate aligners file'''

    try:
        validations = distributors.validate_aligners_file(
            distributor_id=distributor_id,
            file=form_and_files_data['file']
        )
        return {'validations': validations}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/aligners/file/<int:distributor_id>')
@bp.input(AlignersMultipleIn)
@bp.output(Message)
@jwt_required()
def upload_multiple_aligners(distributor_id: int, json_data: dict):
    '''Validate aligners file'''

    try:
        distributors.upload_multiple_aligners(
            distributor_id=distributor_id,
            serials=json_data['serials']
        )
        return {'message': gettext('alignersPairedSuccessfully')}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/aligners/<int:aligner_id>')
@bp.output(Message)
@jwt_required()
def unlink_distributor_aligner(aligner_id: int):
    '''Unlink distributor aligner'''

    try:
        distributors.unlink_distributor_aligner(aligner_id=aligner_id)
        return {'message': gettext('alignerUnlinkedSuccessfully')}
    except Exception as ex:
        abort(500, gettext('abortException'))


# @bp.post('/aligners/file')
# @bp.input(AlignerInCreate)
# @bp.output(Message)
# @jwt_required()
# def associate_aligners_to_distributor_by_file(json_data: dict):
#     '''Associate aligners to distributor by plain text file'''

#     try:
#         distributors.associate_aligner_to_distributor_by_plain(
#             serial=json_data['serial'],
#             distributor_id=json_data['distributor_id'],
#         )
#         return {'message': gettext('alignerAssociatedSuccessfully')}
#     except Exception as ex:
#         abort(500, gettext('abortException'))


@bp.post('/aligners/alias/<int:aligner_id>')
@bp.input(AlignerAliasIn)
@bp.output(Message)
@jwt_required()
def set_aligner_alias(aligner_id: int, json_data: dict):
    '''Set alias for aligner'''

    try:
        distributors.set_aligner_alias(
            current_user=current_user,
            aligner_id=aligner_id,
            alias=json_data['alias']
        )
        return {'message': gettext('alignerAliasSetSuccessfully')}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, gettext('abortException'))
