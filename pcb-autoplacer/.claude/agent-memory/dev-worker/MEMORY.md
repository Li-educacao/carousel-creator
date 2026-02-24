# dev-worker Memory — pcb-autoplacer

## Project Structure
- Source: `src/pcb_autoplacer/` (installed as editable in `.venv/`)
- Tests: `tests/` with `tests/fixtures/` for test data files
- Python interpreter: `.venv/bin/python3` (Python 3.12)
- Test runner: `.venv/bin/pytest` (pytest 9.0.2)
- pyproject.toml: `pythonpath = ["src"]` so imports work as `pcb_autoplacer.*`

## Key Modules
- `parsers/sexpr.py` — tokenize/parse/find_nodes/find_node/get_value
- `parsers/netlist.py` — parse_netlist(path) -> (components, nets); filters code=0 nets
- `parsers/footprint.py` — parse_footprint(path) -> FootprintDef; is_smd = has_smd and not has_thru
- `generators/sexpr_writer.py` — serialize(tree) -> str; simple nodes = single line, complex (with sublists) = multiline
- `generators/board_setup.py` — generate_header/general/layers/board_outline; uses JLCPCB config
- `placer/constraints.py` — BBox, check_overlaps(clearance=0.25), check_boundary(margin=0.5)
- `models.py` — dataclasses: Pad, FootprintDef, Component, NetNode, Net, PlacedComponent, BoardConfig
- `cli.py` — typer app with commands: parse, analyze, place, route, drc, export, run

## BoardConfig defaults
- origin_x=100.0, origin_y=100.0, width_mm=50.0, height_mm=50.0, edge_clearance_mm=1.0

## Test Patterns Confirmed
- Fixture files go in `tests/fixtures/`
- KiCad .net netlist: `(export ...)` root, code "0" = unconnected (filtered)
- CLI tests use `typer.testing.CliRunner`; missing file → exit_code != 0
- BBox clearance: `x_max + clearance <= other.x_min` means edges at 5.0 and 5.1 with clearance=0.2 → overlap
