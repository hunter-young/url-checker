import asyncio
import httpx
from datetime import datetime
from . import database, crud, validations, notifications

"""This module houses all URL check logic and job scheduling functions"""

# get environment variables
settings = validations.EnvironmentSettings()

# helper functions for job 
async def get_receivers(session: database.AsyncSession, 
                        check_definition_id: int):
    receivers = await crud.get_notification_addresses_by_check_id(
        session, check_definition_id)
    return [x.emailAddress for x in receivers]

async def get_state(response, check_definition: validations.Check):
    if check_definition.expectedString:
        expected_string_passes = check_definition.expectedString in response.text
    else:
        expected_string_passes = True
    status_passes = response.status_code == check_definition.expectedStatus        
    return expected_string_passes and status_passes

# main job logic
async def run_check(check_definition: validations.Check, 
                    client: httpx.AsyncClient, fail_count: int):
    response = await client.get(check_definition.url)
    success = await get_state(response, check_definition)
    if not success:
        async with database.OrmSession() as session:
            async with session.begin():
                receivers = await get_receivers(session, check_definition.id)
        # errors shouldn't be fatal, so we'll let them bubble up to stdout
        await notifications.send_alert(check_definition, receivers)
        fail_count += 1
        if fail_count == settings.max_failures:
            # errors shouldn't be fatal, so we'll let them bubble up to stdout
            await notifications.send_admin_alert(check_definition)
    else:
        fail_count = 0
    check_result = validations.CheckResultBase(
        checkId=check_definition.id,
        statusCode=response.status_code,
        state='SUCCESS' if success else 'FAILURE',
        timeChecked=datetime.now()
    )
    async with database.OrmSession() as session:
        async with session.begin():
            await crud.save_check_result(session, check_result)
    return fail_count
            
# loop for job
async def url_check_job(check_definition: validations.Check):
    async with httpx.AsyncClient() as client:
        fail_count = 0
        while True:
            fail_count = await run_check(check_definition, client, fail_count)
            await asyncio.sleep(check_definition.frequency)
            
# scheduling utilities
async def cancel_task_by_name(name: str):
    for task in asyncio.all_tasks():
        if task.get_name() == name:
            try: 
                task.cancel()
                await task
            except asyncio.CancelledError:
                pass  # this exception is raised as a confirmation the task was canceled