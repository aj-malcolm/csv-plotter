import os
import matplotlib
import pandas as pd
import functions as fnc
import numpy as np
from tkinter import Tk, Frame, END
from tkinter import filedialog
from createUI import MainWindow
matplotlib.use('TkAgg')


class Application(Frame, MainWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_ui()

        # Variables inherited from MainWindow
        try:
            self.load_button['command'] = self.create_file_list
            self.file_list_combo.bind("<<ComboboxSelected>>", self.select_new_file)
            self.next_meas_button['command'] = self.select_next_meas
            self.prev_meas_button['command'] = self.select_prev_meas
            self.plot_button['command'] = self.update_main_plot
            self.normalize_button['command'] = self.normalize
            self.normalize_entry.bind("<Return>", self.normalize)
            self.reset_xrange_button['command'] = self.reset_x_range
            self.reset_y1range_button['command'] = self.reset_y1_range
            self.reset_y2range_button['command'] = self.reset_y2_range
            self.save_fig_button['command'] = self.save_fig

            self.set_xmin_range_entry.bind("<Return>", self.update_main_plot)
            self.set_xmax_range_entry.bind("<Return>", self.update_main_plot)
            self.set_y1min_range_entry.bind("<Return>", self.update_main_plot)
            self.set_y1max_range_entry.bind("<Return>", self.update_main_plot)
            self.set_y2min_range_entry.bind("<Return>", self.update_main_plot)
            self.set_y2max_range_entry.bind("<Return>", self.update_main_plot)
            # self.canvas1.mpl_connect('button_press_event', self.on_pick)
            # self.canvas1.mpl_connect('button_release_event', self.off_pick)
        except Exception as err:
            print('Error setting variables: ' + str(err))

        # Variables used in this file
        self.main_dir = None
        self.sub_directories = None
        self.file_list = None
        self.file_dir = None
        self.time = None
        self.drain_current = None
        self.time_orig = None
        self.drain_current_orig = None
        self.num_bins = None
        self.current_histogram = None
        self.current_histogram_bins = None
        self.time_rolling_avg = None
        self.drain_current_rolling_avg = None
        self.current_histogram_rolling_avg = None
        self.current_histogram_rolling_avg_bins = None
        self.rolling_avg_use = False
        self.use_normalize = False
        self.point_num = 0
        self.params = []

        # Lists and dictionaries defining line options for first and second y-axes
        self.markers = ['.', ',', 'o', 'v', '^', '<', '>', '+', '*', 'x', 'D', 'None']
        self.linestyles = ['solid', 'dotted', 'dashed', 'dashdot', 'None']
        self.line_colours = {'Blue': '#1f77b4', 'Orange': '#ff7f0e', 'Green': '#2ca02c', 'Red': '#d62728', 'Purple': '#9467bd',
                             'Brown': '#8c564b', 'Magenta': '#e377c2', 'Grey': '#7f7f7f', 'Yellow': '#bcbd22', 'Cyan': '#17becf'}
        self.marker_size = [str(4 * x) for x in np.linspace(1, 6, 6)]
        self.line_size = [str(x) for x in np.linspace(1, 6, 6)]

        # Populates line options for first y-axis with default values.
        self.y1_linestyle_combo['values'] = self.linestyles
        self.y1_linestyle_combo.set(self.linestyles[0])
        self.y1_marker_combo['values'] = self.markers
        self.y1_marker_combo.set(self.markers[0])
        self.y1_marker_size_combo['values'] = self.marker_size
        self.y1_marker_size_combo.set(self.marker_size[0])
        self.y1_line_width_combo['values'] = self.line_size
        self.y1_line_width_combo.set(self.line_size[0])
        self.y1_colour_combo['values'] = list(self.line_colours.keys())
        self.y1_colour_combo.set(list(self.line_colours.keys())[0])

        # Populates line options for second y-axis with default values.
        self.y2_linestyle_combo['values'] = self.linestyles
        self.y2_linestyle_combo.set(self.linestyles[0])
        self.y2_marker_combo['values'] = self.markers
        self.y2_marker_combo.set(self.markers[0])
        self.y2_marker_size_combo['values'] = self.marker_size
        self.y2_marker_size_combo.set(self.marker_size[0])
        self.y2_line_width_combo['values'] = self.line_size
        self.y2_line_width_combo.set(self.line_size[0])
        self.y2_colour_combo['values'] = list(self.line_colours.keys())
        self.y2_colour_combo.set(list(self.line_colours.keys())[0])

        # Populates font size comboboxes with dictionary keys. 
        # Sets default value to Medium
        self.font_size = {'X-Small': 8, 'Small': 10, 'Medium': 12, 'Large': 14, 'X-Large': 16}
        self.title_size_combo['values'] = list(self.font_size.keys())
        self.title_size_combo.set(list(self.font_size.keys())[1])
        self.axis_label_size_combo['values'] = list(self.font_size.keys())
        self.axis_label_size_combo.set(list(self.font_size.keys())[1])
        self.tick_size_combo['values'] = list(self.font_size.keys())
        self.tick_size_combo.set(list(self.font_size.keys())[1])
        self.legend_size_combo['values'] = list(self.font_size.keys())
        self.legend_size_combo.set(list(self.font_size.keys())[1])

    def create_file_list(self):
        """
            Pick a directory from which to load data
        """
        try:
            self.main_dir = filedialog.askdirectory()
            self.directory_text.delete(1.0, END)
            self.directory_text.insert('1.0', str(self.main_dir))
        except Exception as err:
            print("Error encountered in select_directory: " + str(err))
        self.file_dir = self.main_dir
        try:
            self.file_list = [x[2] for x in os.walk(self.file_dir)][0]
            self.file_list = [x for x in self.file_list if '.csv' in x]
            self.file_list_combo['values'] = self.file_list
            self.file_list_combo.set(self.file_list[0])
        except Exception as err:
            print("Error encountered in create_file_list: " + str(err))
        self.select_new_file()

    def select_new_file(self, event=None):
        """
            Function run when a new file is selected. CSV is read into a Pandas DataFrame,
            then headers are extracted and used to fill the various comboboxes around the UI.
        """
        try:
            file_name = self.file_dir + '\\' + self.file_list_combo.get()

            self.df = pd.read_csv(file_name)
            self.headers = self.df.columns.values.tolist()
            self.x_axis_combo['values'] = self.headers
            self.x_axis_combo.set(self.headers[0])
            self.y_axis_one_combo['values'] = self.headers
            self.y_axis_one_combo.set(self.headers[1])
            self.y1_errorbar_combo['values'] = ['None'] + self.headers
            self.y1_errorbar_combo.set('None')
            y_axis2 = ['None'] + self.headers
            self.y_axis_two_combo['values'] = y_axis2
            self.y2_errorbar_combo['values'] = ['None'] + self.headers
            self.y2_errorbar_combo.set('None')
            self.y_axis_two_combo.set(y_axis2[0])

            # Adding options for subplot comboboxes
            self.subplot1_combo['values'] = ['None'] + self.headers
            self.subplot1_combo.set('None')
            self.subplot2_combo['values'] = ['None'] + self.headers
            self.subplot2_combo.set('None')
            self.subplot3_combo['values'] = ['None'] + self.headers
            self.subplot3_combo.set('None')
            self.subplot4_combo['values'] = ['None'] + self.headers
            self.subplot4_combo.set('None')

        except Exception as err:
            print("Error occurred in read_csv: " + str(err))
        self.update_main_plot()

    def update_axes(self):
        try:
            self.x_data_orig = self.df[self.x_axis_combo.get()].tolist()
            self.x_data = self.x_data_orig
            self.y1_data_orig = self.df[self.y_axis_one_combo.get()].tolist()
            self.y1_data = self.y1_data_orig

            if 'None' in self.y1_errorbar_combo.get():
                self.ax1.plot(self.x_data, self.y1_data, marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(), c=self.line_colours[self.y1_colour_combo.get()],
                              ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))
            else:
                self.y_err = self.df[self.y1_errorbar_combo.get()].tolist()
                self.ax1.errorbar(self.x_data, self.y1_data, yerr=self.y_err, capsize=2, marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                                  c=self.y1_colour_combo.get(), ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))
            self.default_x_lim = self.ax1.get_xlim()
            self.default_y1_lim = self.ax1.get_ylim()

            self.y2_str = self.y_axis_two_combo.get()

            try:
                self.ax2.remove()
            except:
                pass
            if 'None' not in self.y2_str:
                self.y2_data_orig = self.df[self.y2_str].tolist()
                self.y2_data = self.y2_data_orig
                self.ax2 = self.ax1.twinx()
                self.ax2.plot(self.x_data, self.y2_data)
                self.default_y2_lim = self.ax2.get_ylim()

        except Exception as err:
            print('Error encountered in select_new_file 2: ' + str(err))

    def select_next_meas(self):
        """
            Steps to the next item in list which defines the file combobox, and 
            triggers it to load.
        """
        index = self.file_list.index(self.file_list_combo.get())
        if index < len(self.file_list) - 1:
            index = index + 1
        else:
            pass
        self.file_list_combo.set(self.file_list[index])
        self.select_new_file()

    def select_prev_meas(self):
        """
            Steps to the previous item in list which defines the file combobox, and 
            triggers it to load.
        """
        index = self.file_list.index(self.file_list_combo.get())
        if index > 0:
            index = index - 1
        else:
            pass
        self.file_list_combo.set(self.file_list[index])
        self.select_new_file()

    def update_main_plot(self, event=None):
        self.update_axes()
        self.ax1.clear()
        self.ax1.yaxis.set_ticks_position('both')
        try:
            self.ax2.clear()
        except:
            pass

        self.set_limits()
        if 'None' in self.y1_errorbar_combo.get():
            self.ax1.plot(self.x_data, self.y1_data, marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(), c=self.line_colours[self.y1_colour_combo.get()],
                          ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()), label=self.y1_legend_entry.get())
        else:
            self.y1_err = self.df[self.y1_errorbar_combo.get()].tolist()
            self.ax1.errorbar(self.x_data, self.y1_data, yerr=self.y1_err, capsize=2, marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                              c=self.line_colours[self.y1_colour_combo.get()], ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()),
                              label=self.y1_legend_entry.get())
        
        if 'None' not in self.subplot1_combo.get():
            subplot1_data = self.df[self.subplot1_combo.get()].tolist()
            self.ax1.plot(self.x_data, subplot1_data, label=self.subplot1_entry.get(), marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                          ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))
        if 'None' not in self.subplot2_combo.get():
            subplot2_data = self.df[self.subplot2_combo.get()].tolist()
            self.ax1.plot(self.x_data, subplot2_data, label=self.subplot2_entry.get(), marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                          ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))
        if 'None' not in self.subplot3_combo.get():
            subplot3_data = self.df[self.subplot3_combo.get()].tolist()
            self.ax1.plot(self.x_data, subplot3_data, label=self.subplot3_entry.get(), marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                          ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))
        if 'None' not in self.subplot4_combo.get():
            subplot4_data = self.df[self.subplot4_combo.get()].tolist()
            self.ax1.plot(self.x_data, subplot4_data, label=self.subplot4_entry.get(), marker=self.y1_marker_combo.get(), ls=self.y1_linestyle_combo.get(),
                          ms=float(self.y1_marker_size_combo.get()), lw=float(self.y1_line_width_combo.get()))

        self.ax1.set_xlabel(self.x_axis_title_entry.get())
        self.ax1.set_ylabel(self.y1_axis_title_entry.get())

        if 'None' not in self.y2_str:
            self.ax1.yaxis.set_ticks_position('left')
            if 'None' in self.y2_errorbar_combo.get():
                self.ax2.plot(self.x_data, self.y2_data, marker=self.y2_marker_combo.get(), ls=self.y2_linestyle_combo.get(), color=self.line_colours[self.y2_colour_combo.get()],
                              ms=float(self.y2_marker_size_combo.get()), lw=float(self.y2_line_width_combo.get()), label=self.y2_legend_entry.get())
            else:
                self.y2_err = self.df[self.y2_errorbar_combo.get()].tolist()
                self.ax2.errorbar(self.x_data, self.y2_data, yerr=self.y2_err, capsize=2, marker=self.y2_marker_combo.get(), ls=self.y2_linestyle_combo.get(),
                                  color=self.line_colours[self.y2_colour_combo.get()], ms=float(self.y2_marker_size_combo.get()), lw=float(self.y2_line_width_combo.get()),
                                  label=self.y2_legend_entry.get())

            self.default_ylim_two = self.ax2.get_ylim()
            self.ax2.set_ylabel(self.y2_axis_title_entry.get())
            self.ax2.axes.get_yaxis().set_visible(True)    
            self.ax2.yaxis.label.set_fontsize(self.font_size[self.axis_label_size_combo.get()])  
            for tick in self.ax2.get_yticklabels():
                tick.set_fontsize(self.font_size[self.tick_size_combo.get()])

        # Sets figure title and font size of title
        self.ax1.set_title(self.set_title_entry.get().replace('\TITLE', self.file_list_combo.get()), fontsize=self.font_size[self.title_size_combo.get()])

        # Sets font size for both x-axis and y(1)-axis labels
        self.ax1.xaxis.label.set_fontsize(self.font_size[self.axis_label_size_combo.get()])
        self.ax1.yaxis.label.set_fontsize(self.font_size[self.axis_label_size_combo.get()])
        
        # Sets font size for both x-axis and y(1)-axis tick markers
        for tick in self.ax1.get_xticklabels():
            tick.set_fontsize(self.font_size[self.tick_size_combo.get()])
        for tick in self.ax1.get_yticklabels():
            tick.set_fontsize(self.font_size[self.tick_size_combo.get()])

        # Adds legend, either from ax1 or combining ax1 into ax2 legend (when ax2 present)
        # also sets font size
        if self.y1_legend_entry.get() or self.y2_legend_entry.get():
            lines, labels = self.ax1.get_legend_handles_labels()
            if 'None' not in self.y2_str:
                lines2, labels2 = self.ax2.get_legend_handles_labels()
                self.ax2.legend(lines + lines2, labels + labels2, loc=0, fontsize=self.font_size[self.legend_size_combo.get()])
            else:
                self.ax1.legend(lines, labels, loc=0, fontsize=self.font_size[self.legend_size_combo.get()])

        self.main_fig.tight_layout()
        self.canvas1.draw()

    def normalize(self, event=None):
        if event is None:
            self.normalize_entry.delete(0, 'end')
        if len(self.normalize_entry.get()) != 0:
            self.use_normalize = True
        else:
            self.use_normalize = False
        self.update_main_plot()

    def print_pdf(self):
        pass

    def on_pick(self, event):
        y_point, x_point = event.xdata, event.ydata  # have to flip x and y because plot is displayed at right angle
        return y_point, x_point

    def set_limits(self):
        if self.retain_range.get() == 0:
            if len(self.set_xmin_range_entry.get()) == 0:
                xmin = 0
            else:
                xmin = fnc.find_nearest(self.x_data_orig, float(self.set_xmin_range_entry.get()))
            if len(self.set_xmax_range_entry.get()) == 0:
                self.x_data = self.x_data_orig[xmin:]
                self.y1_data = self.y1_data_orig[xmin:]
            else:
                xmax = fnc.find_nearest(self.x_data_orig, float(self.set_xmax_range_entry.get()))
                self.x_data = self.x_data_orig[xmin:xmax]
                self.y1_data = self.y1_data_orig[xmin:xmax]

            if len(self.set_y1min_range_entry.get()) != 0:
                self.ax1.set_ylim(bottom=float(self.set_y1min_range_entry.get()), top=None)
            if len(self.set_y1max_range_entry.get()) != 0:
                self.ax1.set_ylim(bottom=None, top=float(self.set_y1max_range_entry.get()))

            if 'None' not in self.y2_str:
                if len(self.set_y2min_range_entry.get()) != 0:
                    self.ax2.set_ylim(bottom=float(self.set_y2min_range_entry.get()), top=None)
                if len(self.set_y2max_range_entry.get()) != 0:
                    self.ax2.set_ylim(bottom=None, top=float(self.set_y2max_range_entry.get()))

        else:
            self.x_data = self.x_data_orig
            self.y1_data = self.y1_data_orig
            if 'None' not in self.y2_str:
                self.y2_data = self.y2_data_orig

        if self.use_normalize:
            if len(self.normalize_entry.get()) != 0:
                norm_local = float(self.normalize_entry.get())
                norm_index = fnc.find_nearest(self.x_data_orig, norm_local)
                norm_min = max(norm_index - 50, 0)
                norm_value = max(self.y1_data_orig[norm_min: norm_index + 50])
                self.y1_data = [x / norm_value for x in self.y1_data]

    def reset_x_range(self):
        self.set_xmax_range_entry.delete(0, 'end')
        self.set_xmin_range_entry.delete(0, 'end')
        self.update_main_plot()

    def reset_y1_range(self):
        self.set_y1max_range_entry.delete(0, 'end')
        self.set_y1min_range_entry.delete(0, 'end')
        self.update_main_plot()

    def reset_y2_range(self):
        self.set_y2max_range_entry.delete(0, 'end')
        self.set_y2min_range_entry.delete(0, 'end')
        self.update_main_plot()

    def save_fig(self):
        if not os.path.exists(self.file_dir + '/Figures'):
            os.makedirs(self.file_dir + '/Figures')
        self.main_fig.savefig(self.file_dir + '/Figures/' + self.file_list_combo.get().replace('.csv', '.png'))


if __name__ == "__main__":
    # Tk toplevel widget
    root = Tk()

    # Set title using wm (windows manager)
    root.wm_title("CSV Plotter")

    # Create the application
    app = Application()

    # Start the program
    root.mainloop()
