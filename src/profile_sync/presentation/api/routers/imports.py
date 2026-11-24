from fastapi import APIRouter, Depends, UploadFile, HTTPException
from profile_sync.presentation.api.auth import require_staff
from profile_sync.config import Settings
from profile_sync.domain.project_name import extract_project_name
from profile_sync.domain.headers import identify_contacts
from profile_sync.infrastructure.file_readers.reader import read_sheet
from starlette.concurrency import run_in_threadpool

router=APIRouter(prefix='/api/v1/profile-imports',dependencies=[Depends(require_staff)])

@router.post('/inspect')
async def inspect_sheet(file: UploadFile):
    settings=Settings()
    limit=settings.MAX_UPLOAD_SIZE_MB*1024*1024
    try:
        data=await file.read(limit+1)
        name=file.filename or ''
        project=extract_project_name(name)
        sheet=await run_in_threadpool(read_sheet,data,name,limit,settings.MAX_IMPORT_ROWS,settings.MAX_IMPORT_COLUMNS)
        return {'project_name':project,'row_count':len(sheet.rows),'contact_columns':identify_contacts(sheet.headers)}
    except Exception:
        raise HTTPException(422,'Unable to validate screening sheet') from None
    finally: await file.close()
