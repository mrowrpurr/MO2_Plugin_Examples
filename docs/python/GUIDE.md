# Mod Organizer 2 Python Plugin Development Guide

This guide provides step-by-step instructions for developing plugins for Mod Organizer 2 using Python. It covers everything from setting up your development environment to creating and testing your plugins.

## Table of Contents

- [Mod Organizer 2 Python Plugin Development Guide](#mod-organizer-2-python-plugin-development-guide)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setting Up Your Development Environment](#setting-up-your-development-environment)
    - [Prerequisites](#prerequisites)
    - [Setting Up Your Project](#setting-up-your-project)
  - [Creating Your First Plugin](#creating-your-first-plugin)
    - [Basic Plugin Structure](#basic-plugin-structure)
    - [Plugin Registration](#plugin-registration)
    - [Testing Your Plugin](#testing-your-plugin)
  - [Plugin Types](#plugin-types)
    - [Tool Plugins](#tool-plugins)
    - [Game Plugins](#game-plugins)
    - [Installer Plugins](#installer-plugins)
    - [Preview Plugins](#preview-plugins)
    - [Mod Page Plugins](#mod-page-plugins)
  - [Working with the Mod Organizer 2 API](#working-with-the-mod-organizer-2-api)
    - [IOrganizer Interface](#iorganizer-interface)
    - [Working with Mods](#working-with-mods)
    - [Working with Profiles](#working-with-profiles)
    - [Working with the Virtual File System](#working-with-the-virtual-file-system)
  - [Working with Qt](#working-with-qt)
    - [Creating Widgets](#creating-widgets)
    - [Signals and Slots](#signals-and-slots)
    - [Layouts](#layouts)
    - [Dialogs](#dialogs)
  - [Advanced Topics](#advanced-topics)
    - [Creating Multiple Plugins](#creating-multiple-plugins)
    - [Plugin Settings](#plugin-settings)
    - [Error Handling](#error-handling)
    - [Logging](#logging)
    - [Internationalization](#internationalization)
  - [Best Practices](#best-practices)
    - [Modular Plugin Architecture](#modular-plugin-architecture)
    - [Code Organization](#code-organization)
    - [Performance](#performance)
    - [User Experience](#user-experience)
    - [Compatibility](#compatibility)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Debugging](#debugging)
  - [Conclusion](#conclusion)

## Introduction

Mod Organizer 2 (MO2) provides a powerful plugin system that allows developers to extend its functionality. While plugins can be written in C++, Python offers a more accessible and rapid development experience. This guide will walk you through the process of creating plugins for MO2 using Python.

The Python plugin system for MO2 consists of three main components:

1. **Python Proxy Plugin**: A C++ plugin that interfaces with MO2
2. **Python Runner**: A library that manages the Python interpreter and loads/unloads Python plugins
3. **Python Bindings (mobase)**: A Python module that provides access to the MO2 API

With these components, you can create plugins that integrate seamlessly with MO2 and provide new functionality to users.

## Setting Up Your Development Environment

### Prerequisites

Before you start developing plugins for MO2, you'll need the following:

1. **Mod Organizer 2**: You'll need a working installation of MO2 to test your plugins.
2. **Python**: MO2 comes with its own Python installation, so you don't need to install Python separately.
3. **Text Editor or IDE**: Any text editor or IDE that supports Python will work. Visual Studio Code, PyCharm, and Sublime Text are popular choices.

### Setting Up Your Project

To set up your project, follow these steps:

1. Create a new directory for your plugin in the `plugins` directory of your MO2 installation. For example, `C:\Program Files\Mod Organizer 2\plugins\my_plugin`.

2. Create a new Python file in this directory. For a single-file plugin, you can name it anything with a `.py` extension. For a module plugin, create a directory with an `__init__.py` file.

3. Set up your development environment to work with the MO2 Python API. If you're using an IDE, you may want to configure it to use the Python interpreter that comes with MO2.

## Creating Your First Plugin

### Basic Plugin Structure

A basic MO2 plugin in Python consists of a class that implements one of the plugin interfaces and a function that creates and returns an instance of this class. Here's a simple example of a tool plugin:

```python
import mobase
from PyQt6.QtCore import QCoreApplication, qCritical
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

class MyFirstPlugin(mobase.IPluginTool):
    def __init__(self):
        super().__init__()
        self.__organizer = None
        self.__parentWidget = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "My First Plugin"

    def author(self):
        return "Your Name"

    def description(self):
        return "A simple plugin for Mod Organizer 2"

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.final)

    def settings(self):
        return []

    def displayName(self):
        return "My First Plugin"

    def tooltip(self):
        return "A simple plugin for Mod Organizer 2"

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self.__parentWidget = widget

    def display(self):
        QMessageBox.information(self.__parentWidget, "My First Plugin", "Hello, world!")

def createPlugin():
    return MyFirstPlugin()
```

This plugin implements the `IPluginTool` interface, which is used for plugins that add tools to the MO2 tools menu. The `createPlugin()` function is called by MO2 to create an instance of the plugin.

### Plugin Registration

MO2 discovers and loads Python plugins through the Python proxy plugin. The proxy plugin looks for Python files in the `plugins` directory and calls their `createPlugin()` or `createPlugins()` function to create plugin instances.

For a single-file plugin, the file should define a `createPlugin()` function that returns a single plugin instance, or a `createPlugins()` function that returns a list of plugin instances.

For a module plugin, the `__init__.py` file should define these functions.

### Testing Your Plugin

To test your plugin, follow these steps:

1. Save your plugin file in the `plugins` directory of your MO2 installation.
2. Start MO2.
3. If your plugin is a tool plugin, you should see it in the tools menu.
4. Click on your plugin to test it.

If your plugin doesn't appear or doesn't work as expected, check the MO2 log for error messages. The log can be accessed from the MO2 main window by clicking on the "!" icon in the top right corner.

## Plugin Types

MO2 supports several types of plugins, each with its own interface and purpose. Here are the main types of plugins you can create:

### Tool Plugins

Tool plugins add new tools to the MO2 tools menu. They implement the `IPluginTool` interface and provide a way to perform actions on the MO2 installation.

```python
class MyToolPlugin(mobase.IPluginTool):
    # ... implementation ...
```

### Game Plugins

Game plugins add support for new games to MO2. They implement the `IPluginGame` interface and provide information about the game, such as its name, directory, and executable.

```python
class MyGamePlugin(mobase.IPluginGame):
    # ... implementation ...
```

### Installer Plugins

Installer plugins add support for new mod installation methods to MO2. They implement the `IPluginInstaller` interface and provide a way to install mods from archives.

There are two types of installer plugins:

1. **Simple Installer Plugins**: These plugins implement the `IPluginInstallerSimple` interface and are used for simple installation tasks.

```python
class MySimpleInstallerPlugin(mobase.IPluginInstallerSimple):
    # ... implementation ...
```

2. **Custom Installer Plugins**: These plugins implement the `IPluginInstallerCustom` interface and are used for more complex installation tasks.

```python
class MyCustomInstallerPlugin(mobase.IPluginInstallerCustom):
    # ... implementation ...
```

### Preview Plugins

Preview plugins add support for previewing files in MO2. They implement the `IPluginPreview` interface and provide a way to generate previews for files.

```python
class MyPreviewPlugin(mobase.IPluginPreview):
    # ... implementation ...
```

### Mod Page Plugins

Mod page plugins add support for new mod repositories to MO2. They implement the `IPluginModPage` interface and provide a way to browse and download mods from repositories.

```python
class MyModPagePlugin(mobase.IPluginModPage):
    # ... implementation ...
```

## Working with the Mod Organizer 2 API

The MO2 API provides access to various aspects of MO2, such as mods, profiles, and the virtual file system. Here's how to work with some of the key parts of the API:

### IOrganizer Interface

The `IOrganizer` interface is the main entry point to the MO2 API. It provides access to various aspects of MO2, such as mods, profiles, and the virtual file system.

```python
def init(self, organizer):
    self.__organizer = organizer
    return True
```

### Working with Mods

The `IOrganizer` interface provides access to the list of mods through the `modList()` method. You can use this to get information about installed mods, enable or disable mods, and more.

```python
def listMods(self):
    modList = self.__organizer.modList()
    for modName in modList.allModsByProfilePriority():
        print(f"Mod: {modName}, Priority: {modList.priority(modName)}")
```

### Working with Profiles

The `IOrganizer` interface provides access to the current profile through the `profile()` method. You can use this to get information about the current profile, such as its name, directory, and enabled mods.

```python
def getProfileInfo(self):
    profile = self.__organizer.profile()
    print(f"Profile: {profile.name()}")
    print(f"Directory: {profile.absolutePath()}")
```

### Working with the Virtual File System

The `IOrganizer` interface provides access to the virtual file system through the `virtualFileSystem()` method. You can use this to get information about files in the virtual file system, such as their real paths and whether they are overwritten by mods.

```python
def getFileInfo(self, path):
    vfs = self.__organizer.virtualFileSystem()
    info = vfs.getFileInfo(path)
    print(f"Real Path: {info.realPath()}")
    print(f"Overwritten: {info.isOverwritten()}")
```

## Working with Qt

MO2 uses Qt for its user interface, and the Python bindings provide access to Qt through PyQt6. Here's how to work with some of the key parts of Qt:

### Creating Widgets

You can create Qt widgets to build user interfaces for your plugins. Here's an example of creating a simple dialog with a label and a button:

```python
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Dialog")
        
        layout = QVBoxLayout()
        
        label = QLabel("Hello, world!")
        layout.addWidget(label)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        layout.addWidget(button)
        
        self.setLayout(layout)
```

### Signals and Slots

Qt uses signals and slots for communication between objects. In PyQt6, you can connect signals to slots using the `connect()` method:

```python
button.clicked.connect(self.onButtonClicked)

def onButtonClicked(self):
    print("Button clicked!")
```

### Layouts

Qt provides various layout managers to arrange widgets in a user interface. Here's an example of using a grid layout:

```python
from PyQt6.QtWidgets import QGridLayout

layout = QGridLayout()
layout.addWidget(widget1, 0, 0)  # Row 0, Column 0
layout.addWidget(widget2, 0, 1)  # Row 0, Column 1
layout.addWidget(widget3, 1, 0)  # Row 1, Column 0
layout.addWidget(widget4, 1, 1)  # Row 1, Column 1
```

### Dialogs

Qt provides various dialog classes for common tasks, such as file dialogs, message boxes, and input dialogs. Here's an example of using a file dialog:

```python
from PyQt6.QtWidgets import QFileDialog

fileName, _ = QFileDialog.getOpenFileName(self.__parentWidget, "Open File", "", "All Files (*)")
if fileName:
    print(f"Selected file: {fileName}")
```

## Advanced Topics

### Creating Multiple Plugins

You can create multiple plugins in a single file or module by implementing the `createPlugins()` function instead of `createPlugin()`. This function should return a list of plugin instances:

```python
def createPlugins():
    return [MyToolPlugin(), MyGamePlugin(), MyInstallerPlugin()]
```

### Plugin Settings

Plugins can define settings that users can configure through the MO2 settings dialog. To define settings, implement the `settings()` method to return a list of `PluginSetting` objects:

```python
def settings(self):
    return [
        mobase.PluginSetting("enabled", "Enable this plugin", True),
        mobase.PluginSetting("option1", "Option 1", "default value"),
        mobase.PluginSetting("option2", "Option 2", 42)
    ]
```

To access these settings in your plugin, use the `pluginSetting()` method of the `IOrganizer` interface:

```python
def getSetting(self, name):
    return self.__organizer.pluginSetting(self.name(), name)
```

### Error Handling

When developing plugins, it's important to handle errors gracefully to prevent crashes and provide useful feedback to users. Here's an example of error handling in a plugin:

```python
def display(self):
    try:
        # Do something that might fail
        result = self.doSomething()
        QMessageBox.information(self.__parentWidget, "Success", f"Result: {result}")
    except Exception as e:
        QMessageBox.critical(self.__parentWidget, "Error", f"An error occurred: {str(e)}")
```

### Logging

MO2 provides a logging system that you can use to log messages from your plugin. To log messages, use the `log()` method of the `IOrganizer` interface:

```python
def logMessage(self, message, level=mobase.log.DEBUG):
    mobase.log.debug(message)
    mobase.log.info(message)
    mobase.log.warning(message)
    mobase.log.error(message)
```

### Internationalization

MO2 supports internationalization through Qt's translation system. To make your plugin translatable, use the `QCoreApplication.translate()` function for all user-visible strings:

```python
def tr(self, text):
    return QCoreApplication.translate("MyPlugin", text)

def displayName(self):
    return self.tr("My Plugin")
```

## Best Practices

### Modular Plugin Architecture

After examining several well-designed MO2 plugins like Shortcutter, Root Builder, and Profile Sync, we can identify a common modular architecture pattern that promotes maintainability and reusability:

1. **Base Components**: Create base classes that provide common functionality for all plugins:
   - `BasePlugin`: A base class for all plugins that implements common methods
   - `BaseSettings`: A class for managing plugin settings
   - `BaseDialog`: A class for creating consistent dialogs

2. **Common Components**: Create utility classes that can be reused across plugins:
   - `CommonLog`: A class for logging with different severity levels
   - `CommonPaths`: A class for handling path operations
   - `CommonStrings`: A class for managing string constants and operations
   - `CommonUtilities`: A class for common utility functions

3. **Core Components**: Create classes that implement the core functionality of your plugin:
   - Main class (e.g., `Shortcutter`, `RootBuilder`): Orchestrates the plugin functionality
   - Settings class (e.g., `ShortcutterSettings`): Manages plugin-specific settings
   - Paths class (e.g., `ShortcutterPaths`): Handles plugin-specific path operations
   - Strings class (e.g., `ShortcutterStrings`): Manages plugin-specific string constants

4. **Plugin Implementations**: Create classes that implement specific plugin interfaces:
   - Tool plugins (e.g., `ShortcutterManager`): Implement `IPluginTool`
   - Game plugins: Implement `IPluginGame`
   - Installer plugins: Implement `IPluginInstaller`

5. **UI Components**: Create classes for the user interface:
   - Menu classes (e.g., `ShortcutterMenu`): Provide the main UI
   - Dialog classes: Provide specific dialogs
   - Widget classes: Provide reusable UI components

This modular architecture allows for:
- **Reusability**: Common components can be reused across plugins
- **Maintainability**: Each component has a clear responsibility
- **Extensibility**: New functionality can be added by creating new components
- **Testability**: Components can be tested in isolation

Here's an example of how to structure a plugin using this architecture:

```
my_plugin/
├── __init__.py                 # Plugin registration
├── base/
│   ├── base_plugin.py          # Base plugin class
│   ├── base_settings.py        # Base settings class
│   └── base_dialog.py          # Base dialog class
├── common/
│   ├── common_log.py           # Logging utilities
│   ├── common_paths.py         # Path utilities
│   ├── common_strings.py       # String utilities
│   └── common_utilities.py     # General utilities
├── core/
│   ├── my_plugin.py            # Main plugin class
│   └── my_plugin_settings.py   # Plugin settings
├── modules/
│   ├── my_plugin_paths.py      # Plugin-specific paths
│   └── my_plugin_strings.py    # Plugin-specific strings
└── plugins/
    └── my_plugin_manager.py    # IPluginTool implementation
```

### Code Organization

When developing plugins, it's important to organize your code in a way that makes it easy to understand and maintain. Here are some best practices:

1. **Use classes**: Organize your code into classes that implement the appropriate plugin interfaces.
2. **Separate concerns**: Keep different aspects of your plugin in separate classes or modules.
3. **Use descriptive names**: Use descriptive names for classes, methods, and variables.
4. **Document your code**: Add comments to explain complex or non-obvious parts of your code.
5. **Follow a consistent structure**: Use a consistent structure for your plugins, such as the modular architecture described above.

### Performance

When developing plugins, it's important to consider performance to ensure that your plugin doesn't slow down MO2. Here are some best practices:

1. **Avoid unnecessary operations**: Don't perform operations that aren't necessary.
2. **Cache results**: Cache the results of expensive operations to avoid repeating them. The Shortcutter plugin uses the `@cached_property` decorator for properties that don't change often.
3. **Use efficient algorithms**: Use efficient algorithms and data structures.
4. **Avoid blocking the UI**: Perform long-running operations in a separate thread to avoid blocking the UI. The Profile Sync plugin uses threading for asynchronous operations.
5. **Implement retry mechanisms**: For file operations that might fail due to timing issues, implement retry mechanisms with exponential backoff. The Shortcutter plugin's `CommonUtilities` class implements this pattern.

### User Experience

When developing plugins, it's important to consider the user experience to ensure that your plugin is easy to use. Here are some best practices:

1. **Provide clear feedback**: Let users know what your plugin is doing and whether it succeeded or failed.
2. **Handle errors gracefully**: Handle errors in a way that doesn't crash MO2 and provides useful feedback to users.
3. **Respect user preferences**: Respect user preferences and settings.
4. **Follow MO2 conventions**: Follow the conventions and patterns used by MO2 to provide a consistent experience.
5. **Support both Qt5 and Qt6**: MO2 can be built with either Qt5 or Qt6. The Shortcutter plugin demonstrates how to support both versions:

```python
try:
    from PyQt5.QtCore import QCoreApplication, qInfo, qDebug, qWarning, qCritical
except:
    from PyQt6.QtCore import QCoreApplication, qInfo, qDebug, qWarning, qCritical
```

6. **Provide update checking**: Allow users to check for updates to your plugin. The Shortcutter plugin demonstrates a simple update checking mechanism that fetches a JSON file from GitHub.

### Compatibility

When developing plugins, it's important to consider compatibility to ensure that your plugin works with different versions of MO2 and on different systems. Here are some best practices:

1. **Check API versions**: Check the version of the MO2 API to ensure that your plugin is compatible.
2. **Handle platform differences**: Handle differences between platforms, such as file paths and system calls.
3. **Test on different systems**: Test your plugin on different systems to ensure that it works correctly.
4. **Provide fallbacks**: Provide fallbacks for features that may not be available on all systems.
5. **Support both portable and non-portable MO2 installations**: The Shortcutter plugin demonstrates how to handle both portable and non-portable MO2 installations by checking for the instance name:

```python
@cached_property
def moInstanceName(self) -> str:
    """Gets the name of the current Mod Organizer instance. Empty if portable."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\Mod Organizer Team\\Mod Organizer",) as key:
            value = winreg.QueryValueEx(key, "CurrentInstance")
            return str(value[0]).replace("/", "\\")
    except:
        return ""
```

## Troubleshooting

### Common Issues

Here are some common issues that you might encounter when developing plugins for MO2:

1. **Plugin not loading**: Make sure that your plugin file is in the correct directory and has the correct name. Check the MO2 log for error messages.
2. **Plugin crashing**: Make sure that your plugin handles errors gracefully and doesn't have any bugs. Check the MO2 log for error messages.
3. **Plugin not working as expected**: Make sure that your plugin is implemented correctly and follows the MO2 API conventions. Check the MO2 log for error messages.

### Debugging

To debug your plugin, you can use the following techniques:

1. **Print statements**: Add print statements to your code to see what's happening.
2. **Logging**: Use the MO2 logging system to log messages from your plugin.
3. **Debugger**: Use a debugger to step through your code and inspect variables.
4. **Error handling**: Add error handling to your code to catch and report errors.

## Conclusion

Developing plugins for MO2 using Python is a powerful way to extend its functionality and provide new features to users. By following the guidelines and best practices in this guide, you can create plugins that integrate seamlessly with MO2 and provide a great user experience.

Remember to check the MO2 documentation and source code for more information about the API and how to use it. The MO2 community is also a great resource for help and inspiration.

Happy plugin development!
