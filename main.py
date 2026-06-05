from pathlib import Path
from typing import Annotated
from uuid import uuid4

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
            # Get global fields from the first file
            merged_cal.calendar_name = in_cal.calendar_name
            merged_cal.calscale = in_cal.calscale
            merged_cal.version = in_cal.version
            merged_cal.method = in_cal.method
            merged_cal.timezones.extend(in_cal.timezones)
        for ev in in_cal.events:
            if "BYE" in ev.summary:
                # Skip these weeks
                continue
            # Reset some fields
            # uid seems to be identical in all files, so rewrite
            ev.uid = str(uuid4())
            # Rewrite location for Google Calendar to parse
            ev.location = location
            # Clear unneeded fields
            ev.description = None
            ev.organizer = None
            ev.alarms.times.clear()
            # And add it
            merged_cal.add_component(ev.copy(True))
    # print(merged_cal)

    out_file = directory / "merged.ics"
    print(f"Writing to {out_file}")
    out_file.write_bytes(merged_cal.to_ical())


if __name__ == "__main__":
    cli()
