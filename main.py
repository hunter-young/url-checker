from typing import Optional, List
from fastapi import FastAPI, Depends, Response, status
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import uvicorn
import asyncio

from core import database, validations, crud, security, jobs

# grab environment variables and store them in a dictionary
settings = validations.EnvironmentSettings()
app = FastAPI()

# mount the static paths where the UI artifacts are stored
# we can't mount on "/" because apparently this overrides all other routes,
# not just those that aren't explicitly defined
app.mount("/ui", StaticFiles(directory=settings.build_directory, html=True), 
          name="build")
app.mount("/static", StaticFiles(directory= settings.build_directory + "/static"), 
          name="static")

async def get_orm_session() -> database.AsyncSession:
    async with database.OrmSession() as session:
        yield session

@app.on_event('startup')
async def initialize_data_and_jobs():
    async with database.engine.begin() as conn:
        # these queries are responsible for ensuring the necessary tables exist
        if settings.drop_all:
            await conn.run_sync(database.Base.metadata.drop_all)
        await conn.run_sync(database.Base.metadata.create_all)
    async with database.OrmSession() as session:
        async with session.begin():
            # sqlite doesn't have foreign keys turned on by default apparently
            await session.execute('PRAGMA foreign_keys=ON;')
            # start all of the existing URL checks defined in the database
            definitions = await crud.get_check_defintions(session=session)
            for db_check_definition in definitions:
                asyncio.create_task(jobs.url_check_job(db_check_definition), 
                                    name=db_check_definition.id)

# since we can't mount static files on "/", redirect requests from root to "/ui"
@app.get('/')
async def redirect_for_ui(auth = Depends(security.has_auth)):
    response = RedirectResponse(url='/ui')
    return response

@app.get('/latestresults', response_model=List[validations.LatestResult])
async def get_latest_results(response: Response, urlcontains: Optional[str] = None, 
                             orm_session: database.AsyncSession = Depends(get_orm_session), 
                             auth = Depends(security.has_auth)):
    db_latest_checks = await crud.get_latest_results(orm_session, urlcontains)
    # the 'X-Total-Count' header works to allow pagination to occur. 
    # This isn't really implemented correctly, but works fine for small datasets 
    response.headers['X-Total-Count'] = str(len(db_latest_checks))
    return db_latest_checks

@app.get('/checkdefinitions', response_model=List[validations.Check])
async def get_url_checks(response: Response, urlcontains: Optional[str] = None, 
                         orm_session: database.AsyncSession = Depends(get_orm_session), 
                         auth = Depends(security.has_auth)):
    db_check_definitions = await crud.get_check_defintions(orm_session, urlcontains)
    response.headers['X-Total-Count'] = str(len(db_check_definitions))
    return db_check_definitions

@app.post('/checkdefinitions', status_code=status.HTTP_201_CREATED)
async def create_url_check(check_definition: validations.CheckBase, 
                           orm_session: database.AsyncSession = Depends(get_orm_session),
                           auth = Depends(security.has_auth)):
    db_check_definition = await crud.create_check_defintion(orm_session, check_definition)
    asyncio.create_task(jobs.url_check_job(db_check_definition), name=db_check_definition.id)
    return db_check_definition

@app.get('/checkdefinitions/{checkId}', response_model=validations.CheckWithResults)
async def get_url_check_info(checkId: int, response: Response, 
                             orm_session: database.AsyncSession = Depends(get_orm_session),
                             auth = Depends(security.has_auth)):
    db_check_definition = await crud.get_check_definition_by_id(orm_session, checkId)
    db_check_definition
    if not db_check_definition:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    return db_check_definition

@app.put('/checkdefinitions/{checkId}', status_code=status.HTTP_201_CREATED)
async def update_url_check(checkId: int, check_definition: validations.CheckBase, 
                           response: Response, 
                           orm_session: database.AsyncSession = Depends(get_orm_session),
                           auth = Depends(security.has_auth)):
    rows_affected = await crud.update_check_definition_by_id(orm_session, checkId, check_definition)
    if rows_affected == 1:
        # if a job definition was actually uupdated, we should kill the old task...
        await jobs.cancel_task_by_name(str(checkId))
        db_check_definition = validations.Check(id=checkId, **check_definition.dict())
        # ... and spin up a new task with the updated definition
        asyncio.create_task(jobs.url_check_job(db_check_definition), name=checkId)
        return db_check_definition
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.delete('/checkdefinitions/{checkId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_url_check(checkId: int, 
                           orm_session: database.AsyncSession = Depends(get_orm_session),
                           auth = Depends(security.has_auth)):
    rows_affected = await crud.delete_check_definition_by_id(orm_session, checkId)
    if rows_affected == 1:
        # if a job definition was actually deleted, we should kill the active task
        await jobs.cancel_task_by_name(str(checkId))
        # some APIs return the deleted record, some just return 204 No Content.
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/checkresults', response_model=List[validations.CheckResult])
async def get_check_results(response: Response, 
                            orm_session: database.AsyncSession = Depends(get_orm_session),
                            auth = Depends(security.has_auth)):
    results = await crud.get_check_results(orm_session)
    response.headers['X-Total-Count'] = str(len(results))
    return results

@app.get('/notificationaddresses', response_model=List[validations.NotificationAddress])
async def get_notification_addresses(response: Response, checkId: Optional[int] = None, 
                                     orm_session: database.AsyncSession = Depends(get_orm_session),
                                     auth = Depends(security.has_auth)):
    addresses = await crud.get_notification_addresses(orm_session, checkId)
    response.headers['X-Total-Count'] = str(len(addresses))
    return addresses

@app.get('/notificationaddresses/{notificationId}', response_model=validations.NotificationAddress)
async def get_notification_address_by_id(notificationId: int, 
                                         orm_session: database.AsyncSession = Depends(get_orm_session),
                                         auth = Depends(security.has_auth)):
    address = await crud.get_notification_address_by_id(orm_session, notificationId)
    return address

@app.post('/notificationaddresses', status_code=status.HTTP_201_CREATED)
async def create_notification_address(address_definition: validations.NotificationAddressBase, 
                                      orm_session: database.AsyncSession = Depends(get_orm_session),
                                      auth = Depends(security.has_auth)):
    db_address_definition = await crud.create_notification_address(orm_session, address_definition)
    return db_address_definition

@app.put('/notificationaddresses/{addressId}', status_code=status.HTTP_201_CREATED)
async def update_notification_address(addressId: int, 
                                      address_definition: validations.NotificationAddressBase, 
                                      response: Response, 
                                      orm_session: database.AsyncSession = Depends(get_orm_session),
                                      auth = Depends(security.has_auth)):
    rows_affected = await crud.update_notification_address_by_id(orm_session, addressId, address_definition)
    if rows_affected == 1:
        db_check_definition = validations.NotificationAddress(id=addressId, **address_definition.dict())
        return db_check_definition
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.delete('/notificationaddresses/{notificationId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification_address(notificationId: int, 
                                      orm_session: database.AsyncSession = Depends(get_orm_session),
                                      auth = Depends(security.has_auth)):
    rows_affected = await crud.delete_notification_address_by_id(orm_session, notificationId)
    if rows_affected == 1:
        # some APIs return the deleted record, some just return 204 No Content.
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=80, reload=True)