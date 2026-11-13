from fastapi import APIRouter,Depends,Response
from ..config.database import get_db
from ..utils.auth import current,write_user,admin
from ..schemas.report import ReportCreate
from ..controllers import report_controller as controller
router=APIRouter(prefix='/reports',tags=['reports'])
@router.get('')
def listing(db=Depends(get_db),user=Depends(current)):return controller.list_all(db)
@router.get('/{ident}')
def detail(ident:str,db=Depends(get_db),user=Depends(current)):return controller.detail(db,ident)
@router.post('',status_code=201)
def create(body:ReportCreate,db=Depends(get_db),user=Depends(admin)):return controller.create(db,body)
@router.get('/{ident}/csv')
def export(ident:str,db=Depends(get_db),user=Depends(current)):
 from ..models.report import Report
 from ..controllers.common import require
 from ..services.report_service import export
 return Response(export(require(db,Report,ident)),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=evidence-inference.csv'})
