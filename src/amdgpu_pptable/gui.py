import collections.abc
import ctypes
import enum
import functools
import operator
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

from . import version_detect, version


def fancy_type_name(obj_type):
    if hasattr(obj_type, 'wrapped_type'):
        return fancy_type_name(obj_type.wrapped_type)

    if issubclass(obj_type, ctypes.Array):
        return f'{obj_type._type_.__name__}[{obj_type._length_}]'

    return obj_type.__name__


def type_label_item(type):
    item = QtGui.QStandardItem(fancy_type_name(type))
    item.setEnabled(False)
    return item


def build_standard_item(name, obj, edit_func=None):
    name_item = QtGui.QStandardItem(name)

    if isinstance(obj, collections.abc.MutableMapping):
        for key, value in obj.items():
            if isinstance(key, enum.Enum):
                field_name = key.name
            else:
                field_name = key

            name_item.appendRow(build_standard_item(f'{name}[{field_name}]', value,
                                                    functools.partial(operator.setitem, obj, key)))

        return [name_item, type_label_item(type(obj))]

    elif isinstance(obj, ctypes.Structure):
        obj_type = type(obj)

        for field_name, _ in obj_type._fields_:
            name_item.appendRow(build_standard_item(field_name, getattr(obj, field_name),
                                                    functools.partial(setattr, obj, field_name)))

        return [name_item, type_label_item(obj_type)]

    elif isinstance(obj, ctypes.Array):
        for i in range(len(obj)):
            name_item.appendRow(build_standard_item(f'{name}[{i}]', obj[i],
                                                    functools.partial(operator.setitem, obj, i)))

        return [name_item, type_label_item(type(obj))]

    else:
        edit_item = QtGui.QStandardItem(str(obj))
        edit_item.setData(edit_func, Model.EditFuncRole)
        edit_item.setData(type(obj), Model.TypeRole)
        return [name_item, edit_item]


class Model(QtGui.QStandardItemModel):
    EditFuncRole = QtCore.Qt.UserRole + 1
    TypeRole = EditFuncRole + 1

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                target_type = self.data(index, self.TypeRole)
                edit_func = self.data(index, self.EditFuncRole)
                edit_func(target_type(value))
            except ValueError:
                return False

        return super().setData(index, value, role)

    def buddy(self, index):
        return index.siblingAtColumn(1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.buf = None
        self.orig_buf = None
        self.pptables = None

        self.tree = QtWidgets.QTreeView()
        self.setCentralWidget(self.tree)
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(True)
        self.tree.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        self.open_dialog = QtWidgets.QFileDialog()
        self.open_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.open_dialog.fileSelected.connect(self.load)

        self.save_dialog = QtWidgets.QFileDialog()
        self.save_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        self.save_dialog.fileSelected.connect(self.save)

        toolbar = QtWidgets.QToolBar()
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(QtGui.QIcon.fromTheme('document-open'), "Load", self.open_dialog.show).setShortcuts(QtGui.QKeySequence.Open)
        toolbar.addAction(QtGui.QIcon.fromTheme('document-save'), "Save", self.save_dialog.show).setShortcuts(QtGui.QKeySequence.Save)
        toolbar.addAction(QtGui.QIcon.fromTheme('edit-undo'), "Revert", self.revert)
        toolbar.addAction(QtGui.QIcon.fromTheme('view-refresh'), "Reparse", self.parse).setShortcuts(QtGui.QKeySequence.Refresh)
        self.addToolBar(toolbar)

    def update_modified_state(self):
        self.setWindowModified(self.buf != self.orig_buf)

    def parse(self):
        model = Model()
        model.setHorizontalHeaderLabels(["Field", "Value"])
        model.itemChanged.connect(lambda _: self.update_modified_state())
        self.tree.setModel(model)
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.pptables = version_detect.parse(self.buf)
        for name, table in self.pptables._asdict().items():
            model.appendRow(build_standard_item(name, table))

    def revert(self):
        self.buf = bytearray(self.orig_buf)
        self.update_modified_state()
        self.parse()

    def error_message(self, message):
        QtWidgets.QMessageBox.critical(
            self, message, f"{message}: {traceback.format_exc()}"
        )

    def load(self, path):
        try:
            with open(path, 'rb') as f:
                self.orig_buf = f.read()

            self.setWindowFilePath(path)
            self.save_dialog.selectFile(path)
            self.revert()

        except Exception:
            self.error_message(f"Can't load {path!r}")

    def save(self, path):
        try:
            with open(path, 'wb') as f:
                f.write(self.buf)

            self.orig_buf = bytearray(self.buf)
            self.setWindowFilePath(path)
            self.open_dialog.selectFile(path)
            self.update_modified_state()

        except Exception:
            self.error_message(f"Can't write to {path!r}")


def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationVersion(version.version)

    cmdline_parser = QtCore.QCommandLineParser()
    cmdline_parser.addHelpOption()
    cmdline_parser.addVersionOption()
    cmdline_parser.addPositionalArgument('pptable_file', "Powerplay table file")
    cmdline_parser.process(app)

    win = MainWindow()

    if cmdline_parser.positionalArguments():
        win.load(cmdline_parser.positionalArguments()[0])

    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
