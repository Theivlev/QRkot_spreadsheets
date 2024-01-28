from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_duplicate(
    project_name: str,
    session: AsyncSession,
):
    project_id = await charity_project_crud.get_id_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_exists(
    charityproject_id: int,
    session: AsyncSession,
):
    project = await charity_project_crud.get(charityproject_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Проект не найден!'
        )
    return project


async def check_invested(
    project_id: int, session: AsyncSession
):
    invested_project = await charity_project_crud.get_invested_amount(
        project_id, session
    )

    if invested_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_closed(
    project_id: int,
    session: AsyncSession,
):
    project_closed = await charity_project_crud.get_full_invested(
        project_id, session
    )
    if project_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_full_amount(
    project_id: int,
    full_amount: int,
    session: AsyncSession,
):
    invested_amount = await charity_project_crud.get_invested_amount(
        project_id, session
    )
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Значение требуемой суммы не может быть меньше внесённой',
        )
