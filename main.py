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
            #self.canvas1.mpl_connect('button_press_event', self.on_pick)
            #self.canvas1.mpl_connect('button_release_event', self.off_pick)
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

    def create_file_list(self):
        """
            pick a directory from which to load data
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
        try:
            file_name = self.file_dir + '\\' + self.file_list_combo.get()

            self.df = pd.read_csv(file_name)
            self.headers = self.df.columns.values.tolist()
            self.x_axis_combo['values'] = self.headers
            self.x_axis_combo.set(self.headers[0])
            self.y_axis_one_combo['values'] = self.headers
            self.y_axis_one_combo.set(self.headers[1])
            y_axis2 = ['None'] + self.headers
            self.y_axis_two_combo['values'] = y_axis2
            self.y_axis_two_combo.set(y_axis2[0])
        except Exception as err:
            print("Error occurred in read_csv: " + str(err))

        try:
            self.x_data_orig = self.df[self.x_axis_combo.get()].tolist()
            self.x_data = self.x_data_orig
            self.y1_data_orig = self.df[self.y_axis_one_combo.get()].tolist()
            self.y1_data = self.y1_data_orig

            self.ax1.plot(self.x_data, self.y1_data)
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

        self.update_main_plot()

    def select_next_meas(self):
        index = self.file_list.index(self.file_list_combo.get())
        if index < len(self.file_list)-1:
            index = index + 1
        else:
            pass
        self.file_list_combo.set(self.file_list[index])
        self.select_new_file()

    def select_prev_meas(self):
        index = self.file_list.index(self.file_list_combo.get())
        if index > 0:
            index = index - 1
        else:
            pass
        self.file_list_combo.set(self.file_list[index])
        self.select_new_file()

    def update_main_plot(self, event=None):
        self.ax1.clear()
        self.ax1.yaxis.set_ticks_position('both')
        try:
            self.ax2.clear()
        except:
            pass

        self.set_limits()
        self.ax1.plot(self.x_data, self.y1_data)

        self.ax1.set_xlabel(self.x_axis_label_entry.get())
        self.ax1.set_ylabel(self.y_axis_one_label_entry.get())

        if 'None' not in self.y2_str:
            self.ax1.yaxis.set_ticks_position('left')
            self.ax2.plot(self.x_data, self.y2_data)
            self.default_ylim_two = self.ax2.get_ylim()
            self.ax2.set_ylabel(self.y_axis_two_label_entry.get())
            self.ax2.axes.get_yaxis().set_visible(True)

        self.ax1.set_title(self.set_title_entry.get().replace('\TITLE', self.file_list_combo.get()))
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
                norm_min = max(norm_index-50, 0)
                norm_value = max(self.y1_data_orig[norm_min: norm_index+50])
                self.y1_data = [x/norm_value for x in self.y1_data]

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
