
class Application(QApplication):

    def __init__(self):

        super().__init__(list())

        self.main = QMainWindow()

        self.main.show()

        UI.setup(self, self.main)

        self.exec_()

    def openDataset(self):

        path = self.getPath()

        dataset = self.loadDataset(path)

        # eventsFound : 26 * 526 * 5000 array
        eventContainer = self.process(dataset)

        self.displayEvents()

    def displayEvents(self):

        self.event = eventsFound[0]

        stack.setWidget()



        connect.nextClick(self.next)

    def next(self):

        # ring ...
        pass
