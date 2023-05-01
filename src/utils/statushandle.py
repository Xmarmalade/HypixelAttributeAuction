from fastapi import HTTPException

def handle_status_code(status_code: int):
    if status_code == 200:
        return
    elif status_code == 400:
        raise HTTPException(status_code=status_code, detail='Query Parameters Error')
    elif status_code == 403:
        raise HTTPException(status_code=status_code, detail='Forbidden Access')
    elif status_code == 404:
        raise HTTPException(status_code=status_code, detail='Page not found')
    elif status_code == 422:
        raise HTTPException(status_code=status_code, detail='Invalid Data')
    elif status_code == 429:
        raise HTTPException(status_code=status_code, detail='Rate Limited')