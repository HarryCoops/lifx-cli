import typer
from configobj import ConfigObj
from lifx.session import Session
from lifx.selector import Selector 
from lifx.model import State 
from lifx import get_color

from pathlib import Path

app = typer.Typer()

def get_session():
    creds_file = Path.home() / ".lifx_cli" / "credentials"
    config = ConfigObj(str(creds_file))
    if "credentials" in config:
        return Session(config["credentials"]["api_key"])

def write_selector(selector_str: str):
    selector_dir = Path.home() / ".lifx_cli"
    if not selector_dir.exists():
        selector_dir.mkdir()
    selector_file = selector_dir / "selector"
    if not selector_file.exists():
        selector_file.touch()
    config = ConfigObj(str(selector_file))
    if "selector" not in config:
        config["selector"] = {}
    config["selector"]["selector_str"] = selector_str
    config.write()

def get_selector() -> Selector:
    session = get_session()
    creds_file = Path.home() / ".lifx_cli" / "selector"
    config = ConfigObj(str(creds_file))
    return Selector(config["selector"]["selector_str"], session)

@app.command()
def authenticate(api_key: str):

    creds_dir = Path.home() / ".lifx_cli"
    if not creds_dir.exists():
        creds_dir.mkdir()
    creds_file = creds_dir / "credentials"
    if not creds_file.exists():
        creds_file.touch()
    config = ConfigObj(str(creds_file))
    if "credentials" not in config:
        config["credentials"] = {}
    config["credentials"]["api_key"] = api_key
    config.write()
    session = Session(api_key)
    typer.echo("Sucessfully authenticated")

@app.command()
def select(selector: str):
    session = get_session()
    selected = Selector(selector, session)
    write_selector(selector)

@app.command()
def set(color: str = ""):
    session = get_session()
    selector = get_selector()
    color_obj = get_color(session, color)
    state = State(color=color_obj)
    selector.set_state(state)

"""
Available commands 

select selector 
set -c color  -b brightness -h hue -s saturation -k kelvin -p power -i infrared -d duration
auth authtoken
effect 
    breathe -c1 from_color -c2 to_color -t period -c cycle -p power -s persist -k peak
    move
    flame 
    pulse
    off 
    cycle ? not sure how this will fit to CLI
list 
    scenes
    lights
    selectors
scene scene_name  
"""

if __name__ == "__main__":
    app()