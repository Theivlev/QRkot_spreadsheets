from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
):

    if isinstance(obj_in, Donation):
        invested_model = CharityProject
    else:
        invested_model = Donation
    not_invested = await get_not_invested(
        invested_model, session
    )

    if not_invested:
        total_available_amount = obj_in.full_amount
        for obj in not_invested:
            remaining_amount = obj.full_amount - obj.invested_amount
            investment = min(remaining_amount, total_available_amount)
            total_available_amount -= investment
            obj.invested_amount += investment
            obj_in.invested_amount += investment

            if obj.full_amount == obj.invested_amount:
                close_invested(obj)

            if not total_available_amount:
                close_invested(obj_in)
                break
        await session.commit()

    return obj_in


async def get_not_invested(
    model: Union[CharityProject, Donation], session: AsyncSession
):
    objects = await session.execute(
        select(model)
        .where(model.invested_amount < model.full_amount)
        .order_by(model.create_date)
    )
    return objects.scalars().all()


def close_invested(
        obj: Union[CharityProject, Donation],
):
    obj.fully_invested = True
    obj.close_date = datetime.now()