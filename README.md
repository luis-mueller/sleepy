# sleepy
`sleepy` is a Python tool for semi-automatic slow wave detection and labelling. Its user interface is built for data augmentation and helps the user to quickly eliminate false-positives that are usually detected by purely automated approaches.

The project consists of two parts. The `sleepy.processing` package provides a range of algorithms for slow wave detection, a bandpass filter,
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

To start using `sleepy`, please run the commands below. These will clone the
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

## Quickstart GUI

This quick tutorial walks you through the most important features of the `sleepy` GUI application
and demonstrates how you can work with your dataset using this tool.
Upon running `sleepy`, you can open a new dataset by navigating to `File -> Open` as demonstrated in the following
picture or by using the shortcut `Ctrl + O`. Note that the examples are taken from the Windows version of `sleepy`.
For shortcuts for Mac please refer to the section [Keyboard-Shortcuts](#keyboard-shortcuts).

![initial-screen][initial-screen]


[checkpoints-message]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/checkpoints-message.png
[initial-screen]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/initial-screen.png
[preprocessing-choosing-algorithm]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/preprocessing-choosing-algorithm.png
[preprocessing-choosing-filter]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/preprocessing-choosing-filter.png
[preprocessing-compute-hit]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/preprocessing-compute-hit.png
[preprocessing-dataset-selection]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/preprocessing-dataset-selection.png
[preprocessing-screen]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/preprocessing-screen.png
[settings-open]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/settings-open.png
[settings-show-case]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/settings-show-case.png
[tagging-at-first-sight]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/tagging-at-first-sight.png
[tagging-tagging-an-event]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/tagging-tagging-an-event.png
[tagging-user-event-create]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/tagging-user-event-create.png
[tagging-user-event-remove]: https://github.com/pupuis/sleepy/docs/quickstart-screenshots/tagging-user-event-remove.png

## Keyboard-Shortcuts

The `sleepy` GUI supports the following keyboard-shortcuts:

* ```Ctrl+O / ⌘+O``` to open a new dataset
* ```Left``` and ```Right``` arrow keys to navigate backward and forward between the events.
* ```Ctrl+P / ⌘+P``` or the ```Up``` key to tag the selected event in the tagging environment
* ```A``` for navigating backwards through channels and ```D``` for navigating forward through channels.
* ```Ctrl+Q``` to open the settings on Windows and ```⌘+,``` on Mac
