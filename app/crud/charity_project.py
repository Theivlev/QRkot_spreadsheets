from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_id_name(
        self,
        name: str,
        session: AsyncSession,
    ):
        project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_invested_amount(
        self,
        charity_id: int,
        session: AsyncSession,
    ):
        project_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == charity_id
            )
        )
        return project_invested_amount.scalars().first()

    async def get_full_invested(
        self,
        charity_id: int,
        session: AsyncSession,
    ):
        full_invested = await session.execute(
            select(CharityProject.fully_invested).where(
                CharityProject.id == charity_id
            )
        )
        return full_invested.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict]:
        projects = await session.execute(
            select(
                CharityProject.name,
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date),
                CharityProject.description).where(
                    CharityProject.fully_invested == 1
            ).order_by(CharityProject.close_date - CharityProject.create_date)
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
