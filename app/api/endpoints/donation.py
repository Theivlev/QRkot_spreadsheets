from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, Donation, DonationData
from app.services.investition import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationData],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[Donation],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_donations(user=user, session=session)


@router.post(
    '/',
    response_model=Donation,
    response_model_exclude_none=True)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    await investing(new_donation, session)
    await session.refresh(new_donation)
    return new_donation