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
        self.print_pdf_button = None

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

        # Widgets to get x-axis title
        x_axis_label = tk.Label(self.options_frame, text='X-Axis Title: ')
        x_axis_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.x_axis_title_entry = tk.Entry(self.options_frame, width=30)
        self.x_axis_title_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        # Widgets to select x-axis data
        x_axis_label = tk.Label(self.options_frame, text='Select x-axis data: ')
        x_axis_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.x_axis_combo = Combobox(self.options_frame, width=30)
        self.x_axis_combo.grid(row=3, column=1, columnspan=5, padx=10, sticky='w')

        # Widgets to get y-axis (1) title
        y_axis_one_label = tk.Label(self.options_frame, text='Y-Axis (1) Title: ')
        y_axis_one_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y1_axis_title_entry = tk.Entry(self.options_frame, width=30)
        self.y1_axis_title_entry.grid(row=4, column=1, padx=(10, 0), pady=5, sticky='w')

        # Widgets to select y-axis (1) data and set label for legend
        y_axis_one_label = tk.Label(self.options_frame, text='Select y-axis (1) data: ')
        y_axis_one_label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky='w')
        y_axis_one_frame = tk.Frame(master=self.options_frame)
        y_axis_one_frame.grid(row=5, column=1, columnspan=5, padx=10, sticky='w')
        self.y_axis_one_combo = Combobox(y_axis_one_frame, width=30)
        self.y_axis_one_combo.pack(side=tk.LEFT, padx=(0, 5))
        y_axis_one_label_label = tk.Label(y_axis_one_frame, text='Enter Y-axis (1) label: ')
        y_axis_one_label_label.pack(side=tk.LEFT, padx=(0, 5))
        self.y1_legend_entry = tk.Entry(y_axis_one_frame, width=27)
        self.y1_legend_entry.pack(side=tk.RIGHT, padx=(0, 5), pady=5)

        # Widgets to get y-axis (1) title
        y_axis_two_label = tk.Label(self.options_frame, text='Y-Axis (2) Title: ')
        y_axis_two_label.grid(row=6, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y2_axis_title_entry = tk.Entry(self.options_frame, width=30)
        self.y2_axis_title_entry.grid(row=6, column=1, padx=(10, 0), pady=5, sticky='w')

        # Widgets to select y-axis (2) data and set label for legend
        y_axis_two_label = tk.Label(self.options_frame, text='Select y-axis (2) data: ')
        y_axis_two_label.grid(row=7, column=0, padx=(10, 0), pady=5, sticky='w')
        y_axis_two_frame = tk.Frame(master=self.options_frame)
        y_axis_two_frame.grid(row=7, column=1, columnspan=5, padx=10, sticky='w')
        self.y_axis_two_combo = Combobox(y_axis_two_frame, width=30)
        self.y_axis_two_combo.pack(side=tk.LEFT, padx=(0, 5))
        y_axis_two_label_label = tk.Label(y_axis_two_frame, text='Enter y-axis (2) label: ')
        y_axis_two_label_label.pack(side=tk.LEFT, padx=(0, 5))
        self.y2_legend_entry = tk.Entry(y_axis_two_frame, width=27)
        self.y2_legend_entry.pack(side=tk.RIGHT, padx=(0, 5), pady=5)

        # Widgets to get chart title
        set_title_label = tk.Label(self.options_frame, text='Set title text: ')
        set_title_label.grid(row=8, column=0, padx=(10, 0), pady=5, sticky='w')
        self.set_title_entry = tk.Entry(self.options_frame, width=82)
        self.set_title_entry.grid(row=8, column=1, columnspan=5, padx=10, sticky='w')

        self.plot_button = tk.Button(self.options_frame, text='Plot', width=(80))
        self.plot_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.nb = Notebook(self.options_frame)
        self.nb.grid(row=10, column=0, columnspan=2)
        self.graph_options_tab()
        self.font_options_tab()
        self.y1_subplot_tab()
        # self.x_axis_options_tab()
        self.y1_axis_options_tab()
        self.y2_axis_options_tab()

    def graph_options_tab(self):
        more_options_frame = tk.Frame(self.nb, width=10)
        self.nb.add(more_options_frame, text='Graph Options')

        self.retain_range = tk.IntVar(value=1)
        self.retain_range_button = tk.Checkbutton(more_options_frame, text="Use default limits.",
                                                  variable=self.retain_range)
        self.retain_range_button.grid(row=0, column=0, columnspan=2, sticky='w', padx=(10, 0), pady=5)

        set_xmin_range_label = tk.Label(more_options_frame, text='Set min x value: ')
        set_xmin_range_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        self.set_xmin_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_xmin_range_entry.grid(row=1, column=1, padx=(10, 0), sticky='w')
        set_xmax_range_label = tk.Label(more_options_frame, text='Set max x value: ')
        set_xmax_range_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.set_xmax_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_xmax_range_entry.grid(row=2, column=1, padx=(10, 0), sticky='w')
        self.reset_xrange_button = tk.Button(more_options_frame, text='Reset x limits')
        self.reset_xrange_button.grid(row=3, column=0, padx=(10, 0), sticky='w')

        set_y1min_range_label = tk.Label(more_options_frame, text='Set min y1 value: ')
        set_y1min_range_label.grid(row=1, column=2, padx=(10, 0), sticky='w')
        self.set_y1min_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_y1min_range_entry.grid(row=1, column=3, padx=(10, 0), sticky='w')
        set_y1max_range_label = tk.Label(more_options_frame, text='Set max y1 value: ')
        set_y1max_range_label.grid(row=2, column=2, padx=(10, 0), sticky='w')
        self.set_y1max_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_y1max_range_entry.grid(row=2, column=3, padx=(10, 0), sticky='w')
        self.reset_y1range_button = tk.Button(more_options_frame, text='Reset y1 limits')
        self.reset_y1range_button.grid(row=3, column=2, padx=(10, 0), sticky='w')

        set_y2min_range_label = tk.Label(more_options_frame, text='Set min y2 value: ')
        set_y2min_range_label.grid(row=1, column=4, padx=(10, 0), sticky='w')
        self.set_y2min_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_y2min_range_entry.grid(row=1, column=5, padx=(10, 0), sticky='w')
        set_y2max_range_label = tk.Label(more_options_frame, text='Set max y2 value: ')
        set_y2max_range_label.grid(row=2, column=4, padx=(10, 0), sticky='w')
        self.set_y2max_range_entry = tk.Entry(more_options_frame, width=10)
        self.set_y2max_range_entry.grid(row=2, column=5, padx=(10, 0), sticky='w')
        self.reset_y2range_button = tk.Button(more_options_frame, text='Reset y2 limits')
        self.reset_y2range_button.grid(row=3, column=4, padx=(10, 0), sticky='w')

    def y1_subplot_tab(self):
        y1_subplot_frame = tk.Frame(self.nb, width=10)
        self.nb.add(y1_subplot_frame, text='Y-Axis (1) Subplots')

        subplot1_label = tk.Label(y1_subplot_frame, text='Select subplot 1 data: ')
        subplot1_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky='w')
        self.subplot1_combo = Combobox(y1_subplot_frame, width=30)
        self.subplot1_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')

        subplot1_label = tk.Label(y1_subplot_frame, text='Label: ')
        subplot1_label.grid(row=0, column=2, padx=(10, 0), pady=5, sticky='w')
        self.subplot1_entry = tk.Entry(y1_subplot_frame, width=30)
        self.subplot1_entry.grid(row=0, column=3, padx=(10, 0), pady=5, sticky='w')

        subplot2_label = tk.Label(y1_subplot_frame, text='Select subplot 2 data: ')
        subplot2_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        self.subplot2_combo = Combobox(y1_subplot_frame, width=30)
        self.subplot2_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')

        subplot2_label = tk.Label(y1_subplot_frame, text='Label: ')
        subplot2_label.grid(row=1, column=2, padx=(10, 0), pady=5, sticky='w')
        self.subplot2_entry = tk.Entry(y1_subplot_frame, width=30)
        self.subplot2_entry.grid(row=1, column=3, padx=(10, 0), pady=5, sticky='w')

        subplot3_label = tk.Label(y1_subplot_frame, text='Select subplot 3 data: ')
        subplot3_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.subplot3_combo = Combobox(y1_subplot_frame, width=30)
        self.subplot3_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        subplot3_label = tk.Label(y1_subplot_frame, text='Label: ')
        subplot3_label.grid(row=2, column=2, padx=(10, 0), pady=5, sticky='w')
        self.subplot3_entry = tk.Entry(y1_subplot_frame, width=30)
        self.subplot3_entry.grid(row=2, column=3, padx=(10, 0), pady=5, sticky='w')

        subplot4_label = tk.Label(y1_subplot_frame, text='Select subplot 4 data: ')
        subplot4_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.subplot4_combo = Combobox(y1_subplot_frame, width=30)
        self.subplot4_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky='w')

        subplot4_label = tk.Label(y1_subplot_frame, text='Label: ')
        subplot4_label.grid(row=3, column=2, padx=(10, 0), pady=5, sticky='w')
        self.subplot4_entry = tk.Entry(y1_subplot_frame, width=30)
        self.subplot4_entry.grid(row=3, column=3, padx=(10, 0), pady=5, sticky='w')

    def curve_fit_options_tab(self):
        curve_fit_frame = tk.Frame(self.nb, width=10)
        self.nb.add(curve_fit_frame, text='Curve Fit Options')

    def x_axis_options_tab(self):
        x_options_frame = tk.Frame(self.nb)
        self.nb.add(x_options_frame, text='x-axis options')

    def y1_axis_options_tab(self):
        y1_options_frame = tk.Frame(self.nb)
        self.nb.add(y1_options_frame, text='Y-Axis (1) Options')

        normalize_label = tk.Label(y1_options_frame, text='Normalize data to: ')
        normalize_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky='w')
        self.normalize_entry = tk.Entry(y1_options_frame)
        self.normalize_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        self.normalize_button = tk.Button(y1_options_frame, text='Reset normalization')
        self.normalize_button.grid(row=0, column=2, columnspan=2, padx=(10, 0), pady=5, sticky='w')

        y1_marker_label = tk.Label(y1_options_frame, text='Select marker: ')
        y1_marker_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y1_marker_combo = Combobox(y1_options_frame, width=30)
        self.y1_marker_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')

        y1_marker_size_label = tk.Label(y1_options_frame, text='Size: ')
        y1_marker_size_label.grid(row=1, column=2, padx=(10, 0), pady=5, sticky='w')
        self.y1_marker_size_combo = Combobox(y1_options_frame, width=30)
        self.y1_marker_size_combo.grid(row=1, column=3, padx=(10, 0), pady=5, sticky='w')

        y1_linestyle_label = tk.Label(y1_options_frame, text='Select line style: ')
        y1_linestyle_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y1_linestyle_combo = Combobox(y1_options_frame, width=30)
        self.y1_linestyle_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        y1_line_width_label = tk.Label(y1_options_frame, text='Width: ')
        y1_line_width_label.grid(row=2, column=2, padx=(10, 0), pady=5, sticky='w')
        self.y1_line_width_combo = Combobox(y1_options_frame, width=30)
        self.y1_line_width_combo.grid(row=2, column=3, padx=(10, 0), pady=5, sticky='w')

        y1_colour_label = tk.Label(y1_options_frame, text='Select line colour: ')
        y1_colour_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y1_colour_combo = Combobox(y1_options_frame, width=30)
        self.y1_colour_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky='w')

        y1_errorbar_label = tk.Label(y1_options_frame, text='Select errorbar values: ')
        y1_errorbar_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y1_errorbar_combo = Combobox(y1_options_frame, width=30)
        self.y1_errorbar_combo.grid(row=4, column=1, padx=(10, 0), pady=5, sticky='w')

    def y2_axis_options_tab(self):
        y2_options_frame = tk.Frame(self.nb)
        self.nb.add(y2_options_frame, text='Y-Axis (2) Options')

        y2_marker_label = tk.Label(y2_options_frame, text='Select marker: ')
        y2_marker_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y2_marker_combo = Combobox(y2_options_frame, width=30)
        self.y2_marker_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')

        y2_marker_size_label = tk.Label(y2_options_frame, text='Size: ')
        y2_marker_size_label.grid(row=0, column=2, padx=(10, 0), pady=5, sticky='w')
        self.y2_marker_size_combo = Combobox(y2_options_frame, width=30)
        self.y2_marker_size_combo.grid(row=0, column=3, padx=(10, 0), pady=5, sticky='w')

        y2_linestyle_label = tk.Label(y2_options_frame, text='Select line style: ')
        y2_linestyle_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y2_linestyle_combo = Combobox(y2_options_frame, width=30)
        self.y2_linestyle_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')

        y2_line_width_label = tk.Label(y2_options_frame, text='Width: ')
        y2_line_width_label.grid(row=1, column=2, padx=(10, 0), pady=5, sticky='w')
        self.y2_line_width_combo = Combobox(y2_options_frame, width=30)
        self.y2_line_width_combo.grid(row=1, column=3, padx=(10, 0), pady=5, sticky='w')

        y2_colour_label = tk.Label(y2_options_frame, text='Select line colour: ')
        y2_colour_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y2_colour_combo = Combobox(y2_options_frame, width=30)
        self.y2_colour_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        y2_errorbar_label = tk.Label(y2_options_frame, text='Select errorbar values: ')
        y2_errorbar_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.y2_errorbar_combo = Combobox(y2_options_frame, width=30)
        self.y2_errorbar_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky='w')

    def font_options_tab(self):
        font_options_frame = tk.Frame(self.nb)
        self.nb.add(font_options_frame, text='Font Options')

        title_size_label = tk.Label(font_options_frame, text='Select title size: ')
        title_size_label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky='w')
        self.title_size_combo = Combobox(font_options_frame, width=30)
        self.title_size_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')

        axis_label_size_label = tk.Label(font_options_frame, text='Set axis labels size: ')
        axis_label_size_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        self.axis_label_size_combo = Combobox(font_options_frame, width=30)
        self.axis_label_size_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')

        tick_size_label = tk.Label(font_options_frame, text='Set tick size: ')
        tick_size_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.tick_size_combo = Combobox(font_options_frame, width=30)
        self.tick_size_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')

        legend_size_label = tk.Label(font_options_frame, text='Set legend size: ')
        legend_size_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.legend_size_combo = Combobox(font_options_frame, width=30)
        self.legend_size_combo.grid(row=3, column=1, padx=(10, 0), pady=5, sticky='w')

        # y2_colour_label = tk.Label(font_options_frame, text='Set pass size: ')
        # y2_colour_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        # self.y2_colour_combo = Combobox(font_options_frame, width=30)
        # self.y2_colour_combo.grid(row=4, column=1, padx=(10, 0), pady=5, sticky='w')

        # y2_errorbar_label = tk.Label(font_options_frame, text='Select errorbar values: ')
        # y2_errorbar_label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky='w')
        # self.y2_errorbar_combo = Combobox(font_options_frame, width=30)
        # self.y2_errorbar_combo.grid(row=5, column=1, padx=(10, 0), pady=5, sticky='w')

        # y2_errorbar_label = tk.Label(font_options_frame, text='Select errorbar values: ')
        # y2_errorbar_label.grid(row=6, column=0, padx=(10, 0), pady=5, sticky='w')
        # self.y2_errorbar_combo = Combobox(font_options_frame, width=30)
        # self.y2_errorbar_combo.grid(row=6, column=1, padx=(10, 0), pady=5, sticky='w')

    def create_toolbar_frame(self):
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(side=tk.LEFT)

        self.save_fig_button = tk.Button(master=self.graph_frame, text='Save Figure')
        self.save_fig_button.grid(row=2, column=0, sticky='w', padx=10)
        toolbar_frame = tk.Frame(master=self.graph_frame)
        toolbar_frame.grid(row=2, column=1, columnspan=2, sticky='w', padx=10)

        self.main_fig, self.ax1 = plt.subplots(1, 1, figsize=(10, 6), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.main_fig, master=self.graph_frame)
        toolbar1 = NavigationToolbar2Tk(self.canvas1, toolbar_frame)
        toolbar1.update()
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=3, column=0, columnspan=4, padx=0)
