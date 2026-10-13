"""Process entry point for the particle system editor desktop app.

Boots the Qt application, loads user config, registers the default
pipeline (handlers -> processors -> drivers), and hands control to the
main window. Falls back to a headless CLI when ``--headless`` is passed.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import typer

from particle_system_editor.bootstrap.app_context import AppContext
from particle_system_editor.config.settings import load_settings
from particle_system_editor.services.job_runner import JobRunner

log = logging.getLogger("particle_editor")

cli = typer.Typer(add_completion=False, help="Particle system editor.")


def _configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )


@cli.command()
def main(
    source: Path | None = typer.Argument(None, help="Path to a .psys / .emitter file."),
    headless: bool = typer.Option(False, "--headless", help="Run without the GUI."),
    log_level: str = typer.Option("info", "--log-level"),
) -> None:
    """Launch the editor, or run a one-shot pipeline pass headless."""
    _configure_logging(log_level)
    settings = load_settings()
    ctx = AppContext(settings=settings, runner=JobRunner(max_workers=settings.max_workers))

    if headless:
        if source is None:
            log.error("--headless requires a source file")
            raise typer.Exit(code=2)
        result = ctx.runner.run_file(source)
        log.info("pipeline finished: %s", result.summary())
        raise typer.Exit(code=0 if result.ok else 1)

    from particle_system_editor.ui.main_window import MainWindow  # lazy: pulls Qt

    app = MainWindow(ctx)
    sys.exit(app.exec())


if __name__ == "__main__":
    cli()