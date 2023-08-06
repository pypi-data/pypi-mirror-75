import ipywidgets as widgets
from ipyfilechooser import FileChooser
import os
import numpy as np
import pandas as pd


class DrawWidgets(object):
    def __init__(self):
        self.style = {'description_width': 'initial'}

    def drawIntSlider(self, value, min=1, max=100, description="description", width="200pt"):
        widget = widgets.IntSlider(
            value=value,
            min=min,
            max=max,
            step=1,
            description=description,
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            style=self.style
        )
        widget.layout.width = width
        return widget

    def drawFloatSlider(self, value, min=0, max=1, description="description", width="200pt"):
        widget = widgets.FloatSlider(
            value=value,
            min=min,
            max=max,
            step=0.05,
            description=description,
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.2f',
            style=self.style
        )
        widget.layout.width = width
        return widget

    def mountMatrix(self, file):
        lines = str(file.data[0]).split('\\n')
        data = []
        for line in lines[:-1]:
            data.append(line.split(';'))
        columns = data[0]
        index = []
        numData = np.zeros((len(data)-1, len(data[0])-1))
        for i, row in enumerate(data[1:]):
            index.append(row[0])
            for j, num in enumerate(row[1:]):
                numData[i, j] = float(num)
        df = pd.DataFrame(numData)
        df.columns = columns[1:]
        df.index = index
        file.close()
        return df

    def mountyvector(self, filey):
        ystr = str(filey.data[0]).split('\\n')
        y = [float(num) for num in ystr[1:-1]]
        ystr[0][2:]
        y.insert(0, float(ystr[0][2:]))
        vec = np.zeros((len(y), 1))
        vec[:, 0] = np.array(y)
        filey.close()
        return vec
