"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Python JSON:API."""


if __name__ == "__main__":
    main(prog_name="python-jsonapi")  # pragma: no cover
