from sqlalchemy import select, delete, update 
from sqlalchemy.sql.functions import max
from . database import AsyncSession
from . import models, validations

"""This module is responsible for general DAL (Data Access Layer) functions."""

async def get_check_defintions(session: AsyncSession, 
                               urlcontains: str = None) -> list[validations.Check]:
    query = select(models.CheckDefinition)
    if urlcontains:
        query = query.filter(models.CheckDefinition.url.contains(urlcontains))
    result = await session.execute(query)
    return result.scalars().all()

async def create_check_defintion(session: AsyncSession, 
                                 check_definition: validations.CheckBase):
    db_check_definition = models.CheckDefinition(**check_definition.dict())
    session.add(db_check_definition)
    await session.commit()
    return db_check_definition

async def get_check_definition_by_id(session: AsyncSession, checkId: int):
    result = await session.execute(select(models.CheckDefinition).filter(
        models.CheckDefinition.id == checkId))
    return result.scalars().first()

async def delete_check_definition_by_id(session: AsyncSession, checkId: int):
    result = await session.execute(delete(models.CheckDefinition).filter(
        models.CheckDefinition.id == checkId))
    await session.commit()
    return result.rowcount

async def update_check_definition_by_id(session: AsyncSession, checkId: int, 
                                        check_definition = validations.CheckBase):
    result = await session.execute(update(models.CheckDefinition).values(
        **check_definition.dict()).where(models.CheckDefinition.id == checkId))
    await session.commit()
    return result.rowcount

async def get_check_results(session: AsyncSession):
    result = await session.execute(select(models.CheckResult))
    return result.scalars().all()

async def save_check_result(session: AsyncSession, 
                            check_result: validations.CheckResultBase):
    db_check_result = models.CheckResult(**check_result.dict())
    session.add(db_check_result)
    await session.commit()
    return db_check_result

async def get_notification_addresses(session: AsyncSession, checkId: int = None):
    query = select(models.NotificationAddress)
    if checkId:
        query = query.filter(models.NotificationAddress.checkId == checkId)
    result = await session.execute(query)
    return result.scalars().all()

async def create_notification_address(session: AsyncSession, 
                                      address_definition: 
                                      validations.NotificationAddressBase):
    db_address_definition = models.NotificationAddress(**address_definition.dict())
    session.add(db_address_definition)
    await session.commit()
    return db_address_definition

async def get_notification_address_by_id(session: AsyncSession, 
                                         notificationId: int):
    result = await session.execute(select(models.NotificationAddress).filter(
        models.NotificationAddress.id == notificationId))
    return result.scalars().first()

async def delete_notification_address_by_id(session: AsyncSession, notificationId: int):
    result = await session.execute(delete(models.NotificationAddress).filter(
        models.NotificationAddress.id == notificationId))
    await session.commit()
    return result.rowcount

async def update_notification_address_by_id(session: AsyncSession, addressId: int, 
                                            address_definition: 
                                            validations.NotificationAddressBase):
    result = await session.execute(update(models.NotificationAddress).values(
        **address_definition.dict()).where(models.NotificationAddress.id == addressId))
    await session.commit()
    return result.rowcount

async def get_notification_addresses_by_check_id(session: AsyncSession, checkId: int):
    result = await session.execute(select(models.NotificationAddress).filter(
        models.NotificationAddress.checkId == checkId))
    return result.scalars().all()

async def get_latest_results(session: AsyncSession, 
                             urlcontains: str = None) -> list[validations.LatestResult]:
    lastResults = select(models.CheckResult.id, models.CheckResult.checkId, 
                    models.CheckResult.state.label('lastState'), 
                    max(models.CheckResult.timeChecked).label('lastChecked')).group_by(
                        models.CheckResult.checkId).subquery('lastResults')
    query = select(models.CheckDefinition.id, models.CheckDefinition.url, 
                   models.CheckDefinition.frequency, 
                   models.CheckDefinition.expectedStatus, 
                   models.CheckDefinition.expectedString,
                   lastResults.c.lastState, lastResults.c.lastChecked).join(lastResults)
    if urlcontains:
        query = query.filter(models.CheckDefinition.url.contains(urlcontains))
    result = await session.execute(query)
    return result.all()
