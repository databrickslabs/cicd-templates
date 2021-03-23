# platform independent profile configurator
import click
from databricks_cli.configure.cli import DatabricksConfig, update_and_persist_config


@click.command()
@click.option("--profile", required=True, type=str)
@click.option("--host", required=True, type=str)
@click.option("--token", required=True, type=str)
def configure(profile: str, host: str, token: str):
    new_config = DatabricksConfig.from_token(host, token, False)
    update_and_persist_config(profile, new_config)


if __name__ == "__main__":
    configure()
