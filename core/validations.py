from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, BaseSettings, HttpUrl

"""In general, all of the classes in this module are used to validate inputs and outputs
are as expected. These are used for both internal variables as well as external
API record schemas."""

class EnvironmentSettings(BaseSettings):
    """This class is responsible for validating all required
    environment variables are present."""
    # app config
    admin_email: str
    max_failures: int = 3
    sender_email: str 
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_use_tls: bool = True

    # set this to true to drop all data from the db
    drop_all: bool = False

    # credentials
    api_key: str = 'supersecretkey123'
    admin_username: str = 'admin' 
    admin_password: str = 'admin' # for convenience in demo

    # frontend build info
    build_directory = "ui/url-checker/build"

    class Config:
        env_file = '.env'

class NotificationAddressBase(BaseModel):
    checkId: int
    emailAddress: str

    class Config:
        orm_mode = True

class NotificationAddress(NotificationAddressBase):
    id: int

    class Config:
        orm_mode = True

class CheckBase(BaseModel):
    url: HttpUrl
    frequency: int
    expectedStatus: int
    expectedString: Optional[str] = None

class Check(CheckBase):
    id: int
    emailAddresses: Optional[List[NotificationAddress]] = []

    class Config:
        orm_mode = True

class LatestResult(CheckBase):
    id: int
    lastChecked: datetime
    lastState: str

    class Config:
        orm_mode = True

class CheckResultBase(BaseModel):
    checkId: int
    timeChecked: datetime
    statusCode: int
    state: str

class CheckResult(CheckResultBase):
    id: int
    checkDefinition: Optional[Check]

    class Config:
        orm_mode = True

class CheckWithResults(Check):
    results = str 

    class Config:
        orm_mode = True


    