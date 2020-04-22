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

A file-chooser window opens. Once a dataset file is opened, `sleepy` opens the following preprocessing window which
lets you change/verify the path to the dataset, select a filter and an algorithm and their respective parameters, which looks as follows:

![preprocessing-dataset-selection][preprocessing-dataset-selection] ![preprocessing-choosing-filter][preprocessing-choosing-filter]
![preprocessing-choosing-algorithm][preprocessing-choosing-algorithm]

As you can see from the pictures it is not mandatory to apply a filter or an algorithm. However, note that if you do not select an algorithm,
then you can only tag events that are already stored in the dataset.

Once you are finished setting up the preprocessing parameters, you can choose, by pressing the `Compute` button, to let `sleepy` compute the events and inform you of how many events were found, as can be seen in the following picture:

![preprocessing-compute-hit][preprocessing-compute-hit]

However, to actually plot the detected events and start tagging them, you need to load the events into the UI by pressing the `Load` button.

If no events can be found, either because no algorithm was applied and the dataset does not
contain any previously computed events or because the algorithm was applied but unsuccessful in its search, `sleepy` shows an error message to inform you of this.
Otherwise the algorithm has found at least one event and plots this in the main window, as you can see here:

![tagging-at-first-sight][tagging-at-first-sight]

The event in the picture marks an interval were the event occured. At the moment there exist exactly two types of events, said interval events and point events, which mark
a specific point in time as the event. Before continuing from here, you should take a look at the settings. You can open the settings as follows or by using the shortcut `Ctrl+Q` on Windows or the respective shortcut on Mac:

![settings-open][settings-open]

Beside general settings for the application, you find options to customize your plots permanently (in contrast to the temporal changes you can make in the integrated `matplotlib` toolbar) and the possibility to adjust the visible area around the event. As you can see in the following picture the visible is set to 10 seconds before and after the events occurs. Note that you cannot view more than the current epoch allows, i.e. you might increase the visible area without a visible effect which might be because the plot has reached the end of the epoch.

![settings-visible-area][settings-visible-area]

To apply the changes, hit the `Save` button.

We will now turn back to the detected and plotted events. Using the arrow keys of your keyboard or the `Previous` and `Next` buttons on the screen you can navigate between event in the same channel, across all epochs. To switch between channels, you can use the `D` key for navigating backwards and the `A` key for navigating forwards.
The navigation will always select exactly one event by marking the event with a designated color (which can also be customized in the settings). If you select an event that has been detected by the algorithm but you visually recognize that the underlying data does not indicate a slow-wave you can tag the event as a false-positive by pressing the corresponding button, as you can see in the following picture, or by pressing either `Ctrl+P` or the `Up` key. To revert the tag simply hit the button again.

![tagging-tagging-an-event][tagging-tagging-an-event]

Besides navigating with the arrow keys you can also jump to a location in the entire recording by double clicking the timeline below the plotted event. Note that you can also use the toolbar with the timeline, as this it is also drawn on a `matplotlib` canvas. However, you might encounter the case were the history of toolbar actions is cleared but the timeline remains in, e.g. a zoomed in, state. Then, by right-clicking anywhere on the timeline, you can reset the timeline to again show the entire recording.

If you visually detect an event while navigating through the data that has not been detected by the algorithm, you have the possibility to mark this event manually. Note the following. These events are so-called user events which can only be represented by a point, not by an interval. Further, the events are stored separately in the dataset such that they are identified as user events even after loading the dataset again. Note also that a user event cannot be tagged.
You can create an user-event by double-clicking on the respective point on the graph in the main window, which causes the following context menu to appear:

![tagging-user-event-create][tagging-user-event-create]

By selecting the corresponding menu entry, a user event is created and displayed immediately. To revert the action, simply double-click on the user event as follows:

![tagging-user-event-remove][tagging-user-event-remove]

By selecting the corresponding menu entry, the user event will be removed.

You can save your work by either selecting the respective menu entry under `File -> Save` or by pressing `Ctrl+S`. If you activated the usage of checkpoints in the settings, then the following message appears before closing the current dataset:

![checkpoints-message][checkpoints-message]

Checkpoints are references to your last position in the navigation grid that are stored in the dataset. These references consist of the index of the channel and the index of the event in that channel from where you are trying to close the dataset. This feature might be helpful when wanting to continue from the same position another time without having to remember at which event you closed the dataset. Note that checkpoints might be selecting the wrong event if you have reprocessed the dataset or added or removed user events in the mean time.

This concludes our walkthrough. At last, a humble wish from my side. If you are using `sleepy` and encounter any issues, e.g. in the form of crashes, unexpected or unwanted behaviour, please report the bug to us. This helps us constantly improve the application and increase the long-term quality of the `sleepy` software. When reporting a bug, you should add a potential error message you received and always attach a small description of the steps necessary to reproduce the issue. Only then can we reliably spot the erros and correct them.

Thank you.

[checkpoints-message]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/checkpoints-message.PNG
[initial-screen]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/initial-screen.PNG
[preprocessing-choosing-algorithm]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/preprocessing-choosing-algorithm.PNG
[preprocessing-choosing-filter]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/preprocessing-choosing-filter.PNG
[preprocessing-compute-hit]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/preprocessing-compute-hit.PNG
[preprocessing-dataset-selection]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/preprocessing-dataset-selection.PNG
[preprocessing-screen]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/preprocessing-screen.PNG
[settings-open]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/settings-open.PNG
[settings-show-case]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/settings-show-case.PNG
[settings-visible-area]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/settings-visible-area.PNG
[tagging-at-first-sight]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/tagging-at-first-sight.PNG
[tagging-tagging-an-event]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/tagging-tagging-an-event.PNG
[tagging-user-event-create]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/tagging-user-event-create.PNG
[tagging-user-event-remove]: https://github.com/pupuis/sleepy/blob/master/docs/quickstart-screenshots/tagging-user-event-remove.PNG

## Keyboard-Shortcuts

The `sleepy` GUI supports the following keyboard-shortcuts:

* ```Ctrl+O / ⌘+O``` to open a new dataset
* ```Left``` and ```Right``` arrow keys to navigate backward and forward between the events.
* ```Ctrl+P / ⌘+P``` or the ```Up``` key to tag the selected event in the tagging environment
* ```A``` for navigating backwards through channels and ```D``` for navigating forward through channels.
* ```Ctrl+Q``` to open the settings on Windows and ```⌘+,``` on Mac
