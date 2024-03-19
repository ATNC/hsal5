import httpx

from ..database.db import get_db_connection
from ..models.currency import CurrencyData


async def fetch_currency_data() -> CurrencyData:
    async with httpx.AsyncClient() as client:
        response = await client.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/dollar_info?json')
        response.raise_for_status()
        data = response.json()
        return CurrencyData(currency_code='uah', value=data[0]['rate'])


def save_currency_data(currencies_data: CurrencyData):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO '
                     'currency (currency_code, value, date) '
                     'VALUES (?, ?, ?)',
                     (
                         currencies_data.currency_code,
                         currencies_data.value,
                         currencies_data.date
                     ))
        conn.commit()


async def list_currencies() -> list[CurrencyData]:
    with get_db_connection() as conn:
        currencies = conn.execute('SELECT * FROM currency').fetchall()
        return [
            CurrencyData(
                currency_code=row['currency_code'],
                value=row['value'],
                date=row['date']
            ) for row in currencies
        ]
