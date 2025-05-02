from typing import Sequence, override
import mobase
import sys

from PyQt6.QtCore import qInfo

class HelloWorldPlugin(mobase.IPlugin):
    _organizer: mobase.IOrganizer
    
    def __init__(self):
        print("Initializing HelloWorldPlugin")
        super().__init__()

    @override
    def init(self, organizer: mobase.IOrganizer) -> bool:
        self._organizer = organizer
        print("Print logs at DEBUG level")
        print("Errors go to ERROR level", file=sys.stderr)
        qInfo("This one way to put things into the logs at INFO level")
        return True

    @override
    def name(self):
        return "Python: Hello World Plugin"

    @override
    def author(self):
        return "Your Name"

    @override
    def description(self):
        return "A simple plugin for Mod Organizer 2"

    @override
    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.FINAL)

    @override
    def settings(self) -> Sequence[mobase.PluginSetting]:
        return []
        
def createPlugin() -> mobase.IPlugin:
    return HelloWorldPlugin()