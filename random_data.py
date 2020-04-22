
from sleepy.test.data import TestSignal
from sleepy.processing.algorithms.massimi import Massimi
from sleepy.processing.filters.bandpass.core import BandPassFilter
import matplotlib.pyplot as plt

# Prepare the algorithm and filter instances (we keep the standard values)
algorithm = Massimi().render()
filter = BandPassFilter().render()

# Create the x- and y-axis data of a signal with std. dev. 2, 300 samples per sub-wave and 50 sub-waves.
x, y = TestSignal.generate(scale = 2, numberOfSamples = 300, size=50)

# Plot the data
plt.plot(x, y)
plt.show()
