import matplotlib  # Based on testing, v 3.1.0 doesn't work. v 3.0.3 is tested to work.
from tkinter.ttk import Combobox, Notebook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


class MainWindow:
    def __init__(self):

        # Buttons
        self.load_button = None
        self.next_meas_button = None
        self.prev_meas_button = None
        self.print_pdf = None

        # Text Fields and Labels
        self.directory_text = None
        self.file_list_label = None
        self.x_axis_label = None
        self.y_axis_one_label = None
        self.y_axis_two_label = None

        # Comboboxes
        self.file_list_combo = None
        self.x_axis_combo = None
        self.y_axis_one_combo = None
        self.y_axis_two_combo = None

        # Graphs
        self.main_fig = None
        self.ax1 = None
        self.canvas1 = None

    def create_ui(self):
        self.create_options_frame()
        self.create_toolbar_frame()


    def create_options_frame(self):
        self.options_frame = tk.Frame(self)
        self.options_frame.pack(side=tk.LEFT, anchor='n', pady=10)
        self.load_button = tk.Button(self.options_frame, text='Select Directory')
        self.load_button.grid(row=0, column=0, padx=(5, 0), pady=2.5)
        self.directory_text = tk.Text(self.options_frame, height=1, width=80)
        self.directory_text.grid(row=0, column=1, padx=(10, 15), pady=2.5, sticky='w')

        file_list_label = tk.Label(self.options_frame, text='Select a file to load: ')
        file_list_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        row1_frame = tk.Frame(master=self.options_frame)
        row1_frame.grid(row=1, column=1, columnspan=5, padx=10, sticky='w')
        self.file_list_combo = Combobox(row1_frame, width=80)
        self.file_list_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.next_meas_button = tk.Button(row1_frame, text='Next file')
        self.next_meas_button.pack(side=tk.RIGHT, padx=(0, 5))
        self.prev_meas_button = tk.Button(row1_frame, text='Previous file')
        self.prev_meas_button.pack(side=tk.RIGHT, padx=(20, 5))

        x_axis_label = tk.Label(self.options_frame, text='Select x-axis data: ')
        x_axis_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        x_axis_frame = tk.Frame(master=self.options_frame)
        x_axis_frame.grid(row=2, column=1, columnspan=5, padx=10, sticky='w')
        self.x_axis_combo = Combobox(x_axis_frame, width=30)
        self.x_axis_combo.pack(side=tk.LEFT, padx=(0, 5))
        x_axis_label_label = tk.Label(x_axis_frame, text='Enter x-axis label: ')
        x_axis_label_label.pack(side=tk.LEFT, padx=(0, 19))
        self.x_axis_label_entry = tk.Entry(x_axis_frame, width=27)
        self.x_axis_label_entry.pack(side=tk.RIGHT, padx=(3, 5), pady=5)

        y_axis_one_label = tk.Label(self.options_frame, text='Select y-axis (1) data: ')
        y_axis_one_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        y_axis_one_frame = tk.Frame(master=self.options_frame)
        y_axis_one_frame.grid(row=3, column=1, columnspan=5, padx=10, sticky='w')
        self.y_axis_one_combo = Combobox(y_axis_one_frame, width=30)
        self.y_axis_one_combo.pack(side=tk.LEFT, padx=(0, 5))
        y_axis_one_label_label = tk.Label(y_axis_one_frame, text='Enter 1-axis (1) label: ')
        y_axis_one_label_label.pack(side=tk.LEFT, padx=(0, 5))
        self.y_axis_one_label_entry = tk.Entry(y_axis_one_frame, width=27)
        self.y_axis_one_label_entry.pack(side=tk.RIGHT, padx=(0, 5), pady=5)

        y_axis_two_label = tk.Label(self.options_frame, text='Select y-axis (2) data: ')
        y_axis_two_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        y_axis_two_frame = tk.Frame(master=self.options_frame)
        y_axis_two_frame.grid(row=4, column=1, columnspan=5, padx=10, sticky='w')
        self.y_axis_two_combo = Combobox(y_axis_two_frame, width=30)
        self.y_axis_two_combo.pack(side=tk.LEFT, padx=(0, 5))
        y_axis_two_label_label = tk.Label(y_axis_two_frame, text='Enter y-axis (2) label: ')
        y_axis_two_label_label.pack(side=tk.LEFT, padx=(0, 5))
        self.y_axis_two_label_entry = tk.Entry(y_axis_two_frame, width=27)
        self.y_axis_two_label_entry.pack(side=tk.RIGHT, padx=(0, 5), pady=5)

        set_title_label = tk.Label(self.options_frame, text='Set title text: ')
        set_title_label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky='w')
        self.set_title_entry = tk.Entry(self.options_frame, width=82)
        self.set_title_entry.grid(row=5, column=1, columnspan=5, padx=10, sticky='w')

        self.plot_button = tk.Button(self.options_frame, text='Plot', width=(80))
        self.plot_button.grid(row=6, column=0, columnspan=2, pady=10)

        nb = Notebook(self.options_frame)
        nb.grid(row=7, column=0, columnspan=2)
        more_options_frame = tk.Frame(nb, width=10)
        curve_fit_frame = tk.Frame(nb, width=10)
        nb.add(more_options_frame, text='Graph Options')
        nb.add(curve_fit_frame, text='Curve Fit Options')

        range_frame = tk.Frame(more_options_frame, borderwidth=1, relief=tk.GROOVE)
        range_frame.pack()

        self.retain_range = tk.IntVar(value=1)
        self.retain_range_button = tk.Checkbutton(range_frame, text="Use default limits.",
                                                  variable=self.retain_range, padx=5, pady=5)
        self.retain_range_button.grid(row=0, column=0, pady=5, sticky='w')

        set_xmin_range_label = tk.Label(range_frame, text='Set min x value: ')
        set_xmin_range_label.grid(row=1, column=0, pady=5, sticky='w')
        self.set_xmin_range_entry = tk.Entry(range_frame, width=10)
        self.set_xmin_range_entry.grid(row=1, column=1, padx=10, sticky='w')
        set_xmax_range_label = tk.Label(range_frame, text='Set max x value: ')
        set_xmax_range_label.grid(row=2, column=0, pady=5, sticky='w')
        self.set_xmax_range_entry = tk.Entry(range_frame, width=10)
        self.set_xmax_range_entry.grid(row=2, column=1, padx=10, sticky='w')
        self.reset_xrange_button = tk.Button(range_frame, text='Reset x limits')
        self.reset_xrange_button.grid(row=3, column=0, sticky='w')

        set_y1min_range_label = tk.Label(range_frame, text='Set min y1 value: ')
        set_y1min_range_label.grid(row=1, column=2, pady=5, sticky='w')
        self.set_y1min_range_entry = tk.Entry(range_frame, width=10)
        self.set_y1min_range_entry.grid(row=1, column=3, padx=10, sticky='w')
        set_y1max_range_label = tk.Label(range_frame, text='Set max y1 value: ')
        set_y1max_range_label.grid(row=2, column=2, pady=5, sticky='w')
        self.set_y1max_range_entry = tk.Entry(range_frame, width=10)
        self.set_y1max_range_entry.grid(row=2, column=3, padx=10, sticky='w')
        self.reset_y1range_button = tk.Button(range_frame, text='Reset y1 limits')
        self.reset_y1range_button.grid(row=3, column=2, sticky='w')

        set_y2min_range_label = tk.Label(range_frame, text='Set min y2 value: ')
        set_y2min_range_label.grid(row=1, column=4, pady=5, sticky='w')
        self.set_y2min_range_entry = tk.Entry(range_frame, width=10)
        self.set_y2min_range_entry.grid(row=1, column=5, padx=10, sticky='w')
        set_y2max_range_label = tk.Label(range_frame, text='Set max y2 value: ')
        set_y2max_range_label.grid(row=2, column=4, pady=5, sticky='w')
        self.set_y2max_range_entry = tk.Entry(range_frame, width=10)
        self.set_y2max_range_entry.grid(row=2, column=5, padx=10, sticky='w')
        self.reset_y2range_button = tk.Button(range_frame, text='Reset y2 limits')
        self.reset_y2range_button.grid(row=3, column=4, sticky='w')

        normalize_frame = tk.Frame(more_options_frame, borderwidth=1, relief=tk.GROOVE)
        normalize_frame.pack()
        normalize_label = tk.Label(normalize_frame, text='Normalize data to: ')
        normalize_label.pack(side=tk.LEFT)
        self.normalize_entry = tk.Entry(normalize_frame)
        self.normalize_entry.pack(side=tk.LEFT)
        self.normalize_button = tk.Button(normalize_frame, text='Reset normalization')
        self.normalize_button.pack(side=tk.LEFT)






    def create_toolbar_frame(self):
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(side=tk.LEFT)

        self.save_fig_button = tk.Button(master=self.graph_frame, text='Save Figure')
        self.save_fig_button.grid(row=2, column=0, sticky='w', padx=10)
        toolbar_frame = tk.Frame(master=self.graph_frame)
        toolbar_frame.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)

        self.main_fig, self.ax1 = plt.subplots(1, 1, figsize=(8, 6), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.main_fig, master=self.graph_frame)
        toolbar1 = NavigationToolbar2Tk(self.canvas1, toolbar_frame)
        toolbar1.update()
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=3, column=0, columnspan=4, padx=0)



