"""Render DailyBrief to HTML and plain-text via Jinja2."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from sinyra.synthesis.brief import DailyBrief

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=True)


def render_html(brief: DailyBrief) -> str:
    # TODO(P5): implement — render brief.html template
    raise NotImplementedError


def render_text(brief: DailyBrief) -> str:
    # TODO(P5): implement — render brief.txt template
    raise NotImplementedError


def render_preview(output_path: str) -> None:
    # TODO(P5): render with sample data → write to output_path for browser preview
    raise NotImplementedError
