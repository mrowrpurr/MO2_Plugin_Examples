# Basic Games Plugin Documentation

## Table of Contents

- [Basic Games Plugin Documentation](#basic-games-plugin-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Architecture Overview](#architecture-overview)
    - [Plugin Structure](#plugin-structure)
    - [Core Components](#core-components)
  - [Plugin Components](#plugin-components)
    - [BasicGame](#basicgame)
    - [BasicGameMapping](#basicgamemapping)
    - [BasicGameOptionsMapping](#basicgameoptionsmapping)
    - [BasicGameMappings](#basicgamemappings)
    - [BasicIniGame](#basicinigame)
  - [Game Features](#game-features)
    - [BasicGameSaveGameInfo](#basicgamesavegameinfo)
    - [BasicGameSaveGame](#basicgamesavegame)
  - [Game Implementation](#game-implementation)
    - [Python Implementation](#python-implementation)
    - [INI Implementation](#ini-implementation)
    - [Example: Witcher 3](#example-witcher-3)
  - [Game Detection](#game-detection)
    - [Steam Games](#steam-games)
    - [GOG Games](#gog-games)
    - [Origin Games](#origin-games)
    - [Epic Games](#epic-games)
    - [EA Desktop Games](#ea-desktop-games)
  - [Key Processes](#key-processes)
    - [Plugin Registration](#plugin-registration)
    - [Game Detection](#game-detection-1)
    - [Game Initialization](#game-initialization)
    - [Save Game Handling](#save-game-handling)
  - [Configuration](#configuration)
    - [Game Properties](#game-properties)
    - [Game Paths](#game-paths)
    - [Game Features](#game-features-1)
  - [Integration with Mod Organizer 2](#integration-with-mod-organizer-2)
    - [Plugin Registration](#plugin-registration-1)
    - [Game Support](#game-support)
  - [Conclusion](#conclusion)

## Introduction

The Basic Games plugin for Mod Organizer 2 provides a framework for adding support for games that are not natively supported by Mod Organizer 2. It allows developers to easily add support for new games without having to write a full C++ plugin, by using either Python or INI files to define the game's properties and behavior.

The plugin provides several key features:
- Easy addition of new games through Python or INI files
- Automatic detection of games installed through Steam, GOG, Origin, Epic Games, and EA Desktop
- Support for game-specific features like save games
- Integration with Mod Organizer 2's virtual file system

## Architecture Overview

### Plugin Structure

Basic Games follows a modular architecture with clear separation of concerns:

1. **Core Components**: Base classes that provide the core functionality
2. **Game Implementations**: Classes or INI files that define specific games
3. **Game Features**: Classes that provide game-specific features
4. **Utility Modules**: Classes that provide utility functions for the plugin

### Core Components

The core components of Basic Games are:

1. **BasicGame**: Base class for all game implementations
2. **BasicGameMapping**: Class that handles mapping game properties
3. **BasicGameOptionsMapping**: Class that handles mapping game properties with multiple options
4. **BasicGameMappings**: Class that manages all game mappings
5. **BasicIniGame**: Class that loads game definitions from INI files

## Plugin Components

### BasicGame

`BasicGame` is the base class for all game implementations. It inherits from `IPluginGame` and provides default implementations for many of the methods required by the interface.

Key features:
- Implements the `IPluginGame` interface
- Provides default implementations for many methods
- Handles game detection for various platforms (Steam, GOG, Origin, Epic, EA Desktop)
- Manages game paths and properties

```python
class BasicGame(mobase.IPluginGame):
    """This class implements some methods from mobase.IPluginGame
    to make it easier to create game plugins without having to implement
    all the methods of mobase.IPluginGame."""

    # List of steam, GOG, origin and Epic games:
    steam_games: dict[str, Path]
    gog_games: dict[str, Path]
    origin_games: dict[str, Path]
    epic_games: dict[str, Path]
    eadesktop_games: dict[str, Path]

    @staticmethod
    def setup():
        # Initialize game lists
        ...

    def __init__(self):
        super(BasicGame, self).__init__()
        self._fromName = self.__class__.__name__
        self._gamePath = ""
        self._mappings: BasicGameMappings = BasicGameMappings(self)

    def _register_feature(self, feature: mobase.GameFeature) -> bool:
        # Register a game feature
        ...

    # IPlugin interface:
    def init(self, organizer: mobase.IOrganizer) -> bool:
        # Initialize the plugin
        ...

    def name(self) -> str:
        return self._mappings.name.get()

    def author(self) -> str:
        return self._mappings.author.get()

    def description(self) -> str:
        return self._mappings.description.get()

    def version(self) -> mobase.VersionInfo:
        return self._mappings.version.get()

    def isActive(self) -> bool:
        # Check if the plugin is active
        ...

    def settings(self) -> list[mobase.PluginSetting]:
        return []

    # IPluginGame interface:
    def detectGame(self):
        # Detect the game installation
        ...

    def gameName(self) -> str:
        return self._mappings.gameName.get()

    def gameShortName(self) -> str:
        return self._mappings.gameShortName.get()

    def gameIcon(self) -> QIcon:
        # Get the game icon
        ...

    def validShortNames(self) -> list[str]:
        return self._mappings.validShortNames.get()

    def gameNexusName(self) -> str:
        return self._mappings.gameNexusName.get()

    def nexusModOrganizerID(self) -> int:
        return 0

    def nexusGameID(self) -> int:
        return self._mappings.nexusGameId.get()

    def steamAPPId(self) -> str:
        return self._mappings.steamAPPId.current()

    def gogAPPId(self) -> str:
        return self._mappings.gogAPPId.current()

    def epicAPPId(self) -> str:
        return self._mappings.epicAPPId.current()

    def eaDesktopContentId(self) -> str:
        return self._mappings.eaDesktopContentId.current()

    def binaryName(self) -> str:
        return self._mappings.binaryName.get()

    def getLauncherName(self) -> str:
        return self._mappings.launcherName.get()

    def getSupportURL(self) -> str:
        return self._mappings.supportURL.get()

    def iniFiles(self) -> list[str]:
        return self._mappings.iniFiles.get()

    def executables(self) -> list[mobase.ExecutableInfo]:
        # Get the list of executables
        ...

    def executableForcedLoads(self) -> list[mobase.ExecutableForcedLoadSetting]:
        return []

    def listSaves(self, folder: QDir) -> list[mobase.ISaveGame]:
        # List save games
        ...

    def initializeProfile(self, directory: QDir, settings: mobase.ProfileSetting) -> None:
        # Initialize a profile
        ...

    def setGameVariant(self, variant: str) -> None:
        pass

    def gameVersion(self) -> str:
        # Get the game version
        ...

    def looksValid(self, directory: QDir):
        return directory.exists(self.binaryName())

    def isInstalled(self) -> bool:
        return bool(self._gamePath)

    def gameDirectory(self) -> QDir:
        return QDir(self._gamePath)

    def dataDirectory(self) -> QDir:
        # Get the data directory
        ...

    def setGamePath(self, path: Path | str) -> None:
        # Set the game path
        ...

    def documentsDirectory(self) -> QDir:
        return self._mappings.documentsDirectory.get()

    def savesDirectory(self) -> QDir:
        return self._mappings.savesDirectory.get()
```

### BasicGameMapping

`BasicGameMapping` is a class that handles mapping game properties. It provides a way to map properties from the game implementation to the `IPluginGame` interface.

Key features:
- Maps properties from the game implementation to the `IPluginGame` interface
- Handles property validation and transformation
- Provides default values for optional properties

```python
class BasicGameMapping(Generic[_T]):
    # The game:
    _game: "BasicGame"

    # Name of the attribute for exposure:
    _exposed_name: str

    # Name of the internal method:
    _internal_method_name: str

    # Required:
    _required: bool

    # Callable returning a default value (if not required):
    _default: Callable[["BasicGame"], _T]

    # Function to apply to the value:
    _apply_fn: Callable[[_T | str], _T] | None

    def __init__(
        self,
        game: BasicGame,
        exposed_name: str,
        internal_method: str,
        default: Callable[[BasicGame], _T] | None = None,
        apply_fn: Callable[[_T | str], _T] | None = None,
    ):
        # Initialize the mapping
        ...

    def get(self) -> _T:
        """Return the value of this mapping."""
        # Get the value of the mapping
        ...
```

### BasicGameOptionsMapping

`BasicGameOptionsMapping` is a class that handles mapping game properties with multiple options. It extends `BasicGameMapping` to handle properties that can have multiple values, such as Steam App IDs.

Key features:
- Extends `BasicGameMapping` to handle properties with multiple options
- Provides methods to set and get the current option
- Handles option validation and transformation

```python
class BasicGameOptionsMapping(BasicGameMapping[list[_T]]):
    """
    Represents a game mappings for which multiple options are possible. The game
    plugin is responsible to choose the right option depending on the context.
    """

    _index: int

    def __init__(
        self,
        game: BasicGame,
        exposed_name: str,
        internal_method: str,
        default: Callable[[BasicGame], _T] | None = None,
        apply_fn: Callable[[list[_T] | str], list[_T]] | None = None,
    ):
        # Initialize the mapping
        ...

    def set_index(self, index: int):
        """
        Set the index of the option to use.

        Args:
            index: Index of the option to use.
        """
        # Set the index
        ...

    def set_value(self, value: _T):
        """
        Set the index corresponding of the given value. If the value is not present,
        the index is set to -1.

        Args:
            value: The value to set the index to.
        """
        # Set the value
        ...

    def has_value(self) -> bool:
        """
        Check if a value was set for this options mapping.

        Returns:
            True if a value was set, False otherwise.
        """
        # Check if a value was set
        ...

    def current(self) -> _T:
        # Get the current value
        ...
```

### BasicGameMappings

`BasicGameMappings` is a class that manages all game mappings. It provides a central place to define and access all the mappings for a game.

Key features:
- Manages all game mappings
- Provides default values for optional mappings
- Handles mapping validation and transformation

```python
class BasicGameMappings:
    name: BasicGameMapping[str]
    author: BasicGameMapping[str]
    version: BasicGameMapping[mobase.VersionInfo]
    description: BasicGameMapping[str]
    gameName: BasicGameMapping[str]
    gameShortName: BasicGameMapping[str]
    gameNexusName: BasicGameMapping[str]
    validShortNames: BasicGameMapping[list[str]]
    nexusGameId: BasicGameMapping[int]
    binaryName: BasicGameMapping[str]
    launcherName: BasicGameMapping[str]
    dataDirectory: BasicGameMapping[str]
    documentsDirectory: BasicGameMapping[QDir]
    iniFiles: BasicGameMapping[list[str]]
    savesDirectory: BasicGameMapping[QDir]
    savegameExtension: BasicGameMapping[str]
    steamAPPId: BasicGameOptionsMapping[str]
    gogAPPId: BasicGameOptionsMapping[str]
    originManifestIds: BasicGameOptionsMapping[str]
    originWatcherExecutables: BasicGameMapping[list[str]]
    epicAPPId: BasicGameOptionsMapping[str]
    eaDesktopContentId: BasicGameOptionsMapping[str]
    supportURL: BasicGameMapping[str]

    @staticmethod
    def _default_documents_directory(game: mobase.IPluginGame):
        # Get the default documents directory
        ...

    # Game mappings:
    def __init__(self, game: BasicGame):
        self._game = game

        # Initialize all mappings
        ...
```

### BasicIniGame

`BasicIniGame` is a class that loads game definitions from INI files. It extends `BasicGame` to provide a way to define games using INI files instead of Python classes.

Key features:
- Extends `BasicGame` to load game definitions from INI files
- Parses INI files to set game properties
- Provides a simple way to add new games without writing Python code

```python
class BasicIniGame(BasicGame):
    def __init__(self, path: str):
        # Set the _fromName to get more "correct" errors:
        self._fromName = os.path.basename(path)

        # Read the file:
        config = configparser.ConfigParser()
        config.optionxform = str  # type: ignore
        config.read(path)

        # Just fill the class with values:
        for k, v in config["DEFAULT"].items():
            setattr(self, k, v)

        super().__init__()
```

## Game Features

### BasicGameSaveGameInfo

`BasicGameSaveGameInfo` is a class that provides information about save games. It implements the `ISaveGameInfoWidget` interface to provide a way to display save game information in Mod Organizer 2.

### BasicGameSaveGame

`BasicGameSaveGame` is a class that represents a save game. It implements the `ISaveGame` interface to provide a way to interact with save games in Mod Organizer 2.

```python
class BasicGameSaveGame(mobase.ISaveGame):
    def __init__(self, filepath: Path):
        super().__init__()
        self._filepath = filepath

    def getFilepath(self) -> str:
        return str(self._filepath)

    def getName(self) -> str:
        return self._filepath.name

    def getSaveGroupIdentifier(self) -> str:
        return ""

    def allFiles(self) -> list[str]:
        return [self._filepath.name]
```

## Game Implementation

### Python Implementation

Games can be implemented in Python by creating a class that inherits from `BasicGame` and defines the necessary properties and methods.

```python
class MyGame(BasicGame):
    Name = "My Game Support Plugin"
    Author = "Me"
    Version = "1.0.0"

    GameName = "My Game"
    GameShortName = "mygame"
    GameNexusName = "mygame"
    GameNexusId = 1234
    GameSteamId = 5678
    GameBinary = "MyGame.exe"
    GameDataPath = "Data"
    GameSaveExtension = "sav"
    GameDocumentsDirectory = "%DOCUMENTS%/My Game"
    GameSavesDirectory = "%GAME_DOCUMENTS%/Saves"
```

### INI Implementation

Games can also be implemented using INI files, which are simpler but less flexible than Python implementations.

```ini
[DEFAULT]
Name=My Game Support Plugin
Author=Me
Version=1.0.0

GameName=My Game
GameShortName=mygame
GameNexusName=mygame
GameNexusId=1234
GameSteamId=5678
GameBinary=MyGame.exe
GameDataPath=Data
GameSaveExtension=sav
GameDocumentsDirectory=%DOCUMENTS%/My Game
GameSavesDirectory=%GAME_DOCUMENTS%/Saves
```

### Example: Witcher 3

Here's an example of a Python implementation for The Witcher 3:

```python
class Witcher3SaveGame(BasicGameSaveGame):
    def allFiles(self):
        return [self._filepath.name, self._filepath.name.replace(".sav", ".png")]


class Witcher3Game(BasicGame):
    Name = "Witcher 3 Support Plugin"
    Author = "Holt59"
    Version = "1.0.0a"

    GameName = "The Witcher 3: Wild Hunt"
    GameShortName = "witcher3"
    GaneNexusHame = "witcher3"
    GameNexusId = 952
    GameSteamId = [499450, 292030]
    GameGogId = [1640424747, 1495134320, 1207664663, 1207664643]
    GameBinary = "bin/x64/witcher3.exe"
    GameDataPath = "Mods"
    GameSaveExtension = "sav"
    GameDocumentsDirectory = "%DOCUMENTS%/The Witcher 3"
    GameSavesDirectory = "%GAME_DOCUMENTS%/gamesaves"
    GameSupportURL = (
        r"https://github.com/ModOrganizer2/modorganizer-basic_games/wiki/"
        "Game:-The-Witcher-3"
    )

    def init(self, organizer: mobase.IOrganizer):
        super().init(organizer)
        self._register_feature(BasicGameSaveGameInfo(lambda s: s.with_suffix(".png")))
        return True

    def iniFiles(self):
        return ["user.settings", "input.settings"]

    def listSaves(self, folder: QDir) -> List[mobase.ISaveGame]:
        ext = self._mappings.savegameExtension.get()
        return [
            Witcher3SaveGame(path)
            for path in Path(folder.absolutePath()).glob(f"*.{ext}")
        ]
```

## Game Detection

### Steam Games

The Basic Games plugin can detect games installed through Steam. It uses the Steam API to get the list of installed games and their installation paths.

```python
@staticmethod
def setup():
    from .steam_utils import find_games as find_steam_games
    from .gog_utils import find_games as find_gog_games
    from .origin_utils import find_games as find_origin_games
    from .epic_utils import find_games as find_epic_games
    from .eadesktop_utils import find_games as find_eadesktop_games

    errors: list[tuple[str, Exception]] = []
    BasicGame.steam_games = find_steam_games()
    BasicGame.gog_games = find_gog_games()
    BasicGame.origin_games = find_origin_games()
    BasicGame.epic_games = find_epic_games(errors)
    BasicGame.eadesktop_games = find_eadesktop_games(errors)

    if errors:
        QMessageBox.critical(
            None,
            "Errors loading game list",
            (
                "The following errors occurred while loading the list of available games:\n"
                f"\n- {'\n\n- '.join('\n '.join(str(e) for e in messageError) for messageError in errors)}"
            ),
        )
```

### GOG Games

The Basic Games plugin can detect games installed through GOG. It uses the GOG Galaxy API to get the list of installed games and their installation paths.

### Origin Games

The Basic Games plugin can detect games installed through Origin. It uses the Origin API to get the list of installed games and their installation paths.

### Epic Games

The Basic Games plugin can detect games installed through the Epic Games Store. It uses the Epic Games Store API to get the list of installed games and their installation paths.

### EA Desktop Games

The Basic Games plugin can detect games installed through EA Desktop. It uses the EA Desktop API to get the list of installed games and their installation paths.

## Key Processes

### Plugin Registration

The Basic Games plugin registers itself with Mod Organizer 2 by implementing the `createPlugins()` function. This function returns a list of plugin objects that Mod Organizer 2 can use.

```python
def createPlugins():
    # List of game class from python:
    game_plugins: typing.List[BasicGame] = []

    # We are going to list all game plugins:
    curpath = os.path.abspath(os.path.dirname(__file__))
    escaped_games_path = glob.escape(os.path.join(curpath, "games"))

    # List all the .ini files:
    for file in glob.glob(os.path.join(escaped_games_path, "*.ini")):
        game_plugins.append(BasicIniGame(file))

    # List all the python plugins:
    for file in glob.glob(os.path.join(escaped_games_path, "*.py")):
        module_p = os.path.relpath(file, os.path.join(curpath, "games"))
        if module_p == "__init__.py":
            continue

        # Import the module:
        try:
            module = importlib.import_module(".games." + module_p[:-3], __package__)
        except ImportError as e:
            print("Failed to import module {}: {}".format(module_p, e), file=sys.stderr)
        except Exception as e:
            print("Failed to import module {}: {}".format(module_p, e), file=sys.stderr)

        # Lookup game plugins:
        for name in dir(module):
            if hasattr(module, name):
                obj = getattr(module, name)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, BasicGame)
                    and obj is not BasicGame
                ):
                    try:
                        game_plugins.append(obj())
                    except Exception as e:
                        print(
                            "Failed to instantiate {}: {}".format(name, e),
                            file=sys.stderr,
                        )

    return game_plugins
```

### Game Detection

The game detection process is handled by the `detectGame()` method of the `BasicGame` class. This method checks if the game is installed through Steam, GOG, Origin, Epic Games, or EA Desktop, and sets the game path accordingly.

```python
def detectGame(self):
    for steam_id in self._mappings.steamAPPId.get():
        if steam_id in BasicGame.steam_games:
            self.setGamePath(BasicGame.steam_games[steam_id])
            return

    for gog_id in self._mappings.gogAPPId.get():
        if gog_id in BasicGame.gog_games:
            self.setGamePath(BasicGame.gog_games[gog_id])
            return

    for origin_manifest_id in self._mappings.originManifestIds.get():
        if origin_manifest_id in BasicGame.origin_games:
            self.setGamePath(BasicGame.origin_games[origin_manifest_id])
            return

    for epic_id in self._mappings.epicAPPId.get():
        if epic_id in BasicGame.epic_games:
            self.setGamePath(BasicGame.epic_games[epic_id])
            return

    for eadesktop_content_id in self._mappings.eaDesktopContentId.get():
        if eadesktop_content_id in BasicGame.eadesktop_games:
            self.setGamePath(BasicGame.eadesktop_games[eadesktop_content_id])
            return
```

### Game Initialization

The game initialization process is handled by the `init()` method of the `BasicGame` class. This method initializes the game plugin and registers any game features.

```python
def init(self, organizer: mobase.IOrganizer) -> bool:
    self._organizer = organizer

    self._register_feature(BasicGameSaveGameInfo())

    if self._mappings.originWatcherExecutables.get():
        from .origin_utils import OriginWatcher

        self.origin_watcher = OriginWatcher(
            self._mappings.originWatcherExecutables.get()
        )
        if not self._organizer.onAboutToRun(
            lambda appName: self.origin_watcher.spawn_origin_watcher()
        ):
            print("Failed to register onAboutToRun callback!", file=sys.stderr)
            return False
        if not self._organizer.onFinishedRun(
            lambda appName, result: self.origin_watcher.stop_origin_watcher()
        ):
            print("Failed to register onFinishedRun callback!", file=sys.stderr)
            return False
    return True
```

### Save Game Handling

The save game handling process is handled by the `listSaves()` method of the `BasicGame` class. This method lists all the save games in the specified folder.

```python
def listSaves(self, folder: QDir) -> list[mobase.ISaveGame]:
    ext = self._mappings.savegameExtension.get()
    return [
        BasicGameSaveGame(path)
        for path in Path(folder.absolutePath()).glob(f"**/*.{ext}")
    ]
```

## Configuration

### Game Properties

Game properties are defined in the game implementation, either in a Python class or an INI file. These properties include:

- **Name**: The name of the plugin
- **Author**: The author of the plugin
- **Version**: The version of the plugin
- **GameName**: The name of the game
- **GameShortName**: The short name of the game
- **GameNexusName**: The name of the game on Nexus Mods
- **GameNexusId**: The ID of the game on Nexus Mods
- **GameSteamId**: The Steam App ID of the game
- **GameGogId**: The GOG App ID of the game
- **GameBinary**: The name of the game's executable
- **GameDataPath**: The path to the game's data directory
- **GameSaveExtension**: The extension of the game's save files
- **GameDocumentsDirectory**: The path to the game's documents directory
- **GameSavesDirectory**: The path to the game's saves directory

### Game Paths

Game paths are handled by the `BasicGame` class. It provides methods to get and set the game path, as well as to get the data directory, documents directory, and saves directory.

```python
def gameDirectory(self) -> QDir:
    """
    @return directory (QDir) to the game installation.
    """
    return QDir(self._gamePath)

def dataDirectory(self) -> QDir:
    return QDir(
        self.gameDirectory().absoluteFilePath(self._mappings.dataDirectory.get())
    )

def setGamePath(self, path: Path | str) -> None:
    self._gamePath = str(path)

    path = Path(path)

    # Check if we have a matching steam, GOG, Origin or EA Desktop id and set the
    # index accordingly:
    for steamid, steampath in BasicGame.steam_games.items():
        if steampath == path:
            self._mappings.steamAPPId.set_value(steamid)
    for gogid, gogpath in BasicGame.gog_games.items():
        if gogpath == path:
            self._mappings.steamAPPId.set_value(gogid)
    for originid, originpath in BasicGame.origin_games.items():
        if originpath == path:
            self._mappings.originManifestIds.set_value(originid)
    for epicid, epicpath in BasicGame.epic_games.items():
        if epicpath == path:
            self._mappings.epicAPPId.set_value(epicid)
    for eadesktopid, eadesktoppath in BasicGame.eadesktop_games.items():
        if eadesktoppath == path:
            self._mappings.eaDesktopContentId.set_value(eadesktopid)

def documentsDirectory(self) -> QDir:
    return self._mappings.documentsDirectory.get()

def savesDirectory(self) -> QDir:
    return self._mappings.savesDirectory.get()
```

### Game Features

Game features are handled by the `_register_feature()` method of the `BasicGame` class. This method registers a game feature with Mod Organizer 2.

```python
def _register_feature(self, feature: mobase.GameFeature) -> bool:
    return self._organizer.gameFeatures().registerFeature(self, feature, 0, True)
```

## Integration with Mod Organizer 2

### Plugin Registration

The Basic Games plugin registers itself with Mod Organizer 2 by implementing the `createPlugins()` function. This function returns a list of plugin objects that Mod Organizer 2 can use.

### Game Support

The Basic Games plugin provides support for games by implementing the `IPluginGame` interface. This interface allows Mod Organizer 2 to interact with the game, such as detecting the game installation, getting the game's data directory, and listing save games.

## Conclusion

The Basic Games plugin for Mod Organizer 2 provides a powerful framework for adding support for games that are not natively supported by Mod Organizer 2. It allows developers to easily add support for new games without having to write a full C++ plugin, by using either Python or INI files to define the game's properties and behavior.

The plugin follows a modular architecture with clear separation of concerns, making it easy to understand and maintain. It integrates well with Mod Organizer 2, providing a seamless experience for users.
