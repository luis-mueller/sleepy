# sleepy
`sleepy` is a python tool for slow wave detection and labelling. The project consists of
two parts. The `sleepy.processing` package provides a range of algorithms for slow wave detection, a bandpass filter,
an I/O adapter for `.mat` files exported from [fieldtrip](http://www.fieldtriptoolbox.org/) and an engine
that embedds these algorithms, ulitmately allowing for custom algorithm implementations
without the need to load, parse and format the data.
The `sleepy.gui` package provides a cross-platform GUI-extension for `sleepy.processing`, making it possible to
run algorithms on a graphical user-interface, plot detected events, adding manual events on the data
and tagging events as false-positives.
`sleepy` stores the filtered data, the (either automatically or manually) detected events and the
tags associated with these events together with the dataset loaded, such that the work on tagging and/or adding events
can be continued upon reloading the resulting file from any machine.

## Installation

To start using `sleepy`, please execute the commands below. These will clone the
repository, install all dependencies. Note that you need
[python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/).

```
git clone https://github.com/pupuis/sleepy.git
cd sleepy
pip install -r requirements.txt
```

From here on, starting the `sleepy` GUI program is as easy as running the off-the-shelf
script, which is provided in the top-level-folder of `sleepy`.

```
python ots.py
```

## Keyboard-Shortcuts

The `sleepy` GUI supports the following keyboard-shortcuts:

* ```Ctrl+O``` to open a new dataset
* ```Ctrl+Q``` to open the settings on Windows and ```Command+L``` on Mac
* ```Ctrl+P``` or the ```Up``` key to tag the selected event in the tagging environment
* ```Left``` and ```Right``` to navigate backward and forward between the events.
* ```A``` for navigating backwards through channels and ```D``` for navigating forward through channels.
