import ctypes
import functools
import operator
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from . import vega10_pptable


def label_item(text):
    item = QtGui.QStandardItem(text)
    item.setEditable(False)
    return item


def type_label_item(type):
    item = label_item(type.replace('struct__', 'struct '))
    item.setEnabled(False)
    return item


def build_standard_item(name, obj, edit_func=None):
    name_item = label_item(name)

    if isinstance(obj, ctypes.Structure):
        obj_type = type(obj)

        for field_name, _ in obj_type._fields_:
            name_item.appendRow(build_standard_item(field_name, getattr(obj, field_name),
                                                    functools.partial(setattr, obj, field_name)))

        return [name_item, type_label_item(obj_type.__name__)]

    elif isinstance(obj, ctypes.Array):
        obj_type = type(obj)

        for i in range(len(obj)):
            name_item.appendRow(build_standard_item(f'{name}[{i}]', obj[i],
                                                    functools.partial(operator.setitem, obj, i)))

        return [name_item, type_label_item(f'{obj_type._type_.__name__}[{obj_type._length_}]')]

    else:
        edit_item = QtGui.QStandardItem(str(obj))
        edit_item.setData(edit_func, Model.EditFuncRole)
        return [name_item, edit_item]


class Model(QtGui.QStandardItemModel):
    EditFuncRole = QtCore.Qt.UserRole + 1

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                self.data(index, self.EditFuncRole)(int(value))
            except ValueError:
                return False

        return super().setData(index, value, role)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.buf = None
        self.orig_buf = None
        self.pptables = None

        self.tree = QtWidgets.QTreeView()
        self.setCentralWidget(self.tree)

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

        self.pptables = vega10_pptable.parse(self.buf)
        for name, table in self.pptables._asdict().items():
            model.appendRow(build_standard_item(name, table))

    def revert(self):
        self.buf = bytearray(self.orig_buf)
        self.update_modified_state()
        self.parse()

    def load(self, path):
        with open(path, 'rb') as f:
            self.orig_buf = f.read()

        self.setWindowFilePath(path)
        self.save_dialog.selectFile(path)
        self.revert()

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.buf)

        self.orig_buf = bytearray(self.buf)
        self.setWindowFilePath(path)
        self.open_dialog.selectFile(path)
        self.update_modified_state()


def main():
    app = QtWidgets.QApplication(sys.argv)

    cmdline_parser = QtCore.QCommandLineParser()
    cmdline_parser.addHelpOption()
    cmdline_parser.addPositionalArgument('pptable_file', "Powerplay table file")
    cmdline_parser.process(app)

    win = MainWindow()

    if cmdline_parser.positionalArguments():
        win.load(cmdline_parser.positionalArguments()[0])

    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
