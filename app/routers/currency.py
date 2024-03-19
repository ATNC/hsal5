import httpx
from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode

from ..services import currency

router = APIRouter()


@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def fetch_and_save_currencies() -> list[AnyComponent]:
    try:
        currency_data = await currency.fetch_currency_data()
        currency.save_currency_data(currency_data)
        currencies = await currency.list_currencies()
    except (httpx.HTTPStatusError, httpx.ConnectError) as e:
        return [
            c.Page(
                components=[
                    c.Heading(text=str(e), level=2),
                ]
            ),
        ]

    return [
        c.Page(
            components=[
                c.Heading(text='Currencies', level=2),
                c.Table(
                    data=currencies,
                    columns=[
                        DisplayLookup(field='currency_code'),
                        DisplayLookup(field='value'),
                        DisplayLookup(field='date', mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]
