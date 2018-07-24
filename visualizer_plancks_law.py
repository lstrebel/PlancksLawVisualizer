#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This is a small graphical program to visualize the black body radiation.
The black body radiation is calculated using the wavelength form of Planck's law.

This software was also used to learn some basic GUI programming with PyQT5.
Very helpful in this were the answers in
https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies.

Also helpful were these tutorials:
- https://www.tutorialspoint.com/pyqt/
- https://pythonspot.com/pyqt5/
- http://zetcode.com/gui/pyqt5/


Copyright (c) 2018 Lukas Strebel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import sys
from PyQt5.QtWidgets import (QPushButton, QDialog, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QApplication, QLabel, QMessageBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import numpy as np


class PlancksLaw:
    """ Class containing the constants, conversion parameters, and the function
        to compute the black body radiation according to Planck's law.
    """
    # Constants
    h = 6.62606957 * 10.0 ** (-34.0)
    c = 2.99792458 * 10.0 ** 8.0
    kb = 1.3806488 * 10.0 ** (-23.0)

    # Conversion
    m_to_micrometer = 1.0e6

    @staticmethod
    def plancks_law_function(temperature, wavelength):
        """ Planck's law function returns the black body radiation for a given temperature and wavelength.

        :param temperature: Temperature in Kelvin
        :param wavelength: Wavelength in Meter
        :return: Black body radiation in W sr^-1 m^-3
        """
        return ((2.0 * PlancksLaw.h * PlancksLaw.c ** 2.0) / (wavelength ** 5.0)
                * (1.0 / (np.exp((PlancksLaw.h * PlancksLaw.c) / (wavelength * PlancksLaw.kb * temperature)) - 1.0)))


class Window(QDialog):
    """ Main GUI class for the matplotlib visualization and parameter controls.
    """
    def __init__(self, parent=None):
        """ Initialize the main window.

        :param parent: Parent window.
        """
        super(Window, self).__init__(parent)

        # Figure instance to plot on
        self.figure = plt.figure()
        # create an axis
        self.ax = self.figure.add_subplot(111)
        # The Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(self.figure)

        # The Navigation widget
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Refresh plot button
        self.button = QPushButton("Refresh plot")
        self.button.clicked.connect(self.plot)

        # NPP control
        self.npp_label = QLabel("Number of plot points [int]:")
        self.npp_box = QLineEdit(self)
        self.npp_box.setText("300")

        # Temperature control
        self.temp_label = QLabel("Temperature [K]: ")
        self.temp_box = QLineEdit(self)
        self.temp_box.setText("288.0")

        # Wavelength range control
        self.wl_lower_label = QLabel("Wavelength [m] from ")
        self.wl_box_lower = QLineEdit(self)
        self.wl_box_lower.setText("5.0e-6")
        self.wl_upper_label = QLabel(" to ")
        self.wl_box_upper = QLineEdit(self)
        self.wl_box_upper.setText("20.0e-6")

        # Setting up the layout of the Window
        self.hbox0 = QHBoxLayout()
        self.hbox0.addWidget(self.button)
        self.hbox0.addWidget(self.npp_label)
        self.hbox0.addWidget(self.npp_box)
        self.hbox0.addStretch(1)

        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.temp_label)
        self.hbox1.addWidget(self.temp_box)
        self.hbox1.addStretch(1)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.wl_lower_label)
        self.hbox2.addWidget(self.wl_box_lower)
        self.hbox2.addWidget(self.wl_upper_label)
        self.hbox2.addWidget(self.wl_box_upper)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        # Finalize the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.vbox)
        self.setLayout(self.layout)

    def check_input(self):
        """ Small helper function to check if the input in the textfields is valid at a given point.

        :return: True if valid inputs are given. Error messages and False if the inputs are invalid.
        """
        npp_value = int(self.npp_box.text())
        if npp_value < 100:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid number of plot points input")
            msg.setInformativeText("Should have more than 100 plot points for good visual results.")
            msg.setWindowTitle("Invalid number of plot points input")
            msg.exec_()
            return False

        temp_value = float(self.temp_box.text())
        if temp_value < 0.0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid temperature input")
            msg.setInformativeText("Temperature needs to be positive value. [Kelvin]")
            msg.setWindowTitle("Invalid temperature input")
            msg.exec_()
            return False

        wl_lower = float(self.wl_box_lower.text())
        wl_upper = float(self.wl_box_upper.text())
        if wl_lower > wl_upper:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid wavelength input")
            msg.setInformativeText("Lower wavelength needs to be smaller than larger wavelength.")
            msg.setWindowTitle("Invalid wavelength input")
            msg.exec_()
            return False

        return True

    def plot(self):
        """Function to create plots according to the given valid inputs.
        This function is called if the 'plot' button is pressed.
        """
        if self.check_input():
            # Get values from input fields
            temp_value = float(self.temp_box.text())
            wl_lower = float(self.wl_box_lower.text())
            wl_upper = float(self.wl_box_upper.text())

            npp = int(self.npp_box.text())

            # Create arrays for plot
            wave_linspace = np.linspace(wl_lower, wl_upper, npp)
            blackbody_radiation = np.zeros(len(wave_linspace))

            # Calculate all values
            for w in range(len(wave_linspace)):
                blackbody_radiation[w] = PlancksLaw.plancks_law_function(temp_value, wave_linspace[w])

            # Plot the curve
            self.ax.plot(wave_linspace * PlancksLaw.m_to_micrometer, blackbody_radiation[:])

            # Set axis labels
            self.ax.set_xlabel(r"Wavelength $\mu m$")
            self.ax.set_ylabel(r"Black body radiation $W sr^{-1} m^{-3}$", rotation="horizontal")
            self.ax.yaxis.set_label_coords(0.2, 1.05)

            # Tighten the plot
            self.figure.tight_layout()

            # Refresh canvas
            self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
