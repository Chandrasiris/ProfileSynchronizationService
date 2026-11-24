from fastapi import HTTPException

async def require_staff():
    # Never accept unverified JWTs or development bypass headers.
    raise HTTPException(status_code=503,detail='Identity integration not configured')
