import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QAction,
    QFileDialog,
    QStyle,
    QLabel,
    QComboBox,
    QPushButton
)

from PyQt5.QtGui import QIcon

from plot_widget import PlotWidget


class MainWindow(QMainWindow):
    """Doc String"""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        self.keys = ['Interval (s)', 'V_D (V)', 'V_G (V)']

        exit_icon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton)
        exitAct = QAction(QIcon(exit_icon), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(sys.exit)

        load_icon = self.style().standardIcon(QStyle.SP_DialogOpenButton)
        file_load = QAction(QIcon(load_icon), 'Load Data', self)
        file_load.setShortcut('Ctrl+L')
        file_load.setStatusTip('Load a File')
        file_load.triggered.connect(self.load_new_data)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(file_load)
        fileMenu.addAction(exitAct)

        self.toolbar = self.addToolBar('File Menu')
        self.toolbar.addAction(file_load)
        self.toolbar.addAction(exitAct)

        self.options = dict()
        self.layout.addWidget(self.options_widget())

        self.trace_stack = []

        self.fig, self.ax1 = plt.subplots()
        self.trace1, = self.ax1.plot([], [], marker='o', ls='')
        self.layout.addWidget(PlotWidget(self.fig))

        self.statusBar()
        self.showMaximized()

        self.data = pd.DataFrame()

    def add_trace(self):
        trace, = self.ax1.plot([], [], marker='o', ls='')
        self.trace_stack.append(trace)

    def del_trace(self):
        self.trace_stack.pop()

    def update_trace(self):
        trace = self.trace_stack[-1]

        x_data = self.data[self.options['x_dropdown'].currentText()]
        trace.set_xdata(x_data)
        y_data = self.data[self.options['y_dropdown'].currentText()]
        trace.set_ydata(y_data)

        self.ax1.relim()
        self.ax1.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def options_widget(self):
        option_widget = QWidget(self)
        layout = QHBoxLayout()
        option_widget.setLayout(layout)

        self.options['sort_a_label'] = QLabel('Sort 1')
        self.options['sort_a_dropdown'] = QComboBox()
        self.options['sort_a_dropdown'].addItems(self.keys)

        self.options['sort_b_label'] = QLabel('Sort 2')
        self.options['sort_b_dropdown'] = QComboBox()
        self.options['sort_b_dropdown'].addItems(self.keys)

        self.options['sort_c_label'] = QLabel('Sort 3')
        self.options['sort_c_dropdown'] = QComboBox()
        self.options['sort_c_dropdown'].addItems(self.keys)

        self.options['add_trace_button'] = QPushButton('Add New Trace')
        self.options['add_trace_button'].clicked.connect(self.add_trace)

        self.options['del_trace_button'] = QPushButton('Remove Last Trace')
        self.options['del_trace_button'].clicked.connect(self.del_trace)

        self.options['x_label'] = QLabel('x-axis data')
        self.options['x_dropdown'] = QComboBox()

        self.options['y_label'] = QLabel('y-axis data')
        self.options['y_dropdown'] = QComboBox()

        self.options['plot_button'] = QPushButton('Update Plot')
        self.options['plot_button'].clicked.connect(self.update_trace)

        for value in self.options.values():
            layout.addWidget(value)

        return option_widget

    def load_new_data(self):
        dialog_title = 'Load Data'
        file_filter = "csv (*.csv);;delimited text (*.txt);;All files (*)"
        try:
            data_path = Path(openFileNameDialog(dialog_title, file_filter))
        except TypeError:
            # TypeError is caught because it means no file was selected.
            # User choice, nothing else to do in that case.
            pass
        else:
            data = parse_delimited_file(data_path)
            sort_a = self.options['sort_a_dropdown'].currentText()
            sort_b = self.options['sort_b_dropdown'].currentText()
            sort_c = self.options['sort_c_dropdown'].currentText()
            self.data = data.sort_values([sort_a, sort_b, sort_c])
            self.options['x_dropdown'].addItems(self.data.columns)
            self.options['y_dropdown'].addItems(self.data.columns)


def openFileNameDialog(title, file_filter):
    file_path, _ = QFileDialog.getOpenFileName(None, title, "", file_filter)
    return file_path


def parse_delimited_file(file_name, sep=','):
    return pd.read_csv(file_name, sep=sep)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
