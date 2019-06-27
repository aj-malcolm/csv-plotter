import os
import matplotlib
import pandas as pd
import numpy as np
import functions as fnc
from tkinter import Tk, Frame, END
from tkinter import filedialog
from scipy.optimize import curve_fit
from createNoiseClass import NoiseData
from createUI import MainWindow
matplotlib.use('TkAgg')


class Application(Frame, MainWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_ui()

        self.noise_object = NoiseData()

        # Variables inherited from MainWindow
        try:
            self.load_button['command'] = self.select_directory
            self.sub_dir_button['command'] = self.create_file_list
            self.rolling_avg_button['command'] = self.rolling_avg_pushed
            self.begin_analysis_button['command'] = self.begin_analysis
            self.sub_dir_combo.bind("<<ComboboxSelected>>", self.create_file_list)
            self.file_list_combo.bind("<<ComboboxSelected>>", self.select_new_file)
            self.rolling_avg_entry.insert(0, '10')
            self.rolling_avg_entry.bind("<Return>", self.change_rolling_avg_num)
            self.next_meas_button['command'] = self.select_next_meas
            self.prev_meas_button['command'] = self.select_prev_meas
            self.canvas1.mpl_connect('button_press_event', self.on_pick)
            self.canvas1.mpl_connect('button_release_event', self.off_pick)

            self.undo_peak_button['command'] = self.undo_peak
            self.clear_peaks_button['command'] = self.clear_peaks
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
        self.point_num = 0
        self.params = []

    def select_directory(self):
        """
            pick a directory from which to load data
        """
        try:
            self.main_dir = filedialog.askdirectory()
            self.directory_text.delete(1.0, END)
            self.directory_text.insert('1.0', str(self.main_dir))
            self.sub_directories = [x[0].replace(self.main_dir, '') for x in os.walk(self.main_dir)]
            self.sub_dir_combo['values'] = self.sub_directories[1:]
        except Exception as err:
            print("Error encountered in select_directory: " + str(err))

    def create_file_list(self, event=None):
        """
            Create file list
        """
        self.file_dir = self.main_dir + self.sub_dir_combo.get()
        try:
            self.file_list = [x[2] for x in os.walk(self.file_dir)][0]
            self.file_list = [x for x in self.file_list if '.csv' in x]
            self.file_list_combo['values'] = self.file_list
        except Exception as err:
            print("Error encountered in create_file_list: " + str(err))

    def create_noise_object(self, file_name):
        self.noise_object = NoiseData(file_name, self.rolling_avg_use)
        self.clear_peaks()
        self.update_main_plot()

    def select_new_file(self, event=None):
        try:
            file_name = self.file_dir + '\\' + self.file_list_combo.get()
            self.create_noise_object(file_name)
        except Exception as err:
            print("Error occurred in read_csv: " + str(err))

    def select_next_meas(self):
        index = self.file_list.index(self.file_list_combo.get())
        if index < len(self.file_list):
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

    def update_main_plot(self, dig=False):
        self.f1ax1.clear()
        self.f1ax2.clear()

        self.f1ax1.plot(self.noise_object.time, self.noise_object.current)
        self.f1ax1.set_title("Sampled Current Data w/ Rolling Average")
        self.f1ax1.set_xlabel("Time (s)")
        self.f1ax1.set_ylabel("Current (A)")

        self.f1ax2.plot(self.noise_object.current_histogram, self.noise_object.current_histogram_bins)
        self.f1ax2.set_title("Current Levels of Sampled Data")
        self.f1ax2.set_xlabel("Counts")

        if len(self.noise_object.params) > 0:
            try:
                self.f1ax2.plot(self.noise_object.gauss_curve, self.noise_object.current_histogram_bins)
            except Exception as err:
                print('Error in plotting gauss: ' + str(err))

        self.main_fig.tight_layout()
        self.canvas1.draw()

    def rolling_avg_pushed(self):
        try:
            if self.rolling_avg_use:
                self.rolling_avg_button['text'] = 'Enable rolling average'
            else:
                self.rolling_avg_button['text'] = 'Disable rolling average'
        except Exception as err:
            print('Error setting button text. Msg: ' + str(err))
        self.rolling_avg_use = not self.rolling_avg_use
        self.noise_object.toggle_rolling_average(self.rolling_avg_use)
        self.update_main_plot()

    def change_rolling_avg_num(self, event):
        num = int(self.rolling_avg_entry.get())
        self.noise_object.toggle_rolling_average(self.rolling_avg_use, num)
        self.update_main_plot()

    def print_pdf(self):
        pass

    def on_pick(self, event):
        y_point, x_point = event.xdata, event.ydata  # have to flip x and y because plot is displayed at right angle
        self.params += [x_point, y_point, abs(x_point/1000)]
        self.noise_object.create_gaussian_fit(self.params)
        self.update_main_plot()

    def off_pick(self, event):
        x_point, y_point = event.xdata, event.ydata

    def begin_analysis(self):
        self.add_tab()
        self.noise_object.digitize()
        self.f2ax1.plot(self.noise_object.time, self.noise_object.current)
        self.f2ax1.plot(self.noise_object.time, self.noise_object.digitized_current)
        self.f2ax3.plot(self.noise_object.time, self.noise_object.peak_removed)
        self.f2ax4.plot(self.noise_object.current_histogram_peak_removed, self.noise_object.current_histogram_peak_removed_bins)

    def undo_peak(self):
        if len(self.params) > 0:
            self.params = self.params[0:-3]
        self.noise_object.create_gaussian_fit(self.params)
        self.update_main_plot()

    def clear_peaks(self):
        self.params = []
        self.noise_object.create_gaussian_fit(self.params)
        self.update_main_plot()
        self.vt = []


if __name__ == "__main__":
    # Tk toplevel widget
    root = Tk()

    # Set title using wm (windows manager)
    root.wm_title("RTN Analysis Code")

    # Create the application
    app = Application()

    # Start the program
    root.mainloop()
