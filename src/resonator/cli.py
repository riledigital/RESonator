from resonator import RESonator
import click
import pathlib


@click.command()
# @click.option("--lms", help="Path to lms file")
# @click.option("--eval", help="Path to evaluation data")
# @click.option("--meta", help="Path to metadata toml")
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
def process_input(lms, meta, eval, out):
    RESonator.RESonator(lms, meta, eval, out)
    return out


def validate_submission(submission):
    return RESonator.validate_file(submission)


if __name__ == "__main__":
    process_input()
