from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class Donation(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationData(Donation):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]