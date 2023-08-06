"""Console script for tasks3."""
import sys
import click

from tasks3 import config

from pkg_resources import iter_entry_points
from click_plugins import with_plugins


@with_plugins(iter_entry_points("click_command_tree"))
@click.group()
@click.option(
    "--db",
    type=click.Path(dir_okay=False, writable=True),
    default=f"{config.DB_BACKEND}:///{config.DB_PATH.absolute()}",
    show_default=True,
    help="Location of tasks database.",
)
@click.version_option()
@click.pass_context
def main(ctx: click.core.Context, db: str):
    """tasks3 is a commandline tool to create and manage tasks and todo lists"""

    ctx.ensure_object(dict)

    ctx.obj["DB"] = db
    return 0


@main.group()
@click.pass_context
def task(ctx: click.core.Context):
    """Manage a task"""
    pass


@task.command()
@click.option(
    "--id",
    type=str,
    help="Filter by id. "
    "You can pass /partial-id/ to search for all tasks whose id contains partial-id.",
)
@click.option("-T", "--title", type=str, help="Search by Title")
@click.option(
    "-u",
    "--urgency",
    type=click.IntRange(min=0, max=4, clamp=True),
    help="Filter by urgency.",
)
@click.option(
    "-i",
    "--importance",
    type=click.IntRange(min=0, max=4, clamp=True),
    help="Filter by importance.",
)
@click.option("-t", "--tags", multiple=True, help="Filter by tags.")
@click.option(
    "-a",
    "--anchor_folder",
    type=click.Path(exists=True, readable=False, file_okay=False, resolve_path=True),
    help="Filter by anchored folder.",
)
@click.option("-d", "--description", type=str, help="Search in description.")
@click.pass_context
def search(
    ctx: click.core.Context,
    id: str,
    title: str,
    urgency: int,
    importance: int,
    tags: list,
    anchor_folder: str,
    description: str,
):
    """Search for tasks"""
    pass


@task.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["YAML"]),
    default="YAML",
    help="Output format.",
    show_default=True,
)
@click.argument("id", type=str)
@click.pass_context
def show(ctx: click.core.Context, format: str, id: str):
    """Show the task in the specified FORMAT

    ID is the id of the Task to be printed.
    """
    pass


@task.command()
@click.option(
    "--yes", default=False, help="Overwrite task data without confirmation?",
)
@click.argument("id", type=str)
@click.pass_context
def edit(ctx: click.core.Context, yes: bool, id: str):
    """Edit a Task

    ID is the id of the Task to be edited.
    """
    pass


@task.command()
@click.option(
    "--yes", default=False, help="Delete task without confirmation?",
)
@click.argument("id", type=str)
@click.pass_context
def remove(ctx: click.core.Context, yes: bool, id: str):
    """Remove a Task

    ID is the id of the Task to be removed.
    """
    pass


@task.command()
@click.option(
    "-T", "--title", default="Give a Title to this Task.", help="Title of the Task."
)
@click.option(
    "-u",
    "--urgency",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    is_flag=True,
    flag_value=4,
    help="Level of urgency of the Task. "
    "Higher the value (max of 4) greater the urgency. "
    "Defaults to 2 when absent and 4 when present.",
)
@click.option(
    "-i",
    "--importance",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    is_flag=True,
    flag_value=4,
    help="Level of importance of the Task. "
    "Higher the value (max of 4) greater the importance. "
    "Defaults to 2 when absent and 4 when present.",
)
@click.option("-t", "--tags", multiple=True, default=[], help="Tags for the Task.")
@click.option(
    "-a",
    "--anchor_folder",
    type=click.Path(exists=True, readable=False, file_okay=False, resolve_path=True),
    help="Anchor the Task to a specified directory or file.",
)
@click.option(
    "-d", "--description", default="", help="A short description of the Task."
)
@click.option(
    "--yes", default=False, help="Create task without confirmation?",
)
@click.pass_context
def add(
    ctx: click.core.Context,
    title: str,
    urgency: int,
    importance: int,
    tags: tuple,
    anchor_folder: str,
    description: str,
    yes: bool,
):
    """Add a new task"""
    pass


@main.group()
@click.pass_context
def db(ctx: click.core.Context):
    """Manage tasks3's database"""
    pass


@db.command()
@click.pass_context
def init(ctx: click.core.Context):
    """Initialize and setup the database"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to purge all tasks?")
@click.pass_context
def purge(ctx: click.core.Context):
    """Purge all tasks from the database"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to drop the database?")
@click.pass_context
def drop(ctx: click.core.Context):
    """Drop the databse"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to move the database?")
@click.argument(
    "dest_db",
    type=click.Path(dir_okay=False, writable=True),
    default=f"{config.DB_BACKEND}:///{config.DB_PATH.absolute()}",
)
@click.pass_context
def move(ctx: click.core.Context, dest_db: str):
    """Move tasks database to DEST_DB

    DEST_DB will be overwriten if it already exists.
    """
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
