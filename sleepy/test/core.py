
from unittest.mock import MagicMock, Mock, patch, PropertyMock

class TestBase:
    """Provides a set of constructors for different sleepy objects, potentially
    as MagicMock's. These constructors can be nested such that the usage in
    unit- and integration-tests is very flexible, i.e. objects to test can
    simply not be created via the :class:`TestBase`.
    """

    def getBasics(active, name):

        settings = TestBase.getSettings()

        app = TestBase.getApp(settings, name)

        env = TestBase.getEnvironment(app, active)

        return env, app, settings

    def getEnvironment(view, app, active):

        env = MagicMock()
        env.view = view
        env.app = app
        env.active = active
        return env

    def getApp(settings, name = 'TestApplication'):

        app = MagicMock()
        app.name = name
        app.settings = settings
        return app

    def getSettings():

        settings = MagicMock()
        settings.setWindowTitle = MagicMock()
        settings.showIndex = False
        settings.useCheckpoints = False
        return settings

    def getView():

        view = MagicMock()
        view.setButtonStyle = MagicMock()
        return view

    def getNavigator(events, changesMade = False):

        return Navigator(events, changesMade)

    def getDataset():

        return MagicMock()

    def getFileLoader(path = "", dataset = None, navigator = None):

        loader = MagicMock()
        loader.path = path
        loader.app = self.app
        loader.load = MagicMock(return_value=([navigator], dataset))
        return loader

    def getDataSource(filter = 1, samplingRate = 10, interval = (0,100)):

        return DataSource(
            np.arange(*interval, 1),
            np.arange(*interval, 1) / filter,
            interval,
            samplingRate = samplingRate
        )

    def getEvents(points, settings, dataSource = None):

        return [ PointEvent(point, dataSource, settings) for point in points ]
