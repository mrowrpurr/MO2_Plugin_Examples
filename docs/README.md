# Mod Organizer 2 Plugin Development Overview

This document provides a high-level overview of plugin development for Mod Organizer 2 (MO2). It's intended as a starting point for developers interested in creating plugins for MO2.

## Table of Contents
- [Mod Organizer 2 Plugin Development Overview](#mod-organizer-2-plugin-development-overview)
  - [Table of Contents](#table-of-contents)
  - [What is MO2?](#what-is-mo2)
  - [What is a MO2 Plugin?](#what-is-a-mo2-plugin)
    - [Plugin Types](#plugin-types)
  - [Python vs C++: Which to Choose?](#python-vs-c-which-to-choose)
    - [Python](#python)
    - [C++](#c)
  - [API Overview](#api-overview)
    - [Python API](#python-api)
    - [Basic Games API](#basic-games-api)
    - [C++ API](#c-api)
    - [UIBASE API](#uibase-api)
    - [Gamebryo API](#gamebryo-api)
  - [Conclusion](#conclusion)

## What is MO2?

Mod Organizer 2 (MO2) is an advanced mod manager for games that support file-based modding. Its key features include:

- **Virtual File System**: MO2 uses a virtual file system to manage mods, allowing them to override game files without actually modifying them. This enables easy enabling/disabling of mods without conflicts.
- **Profile System**: Users can create different profiles with different mod configurations for the same game.
- **Plugin Management**: MO2 can manage game plugins (e.g., .esp, .esm files for Bethesda games) and their load order.
- **Extensibility**: MO2 has a plugin system that allows developers to extend its functionality.

MO2 is primarily designed for Bethesda games (Skyrim, Fallout, etc.) but can be used with many other games through its plugin system.

## What is a MO2 Plugin?

A MO2 plugin is a module that extends the functionality of Mod Organizer 2. Plugins can be written in C++ or Python and can interact with MO2's core systems to provide additional features.

### Plugin Types

MO2 supports several types of plugins:

1. **Tool Plugins (`IPluginTool`)**: Add new tools to MO2's toolbar. These can be simple utilities or complex applications that interact with the game or mods.

2. **Game Plugins (`IPluginGame`)**: Add support for new games to MO2. These plugins define how MO2 should interact with a specific game, including file paths, plugin management, and game-specific features.

3. **Installer Plugins (`IPluginInstaller`)**: Customize how mods are installed. These can handle specific mod formats or provide custom installation options.

4. **Preview Plugins (`IPluginPreview`)**: Provide previews for mod files directly in MO2's interface.

5. **Mod Page Plugins (`IPluginModPage`)**: Add support for downloading mods from specific websites or repositories.

6. **File Mapper Plugins (`IPluginFileMapper`)**: Customize how MO2 maps files from mods to the virtual file system.

7. **Diagnosis Plugins (`IPluginDiagnose`)**: Add custom diagnostics to help users identify and fix issues with their mod setup.

Plugins can also create custom UI elements, including:
- Toolbar buttons
- Menu items
- Dialog windows
- Custom tabs in the main interface
- Settings pages

## Python vs C++: Which to Choose?

MO2 plugins can be written in either Python or C++. Each has its advantages and disadvantages:

### Python

**Advantages:**
- Easier to develop and iterate
- No need to compile
- Access to Python's extensive library ecosystem
- Simpler syntax and lower learning curve
- Can be modified without restarting MO2

**Disadvantages:**
- Slower performance for intensive operations
- Limited access to low-level system features
- Dependent on MO2's Python API, which may not expose all functionality

**Best for:**
- Simple tools and utilities
- UI-focused plugins
- Plugins that don't require high performance
- Rapid prototyping
- Plugins developed by users with limited C++ experience

### C++

**Advantages:**
- Better performance for intensive operations
- Full access to MO2's internal API
- Can use any C++ library
- Can implement more complex functionality

**Disadvantages:**
- More complex development process
- Requires compilation
- Steeper learning curve
- Changes require recompiling and restarting MO2

**Best for:**
- Performance-critical plugins
- Plugins that need deep integration with MO2
- Game support plugins
- Plugins that use C++ libraries without Python bindings

**General Recommendation:**
- Start with Python for simpler plugins or if you're new to MO2 development
- Use C++ for complex plugins or if you need maximum performance
- Consider a hybrid approach for complex plugins: core functionality in C++, UI in Python

## API Overview

### Python API

The Python API provides access to MO2's functionality through the `mobase` module. This module exposes interfaces for interacting with MO2's core systems.

**Key Features:**
- Access to the organizer interface (`IOrganizer`)
- Mod management through `IModList` and `IModInterface`
- Plugin management through `IPluginList`
- File system operations through the virtual file system
- Game feature access through `IGameFeatures`
- Profile management through `IProfile`
- Qt integration for UI development

**Example Plugin Structure:**
```python
import mobase

class MyTool(mobase.IPluginTool):
    def __init__(self):
        super().__init__()
        self._organizer = None
        
    def init(self, organizer):
        self._organizer = organizer
        return True
        
    def name(self):
        return "My Tool"
        
    def displayName(self):
        return "My Tool"
        
    # Other required methods...
        
    def display(self):
        # Tool functionality here
        pass

def createPlugin():
    return MyTool()
```

### Basic Games API

The Basic Games API is a Python framework for adding support for new games to MO2. It simplifies the process of creating game plugins by providing a base class with common functionality.

**Key Features:**
- Easy game detection (Steam, GOG, Epic, Origin, EA Desktop)
- Simplified game feature implementation
- Automatic handling of common game files
- Support for game variants
- Customizable game settings

**Example Game Plugin:**
```python
from PyQt6.QtCore import QDir
import mobase
from basic_game import BasicGame

class MyGamePlugin(BasicGame):
    Name = "My Game"
    Author = "Plugin Author"
    Version = "1.0.0"
    
    GameName = "My Game"
    GameShortName = "mygame"
    GameBinary = "MyGame.exe"
    GameDataPath = "data"
    
    # Other game-specific settings...

def createPlugin():
    return MyGamePlugin()
```

### C++ API

The C++ API provides direct access to MO2's internal systems. It's more powerful than the Python API but also more complex.

**Key Components:**
- Plugin interfaces (`IPlugin`, `IPluginTool`, etc.)
- Organizer interface (`IOrganizer`)
- Mod management interfaces (`IModList`, `IModInterface`)
- Plugin management interface (`IPluginList`)
- Virtual file system interfaces
- Game feature interfaces

**Example Plugin Structure:**
```cpp
#include <iplugin.h>
#include <iplugintool.h>
#include <imoinfo.h>

class MyTool : public MOBase::IPluginTool {
public:
    MyTool();
    
    // IPlugin interface
    bool init(MOBase::IOrganizer *organizer) override;
    QString name() const override;
    QString author() const override;
    QString description() const override;
    MOBase::VersionInfo version() const override;
    QList<MOBase::PluginSetting> settings() const override;
    
    // IPluginTool interface
    QString displayName() const override;
    QString tooltip() const override;
    QIcon icon() const override;
    void display() const override;
    
private:
    MOBase::IOrganizer *m_Organizer;
};

// Plugin registration
extern "C" DLLEXPORT QList<MOBase::IPlugin*> createPlugins() {
    return QList<MOBase::IPlugin*>() << new MyTool();
}
```

### UIBASE API

The UIBASE API provides the core interfaces and utilities for MO2 plugins. It's the foundation for both C++ and Python plugins.

**Key Components:**
- Plugin interfaces (`IPlugin`, `IPluginTool`, etc.)
- Organizer interface (`IOrganizer`)
- Mod management interfaces (`IModList`, `IModInterface`)
- Plugin management interface (`IPluginList`)
- File system utilities
- UI utilities
- Logging and diagnostics

The UIBASE API is primarily used by C++ plugins, but its interfaces are also exposed to Python through the `mobase` module.

### Gamebryo API

The Gamebryo API provides specialized functionality for Bethesda's Gamebryo/Creation Engine games (Morrowind, Oblivion, Skyrim, Fallout 3, Fallout: New Vegas, Fallout 4, etc.).

**Key Features:**
- BSA/BA2 archive handling
- Plugin (ESP/ESM/ESL) management
- Load order management
- Save game handling
- Script extender integration
- Game-specific file formats

**Example Usage:**
```cpp
// C++ example for a Gamebryo game plugin
#include <gamebryogameplugins.h>
#include <gamebryosavegame.h>

class MyGamePlugin : public GameGamebryo {
public:
    // Game-specific implementations
    
    // Example: Custom plugin management
    std::shared_ptr<GamebryoGamePlugins> plugins() const override {
        return std::make_shared<MyGamePlugins>(this);
    }
    
    // Example: Custom save game handling
    std::shared_ptr<SaveGameInfo> savegameInfo() const override {
        return std::make_shared<MyGameSaveGameInfo>(this);
    }
};
```

```python
# Python example using Gamebryo features through mobase
def init(self, organizer):
    self._organizer = organizer
    game = self._organizer.managedGame()
    
    # Check if game is a Gamebryo game
    if isinstance(game, mobase.IPluginGame) and game.gameName() in ["Skyrim", "Fallout4"]:
        # Access game-specific features
        plugins = self._organizer.pluginList()
        for plugin in plugins.pluginNames():
            if plugins.isMasterFlagged(plugin):
                print(f"{plugin} is a master file")
```

## Conclusion

MO2's plugin system offers a flexible and powerful way to extend its functionality. Whether you choose Python or C++ depends on your specific needs, experience, and the complexity of your plugin.

For more detailed information on specific APIs and plugin types, refer to the dedicated documentation files:
- `PYTHON_DOCUMENTATION.md` for Python API details
- `BASIC_GAMES_DOCUMENTATION.md` for Basic Games API details
- `MO_UIBASE_DOCUMENTATION.md` for UIBASE API details
- `GAMEBRYO_DOCUMENTATION.md` for Gamebryo API details

Happy plugin development!
