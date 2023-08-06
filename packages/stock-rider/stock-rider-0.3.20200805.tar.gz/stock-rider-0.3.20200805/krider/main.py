import click

from krider.tasks.historical_data_downloader import historical_data_downloader
from krider.tasks.volume_analysis import volume_analysis_task
from krider.utils.log_helper import init_logger

init_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--period",
    help="Use periods to download data. Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max",
    default="1mo",
    required=False,
)
@click.option(
    "--interval",
    help="Data interval. 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo",
    required=True,
    default="60m",
)
@click.option(
    "--stocks",
    help="Download historical data and fill gaps for provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
def populate_data(interval, period, stocks):
    result = historical_data_downloader.run_with(interval, period, stocks)
    click.echo(result, nl=False)


@cli.command()
@click.option(
    "--period",
    help="Time period. 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max.",
    required=False,
    default="1mo",
)
def latest_data(period):
    click.echo("Loading Latest data for the last {}".format(period))


@cli.command()
@click.option(
    "--period",
    help="Number of entries to use when running volume analysis",
    required=True,
)
@click.option(
    "--stocks", help="Run analysis on provided list of stocks. Eg. MSFT,TSLA,AAPL",
)
def volume_analysis(period, stocks):
    result = volume_analysis_task.run_with(period, stocks)
    click.echo(result, nl=False)
