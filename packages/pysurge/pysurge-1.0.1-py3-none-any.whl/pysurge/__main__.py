import logging

import click

from .config import load_config
from .pysurge import Manager


log = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c", "--config", required=True, type=click.Path(exists=True), help="Path to config file"
)
@click.option(
    "-d", "--duration", type=int, help="Time in minutes to run (default: indefinite, until ctrl+C)"
)
@click.option("--debug", is_flag=True, default=False, help="Enable debug logging")
def main(config, duration, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(processName)s %(threadName)s %(levelname)s %(message)s",
    )

    config_data = load_config(click.format_filename(config))
    if duration:
        log.info("Running for %d minutes...", duration)
    else:
        log.info("Running indefinitely...")
    log.info("Hit CTRL+C to trigger end of run")
    manager = Manager(config=config_data, duration=duration * 60 if duration else None, debug=debug)
    manager.start()


if __name__ == "__main__":
    main()
