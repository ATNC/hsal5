import datetime

from pydantic import BaseModel, Field


class CurrencyData(BaseModel):
    currency_code: str = Field(..., description='Currency code')
    value: float = Field(..., gt=0, description='Currency value')
    date: datetime.date = Field(default_factory=datetime.date.today)
