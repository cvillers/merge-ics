# merge-ics

Merges iCalendar files into a single file, for ease of import into Google Calendar.

## Usage

Put all `*.ics` files into a directory. The output will be named `merged.ics`.

```bash
uv run python main.py /path/to/files -l "Location Name, 742 Evergreen Terrace, Springfield"
```
