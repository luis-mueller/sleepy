# sleepy
A python tool for slow wave detection and labelling.

## Walkthorugh: Implementing and Integrating an Algorithm
This walkthrough takes you through the steps necessary to extend the existing
algorithm library with a new implementation. Except for the next section, this
walkthough does not distinguish between integrating an algorithm as a
contribution to the `sleepy` project or as a stand-alone implementation.
However, if you are a contributor to `sleepy`, then follow the following
guidelines for integrating a new algorithm.

### Contributors Only: Before You Start
In the folder `sleepy/processing/algorithms` create a new folder for your
algorithm. Then, inside of that folder, create an empty `__init__.py` file and
a `.py` file for your algorithm. To add the algorithm to the list of supported
algorithms import your algorithm class in the file `sleepy/processing/supported.py`
and add the class (not an instance of it) to the list `SUPPORTED_ALGORITHMS`.

### The Algorithm Class
Every algorithm implementation must inherit from the `Algorithm` super-class.
This class can be imported as follows:

```python
from sleepy.processing.algorithms.core import Algorithm
```

This class abstracts the embedding of every algorithm instance into the processing
engine, which calls the algorithm to process epochs of data.
In the following example we create an algorithm class for an algorithm named
"My Detector", which serves us as a minimal example. For the user to be able to see our algorithm we must supply this
name in the attribute `name` of our implementation class. Further in order for the engine
to use our implementation we must add an instance method `compute` with one argument.

```python
from sleepy.processing.algorithms.core import Algorithm

class MyDetector(Algorithm):

  def __init__(self):

    self.name = "My Detector"

  def compute(self, signal):

    # our implementation
    ...
```

This definition is enough to see the algorithm on the screen and execute it
without a runtime error. In the next section we will extend our implementation
with user-supplied parameters.

### User-Supplied Parameters
The `sleepy` framework offers an interface for the user to change algorithm  
parameters in a pre-processing screen. We will now demonstrate how to declare
such parameters in our algorithm implementation. To configure a parameter we
must declare an instance attribute and assign it an instance of the `Parameter`
class from `sleepy.processing.algorithms.parameters`. The constructor of this
class takes three arguments: `title`, `fieldType` and `default`. It is necessary
to supply all of these arguments when creating a parameter. The value of `title`
is a short-description of the parameter that will be displayed next to its
value field. The value of `fieldType` decides the type of value that the user can
change, determining the widget that we will use in the frontend. Supported values
for this field are:
```python

# Displays an integer spinner in the frontend
int

# Displays a double spinner in the frontend with two decimals
float

# Displays a checkbox in the frontend
bool
```

The value of `default` determines the initial value that is assigned to the
parameter. Note that this value must be compatible with the `fieldType`, as otherwise
`sleepy` will throw an error.

The following example shows how we can extend our implementation of "My Detector"
with two parameters: Integer value `alpha` and floating-point value `beta`.

```python
from sleepy.processing.algorithms.core import Algorithm
from sleepy.processing.algorithms.parameter import Parameter

class MyDetector(Algorithm):

  def __init__(self):

    self.name = "My Detector"

    self.alpha = Parameter(
        title = "Integer parameter alpha",
        fieldType = int,
        default = 5
    )

    self.beta = Parameter(
        title = "Floating-point parameter beta",
        fieldType = float,
        default = 1.2
    )

  def compute(self, signal):

    # our implementation
    ...
```

This will render a box on the pre-processing screen, once the user selects our
algorithm, containing the parameters `alpha` and `beta` and the corresponding
spinner widgets.
The renderer will replace the instances of `Parameter` with our default values and
also update the attributes if the user changes them on the screen. This means that
once the user executes our algorithm and the `compute` method is called by the engine
the selected parameter values are set to the corresponding attributes of our `MyDetector`-
instance and we can use them in our computation.

### Working With Signals and the Compute Method
We will now discuss in detail how we can implement the `compute` method.
Apart from the reference to our instance, `self`, we are receiving an instance of the
`sleepy.processing.signal.Signal` class. This instance serves two purposes.
First, it stores all relevant information like the actual data points and the sampling
rate and second, it gives us an interface to do computations on the data points.
For example, we can get a list of the samples whose corresponding
amplitudes have a
specified negative peak, using the `getNegativePeaks`-method. Please refer to the implementation of `sleepy.processing.signal.Signal` for
detailed information about which computations are offered.

```python

# Hint: You can access the data points supplied by the engine via
signal.data
```

To create renderable events from our results we must return the events that our
implementation found in a specific form such that there exists a sub-class of
the `sleepy.tagging.model.event.core.Event` class which expects an object representing
sample values. Currently there are two such events: `PointEvent` and `IntervalEvent`.
The `PointEvent` expects a sample value at which the event happens, the `IntervalEvent`
expects a 2-tuple of sample values between which the event happens. Feel free to
contribute to `sleepy` by implementing more event types.
The following code snippet gives two examples of a return value for the `compute`
method, one with detected points and one with detected intervals:

```python
import numpy as np

# will cause three instance of `PointEvent` which are displayed to the user
return np.array([3, 19, 120])

# will cause three instance of `IntervalEvent` which are displayed to the user
return np.array([
  [3, 8],
  [19, 26],
  [120, 131]
])
```

Note that the sample values are relative to the signal we are processing. That means
that the sample value is always equal to the index in the `signal.data` array.
The engine will take care of recovering the absolute sample values, in case there
are multiple signals in one dataset, which could be different epochs or different channels.

### A Minimal Example
We conclude this walkthrough by implementing a very basic algorithm that detects
an event if the amplitude of the data point is greater than `alpha` and smaller than
`beta`.

```python
from sleepy.processing.algorithms.core import Algorithm
from sleepy.processing.algorithms.parameter import Parameter

class MyDetector(Algorithm):

  def __init__(self):

    self.name = "My Detector"

    self.alpha = Parameter(
        title = "Integer parameter alpha",
        fieldType = int,
        default = 5
    )

    self.beta = Parameter(
        title = "Floating-point parameter beta",
        fieldType = float,
        default = 1.2
    )

  def compute(self, signal):

    # Declare an inner function that can be used as a filter
    def isEvent(sample):

      # Get the amplitude for a given sample value
      amplitude = signal.data[sample]

      # Returns true if the filter condition is satisfied
      return amplitude > self.alpha and amplitude < self.beta

    signalLength = len(signal.data)

    # List comprehension to filter all the samples that satisfy our filter
    # condition
    return np.array([ sample for sample in range(signalLength) if isEvent(sample) ])
```
