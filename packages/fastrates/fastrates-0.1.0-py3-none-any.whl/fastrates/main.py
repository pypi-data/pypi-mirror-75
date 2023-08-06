import typer
from typer import Option, Typer
import requests

app = Typer()


@app.command()
def main(
    base: str = Option("EUR", help="Base ticker for currency"),
    latest: bool = Option(False, help="Get the latest foreign exchange reference rates"),
    start_at: str = Option(None, help="Get historical rates for any day since start_at"),
    end_at: str = Option(None, help="Get historical rates for any day till end_at"),
    symbols: str = Option(None, help="Compare specific exchange rates"),
    date: str = Option(None, help="Get historical date"),
):
    if start_at and end_at and symbols:
        res = requests.get(
            f"https://fastrates.herokuapp.com/historical?start_at={start_at.upper()}&end_at={end_at.upper()}&base={symbols.upper()}&base={base.upper()}"
        ).json()
        typer.echo(res)

    elif end_at and start_at:
        res = requests.get(
            f"https://fastrates.herokuapp.com/historical?start_at={start_at.upper()}&end_at={end_at.upper()}&base={base.upper()}"
        ).json()
        typer.echo(res)

    elif start_at:
        res = requests.get(
            f"https://fastrates.herokuapp.com/historical?start_at={start_at.upper()}&base={base.upper()}"
        ).json()
        typer.echo(res)

    elif end_at:
        res = requests.get(
            f"https://fastrates.herokuapp.com/historical?end_at={end_at.upper()}&base={base.upper()}"
        ).json()
        typer.echo(res)

    elif date:
        res = requests.get(
            f"https://fastrates.herokuapp.com/historical?date={date}&base={base.upper()}"
        ).json()
        typer.echo(res)

    elif latest:
        res = requests.get(
            f"https://fastrates.herokuapp.com/latest?base={base.upper()}"
        ).json()
        typer.echo(res)


