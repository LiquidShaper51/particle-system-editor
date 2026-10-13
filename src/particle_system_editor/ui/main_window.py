"""Main editor window.

Thin Qt shell: opens files, shows the emitter list, and dispatches
pipeline work to the JobRunner. All heavy lifting lives in services/.
"""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from particle_system_editor.bootstrap.app_context import AppContext


class MainWindow(QMainWindow):
    def __init__(self, ctx: AppContext) -> None:
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("Particle System Editor")
        self.resize(1000, 640)

        central = QWidget()
        layout = QVBoxLayout(central)
        self.status = QLabel("Open a .psys or .emitter file to begin.")
        self.emitter_list = QListWidget()
        open_btn = QPushButton("Open…")
        open_btn.clicked.connect(self._open_file)

        layout.addWidget(open_btn)
        layout.addWidget(self.status)
        layout.addWidget(self.emitter_list)
        self.setCentralWidget(central)

    def _open_file(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Open particle source",
            str(Path.cwd()),
            "Particle sources (*.psys *.emitter)",
        )
        if not path_str:
            return
        result = self.ctx.runner.run_file(Path(path_str))
        self.status.setText(result.summary())
        self.emitter_list.clear()
        if result.ok and result.graph is not None:
            for emitter in result.graph.emitters:
                self.emitter_list.addItem(
                    f"{emitter.name}  ({emitter.shape.value}, {emitter.rate:.0f} p/s)"
                )