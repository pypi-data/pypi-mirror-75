
import numpy as np
from figure_formating import FormatPlot as fp

x = np.arange(0, 10, 0.1)
y = np.sin(x)
fp.plot(x,y)

x1 = np.random.rand(100,1)
fp.hist(x1)
