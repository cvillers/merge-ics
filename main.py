from pathlib import Path
from typing import Annotated

from icalendar import Calendar
from typer import Argument, Option, Typer

cli = Typer(name="merge-ics", no_args_is_help=True)

MERGED_FILE = "merged.ics"


@cli.command()
def main(
    directory: Annotated[Path, Argument(help="Directory with input files; output will be written here")],
    location: Annotated[str, Option("-l", "--location", help="New location")],
):
    merged_cal = Calendar()
    for i, in_file in enumerate(directory.glob("*.ics")):
        if in_file.name == MERGED_FILE:
            continue
        print(f"Adding {in_file.name}")
        in_cal = Calendar.from_ical(in_file, False)
        if i == 0:
            merged_cal.calendar_name = in_cal.calendar_name
            merged_cal.calscale = in_cal.calscale
        for ev in in_cal.events:
            ev.location = location
            ev.description = None
            merged_cal.add_component(ev.copy(True))
    print(merged_cal)

    out_file = directory / "merged.ics"
    out_file.write_bytes(merged_cal.to_ical())


if __name__ == "__main__":
    cli()
