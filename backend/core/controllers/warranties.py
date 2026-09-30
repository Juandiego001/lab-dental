from flask import send_file
from flask_babel import gettext
from core.services import warranties
from apiflask import APIBlueprint, abort
from flask_jwt_extended import current_user, jwt_required
from werkzeug.exceptions import HTTPException
from core.schemas.utils import Message
from core.schemas.warranties import WarrantyFileIn, WarrantyFileOut, WarrantyFilesIn, WarrantyFilesOut, WarrantyFilesSearch, WarrantyInUpdate, WarrantyInCreate, WarrantyOut, WarrantiesOut, WarrantyRejectCommentsIn, WarrantySearch


bp = APIBlueprint('warranties', __name__)


@bp.post('/search')
@bp.input(WarrantySearch)
@bp.output(WarrantiesOut)
@jwt_required()
def get_warranties(json_data):
    '''Get warranties'''

    try:
        results, total = warranties.get_warranties(
            current_user=current_user,
            distributor_id=json_data['distributor_id'],
            equipment_id=json_data['equipment_id'],
            wco_code=json_data['wco_code'],
            wco_year=json_data['wco_year'],
            sale_date=json_data['sale_date'],
            invoice=json_data['invoice'],
            serial=json_data['serial'],
            status=json_data['status'],
            page=json_data['page'],
            per_page=json_data['per_page'],
            sort_by=json_data['sort_by']
        )
        return {'items': results, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:warranty_id>')
@bp.output(WarrantyOut)
@jwt_required()
def get_warranty(warranty_id):
    '''Get warranty'''

    try:
        return warranties.get_warranty_by_id(warranty_id)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('')
@bp.input(WarrantyInCreate, location='form_and_files')
@jwt_required()
def create_warranties(form_and_files_data: dict):
    '''Create warranties'''

    try:
        warranty = warranties.create_warranty(form_and_files_data)
        warranties.notify_creation(warranty)
        return {'message': gettext('warrantyCreated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/<int:warranty_id>')
@bp.input(WarrantyInUpdate)
@bp.output(Message)
@jwt_required()
def update_warranties(warranty_id: int, json_data: dict):
    '''Update warranties'''
    try:
        warranties.update_warranty(warranty_id, json_data)
        warranties.notify_update(warranty_id)
        return {'message': gettext('warrantyUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/<int:warranty_id>')
@bp.output(Message)
@jwt_required()
def delete_warranties(warranty_id):
    '''Delete warranties'''

    try:
        warranties.delete_warranty(warranty_id)
        warranties.notify_delete(warranty_id)
        return {'message': gettext('warrantyDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/<int:warranty_id>/pdf')
@jwt_required()
def get_warranty_pdf(warranty_id: int):
    '''Get warranty PDF'''

    try:
        pdf_buffer = warranties.get_warranty_pdf(warranty_id)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f'{warranty_id}.pdf'
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.patch('/approve/<int:warranty_id>')
@bp.output(Message)
@jwt_required()
def approve_warranty(warranty_id: int):
    '''Approve warranty'''

    try:
        warranties.approve_warranty(
            current_user=current_user,
            warranty_id=warranty_id
        )
        warranties.notify_approval(warranty_id)
        return {'message': gettext('warrantyApproved')}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/reject/<int:warranty_id>')
@bp.input(WarrantyRejectCommentsIn)
@bp.output(Message)
@jwt_required()
def reject_warranty(warranty_id: int, json_data: dict):
    '''Reject warranty'''

    try:
        warranties.reject_warranty(warranty_id)
        warranties.notify_rejection(
            warranty_id, json_data['reject_comments'])
        return {'message': gettext('warrantyRejected')}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/<int:warranty_id>/files/search')
@jwt_required()
@bp.input(WarrantyFilesSearch)
@bp.output(WarrantyFilesOut)
def get_warranty_files(warranty_id: int, json_data: dict):
    '''Search warranty files'''

    try:
        items, total = warranties.search_warranty_files(
            warranty_id=warranty_id,
            title=json_data['title'],
            description=json_data['description'],
            original_name=json_data['original_name'],
            extension=json_data['extension'],
            page=json_data['page'],
            per_page=json_data['per_page']
        )
        return {'items': items, 'total': total}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.post('/<int:warranty_id>/files')
@jwt_required()
@bp.input(WarrantyFilesIn, location='form_and_files')
@bp.output(Message)
def add_warranty_files(warranty_id: int, form_and_files_data: dict):
    '''Add warranty files'''

    try:
        warranties.add_files(
            warranty_id=warranty_id,
            files=form_and_files_data['files']
        )
        return {'message': gettext('warrantyFilesAdded')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.get('/files/<int:file_id>')
@jwt_required()
@bp.output(WarrantyFileOut)
def get_warranty_file(file_id: int):
    '''Get warranty file'''

    try:
        return warranties.get_warranty_file(
            file_id=file_id
        )
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.put('/files/<int:file_id>')
@jwt_required()
@bp.input(WarrantyFileIn)
@bp.output(Message)
def update_warranty_file(file_id: int, json_data: dict):
    '''Update Warranty File'''

    try:
        warranties.update_warranty_file(
            file_id=file_id,
            data=json_data
        )
        return {'message': gettext('warrantyFileUpdated')}
    except Exception as ex:
        abort(500, gettext('abortException'))


@bp.delete('/files/<int:warranty_file_id>')
@jwt_required()
@bp.output(Message)
def delete_warranty_file(warranty_file_id: int):
    '''Delete warranty file'''

    try:
        warranties.remove_warranty_file(warranty_file_id=warranty_file_id)
        return {'message': gettext('warrantyFileDeleted')}
    except Exception as ex:
        abort(500, gettext('abortException'))
