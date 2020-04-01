# sleepy
A python tool for slow wave detection and labelling.

## Walkthorugh: Implementing and Integration an Algorithm
This walkthrough takes you through the steps necessary to extend the existing
algorithm library with a new implementation.

### The Algorithm Class
Every algorithm implementation should inherit from the `Algorithm` super-class.
This class can be imported as follows:

```python
from sleepy.processing.algorithms.core import Algorithm
```

This class abstracts the embedding of every algorithm instance into the processing
engine, which calls the algorithm to process epochs of data.

### The Algorithm Metadata
Together with your `.py` file containing the implementation, you can store the
entire metadata of your algorithm in a `.json` file. In its simplest form this
metadata looks as follows:

```json
{
  "name" : "New Detector"
}
```

In the section we will see how to extend this file with a description of
user-supplied paramters.

#### User-Supplied Parameters
If your algorithm implementation depends on parameters that the user should be
able to choose before executing it, then you need to provide a `PyQt5` widget
that will be embedded into the processing window at runtime. Note, however, that
this can be abstracted using the algorithm base class `Algorithm`. For this we
need to extend the algorithm metadata with parameters. A parameter can be described
as in the following example:

```json
"floatParameter" : {
  "title" : "This is a floating-point parameter",
  "fieldType" : "float",
  "default" : 1.0
}
```

Adding this parameter to the `Algorithm` instance will create a new
class attribute `floatParameter` with default value `1.0`. Further,
this parameter will be displayed in the pre-processing window of `sleepy` and if the user changes the value of the parameter on the screen, `floatParameter` will be update automatically.
To extend the metadata with such parameters add the following lines
to the `.json` file:

```json
{
  "name" : "New Detector",
  "parameters": {
    "title": "Parameters",
    "fields": {
      "floatParameter": {
        "title": "This is a floating-point parameter",
        "fieldType": "float",
        "default": 1.0
      },
      "boolParameter": {
        "title": "This is a boolean parameter",
        "fieldType": "bool",
        "default": false
      },
      "negativeHeight": {
        "title": "Another floating-point parameter",
        "fieldType": "float",
        "default": 30.0
      }
    }
  }
}
```

Note that the list of parameters are stored with the key `fields`.

### Setting Up the Algorithm Implementation
We are now set to create a new implementation. We call the algorithm `NewDetector` and begin with the following code-stub,
setting the attributes that we defined in the metadata dynamically. To do so
we call the parent method `setAttributesRelative`, if the metadata is stored inside of
the `sleepy` package or `setAttributes` else.

```python
from sleepy.processing.algorithms.core import Algorithm

class NewDetector(Algorithm):

  def __init__(self, engine):

    self.setAttributesRelative('path/to/my/algorithm/newDetector.json')
```

The only other thing we need to do now is to implement the method `compute`,
which takes an instance of the `Signal` class as its only argument and returns
a list with samples at which we detected an event. This result will then be
converted and plotted automatically.
Before we continue let us quickly turn to the specifics of the `Signal` class.
This class abstracts an epoch of recorded data and has a couple of built-in
functionality. We can access the data as a `numpy` array via `Signal.data`.
Additional attributes are `zeroCrossings`, which returns a list of samples at which
there happens a zero-crossing, and `positivePeaks` which returns all samples where the
corresponding amplitude is greater or equal than `0`.
Further, the method `getNegativePeaks` returns a list of samples whose amplitudes are
lower or equal to a negative height which has to be supplied as an argument to
`getNegativePeaks`. For each negative peak the method `findValley` tries to find
two positive peaks surrounding the negative peak and return an instance of the `Valley`
class. The following implementation is an example for how to use these methods.
If you would like to process the data yourself you always have full access to it
via the `data` attribute of the `Signal` instance.
