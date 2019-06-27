import os
import matplotlib
import pandas as pd
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
            self.select_new_file()
        except Exception as err:
            print("Error encountered in create_file_list: " + str(err))

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

            self.update_main_plot()
        except Exception as err:
            print("Error occurred in read_csv: " + str(err))

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

    def update_main_plot(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax2.axes.get_yaxis().set_visible(False)
        self.ax1.yaxis.set_ticks_position('both')

        x_data = self.df[self.x_axis_combo.get()].tolist()
        y1_data = self.df[self.y_axis_one_combo.get()].tolist()
        y2_str = self.y_axis_two_combo.get()
        self.ax1.plot(x_data, y1_data)

        self.ax1.set_xlabel(self.x_axis_label_entry.get())
        self.ax1.set_ylabel(self.y_axis_one_label_entry.get())

        if 'None' not in y2_str:
            y2_data = self.df[y2_str].tolist()
            self.ax1.yaxis.set_ticks_position('left')
            self.ax2.plot(x_data, y2_data)
            self.ax2.set_ylabel(self.y_axis_two_label_entry.get())
            self.ax2.axes.get_yaxis().set_visible(True)

        self.ax1.set_title(self.set_title_entry.get().replace('\TITLE', self.file_list_combo.get()))
        self.main_fig.tight_layout()
        self.canvas1.draw()

    def print_pdf(self):
        pass

    def on_pick(self, event):
        y_point, x_point = event.xdata, event.ydata  # have to flip x and y because plot is displayed at right angle


if __name__ == "__main__":
    # Tk toplevel widget
    root = Tk()

    # Set title using wm (windows manager)
    root.wm_title("CSV Plotter")

    # Create the application
    app = Application()

    # Start the program
    root.mainloop()
