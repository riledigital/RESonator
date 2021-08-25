from resonator.RESonator import RESonator
import logging
import click
import pathlib

logging.basicConfig(level=logging.INFO)


@click.group()
@click.version_option(prog_name="RESonator CLI")
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
def process_job(
    lms: pathlib.Path, meta: pathlib.Path, eval: pathlib.Path, out: pathlib.Path
) -> pathlib.Path:
    """Process a RES job using inputs.

    Args:
        lms (pathlib.Path): CSV file for LMS data
        meta (pathlib.Path): TOML file for job metadata
        eval (pathlib.Path): XLSX file for Qualtrics
        out (pathlib.Path): File to output to

    Returns:
        pathlib.Path: File output
    """
    RESonator.process_job(lms, meta, eval, out)
    click.echo(f"Output written to {out}")
    return out


@click.command()
@click.argument(
    "test_file",
    type=click.Path(exists=True, dir_okay=False, path_type=str, resolve_path=True),
)
def validate_submission(test_file):
    """Validate a RES submission against `submission.dtd`.

    Args:
        test_file (pathlib.Path): Path to the file to validate.

    Returns:
        int: Returns 0 if passed, -1 if failed.
    """
    result = RESonator.validate_file(test_file)
    if result is True:
        logging.info("DTD Validation passed.")
        click.echo(0)
    else:
        logging.info("DTD Validation failed. See log for specific errors.")
        click.echo(-1)
        return result


cli.add_command(process_job)
cli.add_command(validate_submission)

if __name__ == "__main__":
    cli()
