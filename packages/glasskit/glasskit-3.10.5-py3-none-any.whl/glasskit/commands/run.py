from . import Command


class Run(Command):

    def run(self):
        self.app.run(debug=True)
