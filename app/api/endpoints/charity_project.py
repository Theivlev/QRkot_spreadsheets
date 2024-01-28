from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_closed,
    check_exists,
    check_duplicate,
    check_invested,
    check_full_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectBase,
    CharityProjectData,
    CharityProjectUpdate,
)
from app.services.investition import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectData],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):

    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectData,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
    project: CharityProjectBase,
    session: AsyncSession = Depends(get_async_session),
):
    await check_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await investing(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectData,
    dependencies=[Depends(current_superuser)],
)
async def renew_poject(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):

    project = await check_exists(project_id, session)
    await check_closed(project_id, session)
    if obj_in.full_amount is not None:
        await check_full_amount(
            project_id, obj_in.full_amount, session
        )

    if obj_in.name is not None:
        await check_duplicate(obj_in.name, session)
    await investing(project, session)
    await session.refresh(project)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectData,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_exists(project_id, session)
    await check_invested(project_id, session)

    return await charity_project_crud.remove(charity_project, session)