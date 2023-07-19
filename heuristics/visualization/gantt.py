#!/usr/bin/env python
# pylint: disable=R0902, R0903, C0103

"""
Gantt.py is a simple class to render Gantt charts.

Disclaimer: This module was taken from somewhere a long time ago.
The original author is unknown.
"""

import os
import json
import platform
from operator import sub

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# TeX support: on Linux assume TeX in /usr/bin, on OSX check for texlive
if (platform.system() == 'Darwin') and 'tex' in os.getenv("PATH"):
    LATEX = True
elif (platform.system() == 'Linux') and os.path.isfile('/usr/bin/latex'):
    LATEX = True
else:
    LATEX = False

# setup pyplot w/ tex support
if LATEX:
    rc('text', usetex=True)


class Package():
    """Encapsulation of a work package

    A work package is instantiated from a dictionary. It **has to have**
    a label, astart and an end. Optionally it may contain milestones
    and a color

    :arg str pkg: dictionary w/ package data name
    """
    def __init__(self, pkg):

        DEFCOLOR = "#32AEE0"

        self.label = pkg['label']
        self.start = pkg['start']
        self.end = pkg['end']
        self.resource = pkg['resource']

        if self.start < 0 or self.end < 0:
            raise ValueError("Package cannot begin at t < 0")
        if self.start > self.end:
            raise ValueError("Cannot end before started")

        try:
            self.milestones = pkg['milestones']
        except KeyError:
            pass

        try:
            self.color = pkg['color']
        except KeyError:
            self.color = DEFCOLOR

        try:
            self.legend = pkg['legend']
        except KeyError:
            self.legend = None


class Gantt():
    """Gantt
    Class to render a simple Gantt chart, with optional milestones
    """
    def __init__(self, dataFile):
        """ Instantiation

        Create a new Gantt using the data in the file provided
        or the sample data that came along with the script

        :arg str dataFile: file holding Gantt data
        """
        self.dataFile = dataFile

        # some lists needed
        self.packages = []
        self.labels = []

        self._loadData()
        self._procData()

    def _loadData(self):
        """ Load data from a JSON file that has to have the keys:
            packages & title. Packages is an array of objects with
            a label, start and end property and optional milesstones
            and color specs.
        """

        # load data
        with open(self.dataFile) as fh:
            data = json.load(fh)

        # must-haves
        self.title = data['title']

        for pkg in data['packages']:
            self.packages.append(Package(pkg))

        self.labels = [pkg['label'] for pkg in data['packages']]

        self.resources = [pkg['resource'] for pkg in data['packages']]

        # optionals
        self.milestones = {}
        for pkg in self.packages:
            try:
                self.milestones[pkg.label] = pkg.milestones
            except AttributeError:
                pass

        try:
            self.xlabel = data['xlabel']
            # TODO: Add dynamic xtick + labeling according to latest day of finishing a project (project time)

        except KeyError:
            self.xlabel = ""
        try:
            self.ylabel = data['ylabel']
        except KeyError:
            self.ylabel = ""
        try:
            #self.xticks = data['xticks']
            self.xticks = list(range(1, max(pkg.end for pkg in self.packages) + 1))
        except KeyError:
            self.xticks = ""

    def _procData(self):
        """ Process data to have all values needed for plotting
        """
        # parameters for bars
        self.nPackages = len(self.labels)
        self.start = [None] * self.nPackages
        self.end = [None] * self.nPackages

        for pkg in self.packages:
            idx = self.labels.index(pkg.label)
            self.start[idx] = pkg.start
            self.end[idx] = pkg.end

        self.durations = map(sub, self.end, self.start)
        self.yPos = np.arange(self.nPackages, 0, -1)

    def format(self):
        """ Format various aspect of the plot, such as labels,ticks, BBox
        :todo: Refactor to use a settings object
        """
        # format axis
        plt.tick_params(
            axis='both',    # format x and y
            which='both',   # major and minor ticks affected
            bottom='on',    # bottom edge ticks are on
            top='off',      # top, left and right edge ticks are off
            left='off',
            right='off')

        # tighten axis but give a little room from bar height
        plt.xlim(0, max(self.end))
        plt.ylim(1, self.nPackages + 1)

        # add title
        self.yticks = self.yPos
        plt.title(self.title)

        if self.xlabel:
            plt.xlabel(self.xlabel)

        if self.ylabel:
            plt.ylabel(self.ylabel)

        if self.xticks:
            plt.xticks(self.xticks, map(str, self.xticks))

        # Rotate x tick labels so that largest numbers fit
        plt.xticks(rotation=45, ha='right')

        # Add package names as labels
        # Major ticks
        self.ax.set_yticks(self.yPos)

        # Labels for major ticks (empty strings)
        self.ax.set_yticklabels(["   " for x in self.labels])

        # Minor ticks
        # Arange for minor ticks to be in the correct position
        yticks = np.arange(1.5, len(self.yPos) + 1, 1)
        self.ax.set_yticks(yticks, minor=True)
        labels_modified = reversed(self.labels)
        self.ax.set_yticklabels(labels_modified, minor=True)

    def add_milestones(self):
        """Add milestones to GANTT chart.
        The milestones are simple yellow diamonds
        """

        if not self.milestones:
            return

        x = []
        y = []
        for key in self.milestones.keys():
            for value in self.milestones[key]:
                y += [self.yPos[self.labels.index(key)]]
                x += [value]

        plt.scatter(x, y, s=120, marker="D",
                    color="yellow", edgecolor="black", zorder=3)

    def add_legend(self):
        """Add a legend to the plot iff there are legend entries in
        the package definitions
        """

        cnt = 0
        for pkg in self.packages:
            if pkg.legend:
                cnt += 1
                idx = self.labels.index(pkg.label)
                self.barlist[idx].set_label(pkg.legend)

        if cnt > 0:
            self.legend = self.ax.legend(
                shadow=False, ncol=3, fontsize="medium")

    def add_resource_requirements(self):
        """Add a resourse requirements to the plot iff there are resource requirements in
        the package definitions
        """
        reversed_package_list = list(reversed([x for x in self.packages]))
        cnt = 0
        for pkg in reversed_package_list:
            if pkg.resource:
                cnt += 1
                for i in range(pkg.start, pkg.end):
                    self.ax.text(i + 0.3, cnt + 0.35, pkg.resource, color='black', fontweight='bold')

    def render(self):
        """ Prepare data for plotting
        """

        # init figure
        self.fig, self.ax = plt.subplots(figsize=(10,5))
        self.ax.yaxis.grid(True)
        self.ax.xaxis.grid(True)

        # assemble colors
        colors = []
        for pkg in self.packages:
            colors.append(pkg.color)

        self.barlist = plt.barh(self.yPos, list(self.durations),
                                left=self.start,
                                align='edge',
                                height=1,
                                alpha=1,
                                color="none",
                                edgecolor="black")

        # format plot
        self.format()
        self.add_milestones()
        self.add_legend()
        self.add_resource_requirements()

    @staticmethod
    def show():
        """ Show the plot
        """
        plt.show()

    @staticmethod
    def save(saveFile='img/GANTT.png'):
        """ Save the plot to a file. It defaults to `img/GANTT.png`.

        :arg str saveFile: file to save to
        """
        plt.savefig(saveFile, bbox_inches='tight')


if __name__ == '__main__':
    g = Gantt('sample.json')
    g.render()
    g.show()
    # g.save('img/GANTT.png')
