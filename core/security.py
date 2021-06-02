import secrets
from fastapi import Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKeyCookie, APIKey
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from . import validations

settings = validations.EnvironmentSettings()

API_KEY_NAME = 'api_key'
API_KEY = settings.api_key

# having 'auto_error' set to False ensures that we can use any method to authenticate
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)
http_basic = HTTPBasic(auto_error=False)

async def is_admin(credentials: HTTPBasicCredentials = Depends(http_basic)):
    if credentials is None:
        return False
    correct_username = secrets.compare_digest(credentials.username, settings.admin_username)
    correct_password = secrets.compare_digest(credentials.password, settings.admin_password)
    return (correct_password and correct_username)

async def get_api_key(api_key_query: str = Security(api_key_query),
                      api_key_header: str = Security(api_key_header),
                      api_key_cookie: str = Security(api_key_cookie)):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
       return False

async def has_auth(is_admin: bool = Depends(is_admin),
                   api_key: APIKey = Depends(get_api_key)):
    if api_key:  # check for apikey first
        return True
    elif is_admin:  # fall back to http basic auth
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication required',
            headers={'WWW-Authenticate': 'Basic'}
        )

