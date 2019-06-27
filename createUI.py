import matplotlib  # Based on testing, v 3.1.0 doesn't work. v 3.0.3 is tested to work.
from tkinter.ttk import Combobox, Notebook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


class MainWindow:
    def __init__(self):
        # Buttons
        self.sub_dir_button = None
        self.load_button = None
        self.rolling_avg_button = None
        self.next_meas_button = None
        self.prev_meas_button = None
        self.print_pdf = None
        self.begin_analysis_button = None
        self.clear_peaks_button = None
        self.undo_peak_button = None

        # Text Entries
        self.rolling_avg_entry = None

        # Text Fields and Labels
        self.directory_text = None
        self.sub_dir_label = None
        self.file_list_label = None
        self.rolling_avg_label = None

        # Comboboxes
        self.file_list_combo = None
        self.sub_dir_combo = None

        # Graphs
        self.main_fig = None
        self.f1ax1 = None
        self.f1ax2 = None
        self.canvas1 = None

        # Notebook
        self.nb = None

    def create_ui(self):
        self.load_button = tk.Button(self, text='Select Directory')
        self.load_button.grid(row=0, column=0, padx=(5, 0), pady=2.5)
        self.directory_text = tk.Text(self, height=1, width=160)
        self.directory_text.grid(row=0, column=1, padx=(10, 15), pady=2.5, sticky='w')

        self.sub_dir_label = tk.Label(self, text='Select sub-directory: ')
        self.sub_dir_label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky='w')
        row1_frame = tk.Frame(master=self)
        row1_frame.grid(row=1, column=1, columnspan=5, padx=10, sticky='w')
        self.sub_dir_combo = Combobox(row1_frame, width=30)
        self.sub_dir_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.sub_dir_button = tk.Button(row1_frame, text='No sub-dir', width=10)
        self.sub_dir_button.pack(side=tk.LEFT, padx=5)
        self.file_list_label = tk.Label(row1_frame, text='Select a file to load: ')
        self.file_list_label.pack(side=tk.LEFT, padx=(15, 5))
        self.file_list_combo = Combobox(row1_frame, width=80)
        self.file_list_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.next_meas_button = tk.Button(row1_frame, text='Next measurement')
        self.next_meas_button.pack(side=tk.RIGHT, padx=(0, 5))
        self.prev_meas_button = tk.Button(row1_frame, text='Previous measurement')
        self.prev_meas_button.pack(side=tk.RIGHT, padx=(20, 5))

        self.nb = Notebook(self)
        self.nb.grid(row=2, column=0, columnspan=10)
        self.add_tab(True)

    def add_tab(self, main=False):
        if main:
            main_frame = tk.Frame(self.nb)
            self.nb.add(main_frame, text='Main Viewer')

            toolbar_frame = tk.Frame(master=main_frame)
            toolbar_frame.grid(row=0, column=0, columnspan=2, sticky='w', padx=10)

            peak_options_frame = tk.Frame(main_frame)
            peak_options_frame.grid(row=0, column=1, sticky='e')
            self.clear_peaks_button = tk.Button(peak_options_frame, text='Clear Peaks')
            self.clear_peaks_button.pack(padx=(5, 10), pady=2.5, side=tk.RIGHT)
            self.undo_peak_button = tk.Button(peak_options_frame, text='Undo Last Peak')
            self.undo_peak_button.pack(padx=5, pady=2.5, side=tk.RIGHT)

            self.main_fig, (self.f1ax1, self.f1ax2) = plt.subplots(1, 2, figsize=(14, 4), dpi=100,
                                                                   gridspec_kw={'width_ratios': [4, 1]})
            self.canvas1 = FigureCanvasTkAgg(self.main_fig, master=main_frame)
            toolbar1 = NavigationToolbar2Tk(self.canvas1, toolbar_frame)
            toolbar1.update()
            self.canvas1.draw()
            self.canvas1.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=0)

            graph_options_frame = tk.Frame(master=main_frame)
            graph_options_frame.grid(row=2, column=0, pady=5, columnspan=2, padx=(5, 0), sticky='w')
            self.rolling_avg_button = tk.Button(graph_options_frame, text='Enable rolling average')
            self.rolling_avg_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)
            self.rolling_avg_label = tk.Label(graph_options_frame, text='Rolling length: ')
            self.rolling_avg_label.pack(side=tk.LEFT, padx=(0, 5), pady=5)
            self.rolling_avg_entry = tk.Entry(graph_options_frame, width=10)
            self.rolling_avg_entry.pack(side=tk.LEFT, padx=(0, 5), pady=5)

            major_options_frame = tk.Frame(master=main_frame)
            major_options_frame.grid(row=2, column=1, padx=(5, 0), pady=2.5, sticky='e')
            self.begin_analysis_button = tk.Button(major_options_frame, text='Begin Analysis')
            self.begin_analysis_button.pack(padx=5, pady=2.5, side=tk.RIGHT)
            self.print_pdf = tk.Button(major_options_frame, text='Generate PDF', width=15)
            self.print_pdf.pack(padx=5, pady=2.5, side=tk.RIGHT)

            '''
            main_fig, self.dI_distro = plt.subplots(1, 1, figsize=(4, 3), dpi=100)
            self.analysis_canvas = FigureCanvasTkAgg(main_fig, master=main_frame)
            self.main_fig.tight_layout()
            self.analysis_canvas.draw()
            self.analysis_canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=0)
            '''
        else:
            self.analysis_frame = tk.Frame(self.nb)
            self.nb.add(self.analysis_frame, text='Analysis Viewer')

            toolbar_frame = tk.Frame(master=self.analysis_frame)
            toolbar_frame.grid(row=0, column=0, columnspan=2, sticky='w', padx=10)

            self.fig_analysis, ((self.f2ax1, self.f2ax2), (self.f2ax3, self.f2ax4)) = plt.subplots(2, 2, figsize=(14, 4), dpi=100,
                                                                   gridspec_kw={'width_ratios': [4, 1]})
            self.canvas_analysis = FigureCanvasTkAgg(self.fig_analysis, master=self.analysis_frame)
            toolbar1 = NavigationToolbar2Tk(self.canvas_analysis, toolbar_frame)
            toolbar1.update()
            self.fig_analysis.tight_layout()
            self.canvas_analysis.draw()
            self.canvas_analysis.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=0)
