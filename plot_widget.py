from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as QtCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as QtToolBar

from PyQt5.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout
)


class PlotWidget(QWidget):

    def __init__(self, fig):
        super(PlotWidget, self).__init__()
        self.fig = fig
        layout = QVBoxLayout()
        self.setLayout(layout)

        canvas = QtCanvas(self.fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layouts = {
            'nav_layout': QHBoxLayout(),
            'fig_layout': QVBoxLayout()
        }
        layout.addLayout(layouts['nav_layout'])
        layout.addLayout(layouts['fig_layout'])

        toolbar_widget = QWidget()
        toolbar_widget.setFixedHeight(40)
        toolbar = QtToolBar(canvas, toolbar_widget, coordinates=True)

        layouts['nav_layout'].addWidget(toolbar)
        layouts['fig_layout'].addWidget(canvas)
