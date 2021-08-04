from resonator.RESonator import RESonator
import logging
import click
import pathlib

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@click.command()
@click.argument(
    "lms",
    type=click.Path(
        exists=True, dir_okay=False, path_type=pathlib.Path, resolve_path=True
    ),
)
@click.argument(
    "eval",
    type=click.Path(
        exists=True, dir_okay=False, path_type=pathlib.Path, resolve_path=True
    ),
)
@click.argument(
    "meta",
    type=click.Path(
        exists=True, dir_okay=False, path_type=pathlib.Path, resolve_path=True
    ),
)
@click.argument(
    "out",
    type=click.Path(
        exists=False, dir_okay=False, path_type=pathlib.Path, resolve_path=True
    ),
)
def process_job(lms, meta, eval, out):
    RESonator.process_job(lms, meta, eval, out)
    click.echo(f"Output written to {out}")


@click.command()
@click.argument(
    "test_file",
    type=click.Path(exists=True, dir_okay=False, path_type=str, resolve_path=True),
)
def validate_submission(test_file):
    result = RESonator.validate_file(test_file)
    if result is True:
        logging.info("DTD Validation passed.")
    else:
        logging.info("DTD Validation failed. See log for specific errors.")
    click.echo(result)
    return result


cli.add_command(process_job)
cli.add_command(validate_submission)

# if __name__ == "__main__":
#     process_input()
