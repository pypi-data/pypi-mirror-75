import sys
import traceback
from pathlib import Path

import chardet
from pkg_resources import resource_filename
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot

from . import qt_margin_fix  # noqa
from .process import SubFix


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(resource_filename(__name__, "error.ui"), self)


class SubFixWorker(QObject):
    """
    Background worker thread that processes the file (to avoid
    freezing up the user interface.)
    """

    # https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt
    subfix: SubFix = None
    input_path: Path = None
    input_encoding: str = None
    output_path: Path = None
    output_encoding: str = None
    line_span = None

    finished = Signal()
    progress = Signal(int)

    @Slot()
    def run(self):
        num_lines = 0
        with open(self.input_path, "rt", encoding=self.input_encoding) as file:
            for _ in file:
                num_lines += 1

        min_line, max_line = self.line_span

        with open(self.input_path, "rt", encoding=self.input_encoding) as file:
            with open(
                self.output_path, "wt", encoding=self.output_encoding
            ) as wfile:
                for i, line in enumerate(file):
                    if min_line <= i <= max_line:
                        replaced = self.subfix.substitute(line)
                    else:
                        replaced = line

                    wfile.write(replaced)

                    if i % 50 == 0:
                        self.progress.emit(min(100, round(i * 100 / num_lines)))

        self.progress.emit(100)
        self.finished.emit()

    def setup_thread(self, thread):
        self.moveToThread(thread)
        self.finished.connect(thread.quit)
        thread.started.connect(self.run)


class MainWindow(QtWidgets.QMainWindow):
    _subfix = None
    dictionary_file_mtime = None
    dictionary_file_path = None
    autodetected_input_encoding = "iso-8859-2"

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(resource_filename(__name__, "main.ui"), self)
        self.button_input_file.clicked.connect(self._select_input_file)

        self.combo_encoding_list = [None, "utf-8", "iso-8859-2"]
        self.combo_encoding.addItems(
            ["Autodetect"] + self.combo_encoding_list[1:]
        )

        self.menuaction_load_dictionary_file.triggered.connect(
            self._select_dictionary_file
        )

        self.exp_textbox_before.textChanged.connect(self._exp_update)

        self.button_process.clicked.connect(self._process_pre_start)

    @property
    def input_path(self):
        path = Path(self.line_input_file.text())
        return path if path.is_file() else None

    def _select_input_file(self):
        self._dialog = dlg = QtWidgets.QFileDialog(parent=self)
        dlg.setModal(True)
        dlg.open(self._select_input_file_done)

    def _select_input_file_done(self):
        self.line_input_file.setText(self._dialog.selectedFiles()[0])
        self.autodetect_input_encoding()

    def autodetect_input_encoding(self):
        if not self.input_path:
            return

        try:
            with open(self.input_path, "rb") as file:
                encoding = chardet.detect(file.read(1024 * 1024))["encoding"]
        except Exception:
            encoding = None

        if encoding != "utf-8":
            encoding = "iso-8859-2"

        self.autodetected_input_encoding = encoding
        self.combo_encoding.setItemText(0, f"Autodetect ({encoding})")

    @property
    def input_encoding(self):
        encoding = self.combo_encoding_list[self.combo_encoding.currentIndex()]

        if encoding is None:
            encoding = self.autodetected_input_encoding

        return encoding

    def _select_dictionary_file(self):
        self._dialog = dlg = QtWidgets.QFileDialog(parent=self)
        dlg.setModal(True)
        dlg.open(self._select_dictionary_file_done)

    def _select_dictionary_file_done(self):
        self.dictionary_file_path = Path(self._dialog.selectedFiles()[0])
        self.line_dictionary_file.setText(str(self.dictionary_file_path))
        self.get_subfix_qt()  # try to load dictionary, or raise exception

    def _exp_update(self):
        sf = self.get_subfix_qt()
        if sf is None:
            return

        before = self.exp_textbox_before.toPlainText()

        try:
            after = sf.substitute(before)
        except Exception as exc:
            self._open_error_dialog(exc)

        self.exp_textbox_after.setPlainText(after)

    def _open_error_dialog(self, exc):
        self._error_dialog = dlg = ErrorDialog(parent=self)
        dlg.text_message.setPlainText(
            "".join(traceback.format_exception(None, exc, exc.__traceback__))
        )
        dlg.setModal(True)
        dlg.show()

    def get_subfix_qt(self):
        try:
            return self.get_subfix()
        except Exception as exc:
            self._open_error_dialog(exc)
            return None

    def get_subfix(self):
        path = self.dictionary_file_path

        if path is None:
            raise RuntimeError("dictionary file path is not set")

        if not path.is_file():
            raise RuntimeError(f"no file {path}")

        # reload if file modification time changed
        mtime = path.stat().st_mtime
        if mtime != self.dictionary_file_mtime:
            self.dictionary_file_mtime = mtime
            self._subfix = None

        if self._subfix is None:
            self._subfix = SubFix(path)

        return self._subfix

    def _process_pre_start(self):
        self._dialog = dlg = QtWidgets.QFileDialog(parent=self)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setModal(True)
        dlg.open(self._process_start)

    def _process_start(self):
        output_path = Path(self._dialog.selectedFiles()[0])

        sf = self.get_subfix_qt()
        try:
            input_path = self.input_path
            if input_path is None:
                raise RuntimeError("input file not set")

            line_span_str = self.line_file_lines.text().strip()
            if not line_span_str:
                line_span = (1, float("inf"))
            try:
                line_start, _, line_end = line_span_str.partition("-")
                line_span = (int(line_start) - 1, int(line_end))
            except Exception as exc:
                raise RuntimeError(
                    f"invalid line span {line_span_str!r}; must "
                    f'be "17-30" for example'
                ) from exc

        except Exception as exc:
            self._open_error_dialog(exc)
            return

        input_encoding = output_encoding = self.input_encoding

        self._worker = worker = SubFixWorker()
        worker.subfix = sf
        worker.input_path = input_path
        worker.input_encoding = input_encoding
        worker.output_path = output_path
        worker.output_encoding = input_encoding
        worker.line_span = line_span

        self._worker_thread = thread = QThread()
        worker.progress.connect(self._process_update_progress)
        worker.finished.connect(self._process_finished)
        worker.setup_thread(thread)

        thread.start()
        self.button_process.setEnabled(False)

    def _process_finished(self):
        self.button_process.setEnabled(True)

    def _process_update_progress(self, value):
        self.progressbar_process.setValue(value)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
