# Mod Organizer 2 Tool Plugins Documentation

This document provides a detailed overview of how tool plugins are implemented in Mod Organizer 2, based on the analysis of the INI Editor and FNIS tool plugins.

## Table of Contents

- [Mod Organizer 2 Tool Plugins Documentation](#mod-organizer-2-tool-plugins-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Tool Plugin Interface](#tool-plugin-interface)
    - [IPluginTool Interface](#iplugintool-interface)
    - [Required Methods](#required-methods)
    - [Tool Registration](#tool-registration)
  - [INI Editor Plugin](#ini-editor-plugin)
    - [Overview](#overview)
    - [Implementation Details](#implementation-details)
    - [UI Components](#ui-components)
    - [Settings](#settings)
  - [FNIS Tool Plugin](#fnis-tool-plugin)
    - [Overview](#overview-1)
    - [Implementation Details](#implementation-details-1)
    - [Multiple Tool Entries](#multiple-tool-entries)
    - [Settings](#settings-1)
    - [Python vs C++](#python-vs-c)
  - [Common Patterns](#common-patterns)
    - [Tool Organization](#tool-organization)
    - [Settings Management](#settings-management)
    - [UI Integration](#ui-integration)
    - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [User Experience](#user-experience)
    - [Performance](#performance)
    - [Compatibility](#compatibility)
  - [Conclusion](#conclusion)

## Introduction

Tool plugins in Mod Organizer 2 provide additional functionality through the tools menu. They can range from simple utilities like the INI Editor to more complex tools like the FNIS integration. Tool plugins can be implemented in either C++ or Python, and they can use both the Mod Organizer 2 API and Qt directly for their UI components.

## Tool Plugin Interface

### IPluginTool Interface

All tool plugins must implement the `IPluginTool` interface, which is defined in `iplugintool.h`. This interface extends the base `IPlugin` interface and adds methods specific to tools.

```cpp
class IPluginTool : public QObject, public virtual IPlugin
{
  Q_INTERFACES(IPlugin)
public:
  IPluginTool() : m_ParentWidget(nullptr) {}

  virtual QString displayName() const = 0;
  virtual QString localizedName() const { return displayName(); }
  virtual QString tooltip() const = 0;
  virtual QIcon icon() const = 0;
  virtual void setParentWidget(QWidget* widget) { m_ParentWidget = widget; }

public Q_SLOTS:
  virtual void display() const = 0;

protected:
  QWidget* parentWidget() const { return m_ParentWidget; }

private:
  QWidget* m_ParentWidget;
};
```

### Required Methods

Tool plugins must implement the following methods:

1. **From IPlugin:**
   - `init(IOrganizer* moInfo)`: Initializes the plugin with the Mod Organizer instance
   - `name()`: Returns the name of the plugin
   - `author()`: Returns the author of the plugin
   - `description()`: Returns a description of the plugin
   - `version()`: Returns the version of the plugin
   - `settings()`: Returns a list of settings for the plugin

2. **From IPluginTool:**
   - `displayName()`: Returns the name of the tool as displayed in the UI
   - `tooltip()`: Returns the tooltip for the tool
   - `icon()`: Returns the icon for the tool
   - `display()`: Called when the user clicks on the tool in the menu

### Tool Registration

Tool plugins are registered with Mod Organizer 2 using the Qt plugin system. In C++, this is done using the `Q_PLUGIN_METADATA` macro:

```cpp
Q_PLUGIN_METADATA(IID "org.tannin.IniEditor" FILE "inieditor.json")
```

In Python, this is done by implementing a `createPlugin()` function that returns an instance of the plugin class:

```python
def createPlugin():
    return FNISTool()
```

## INI Editor Plugin

### Overview

The INI Editor plugin provides a simple editor for INI files in the current profile. It allows users to edit the INI files directly within Mod Organizer 2 or using an external editor.

### Implementation Details

The INI Editor plugin is implemented in C++ and consists of two main files:

1. `inieditor.h`: Defines the `IniEditor` class that implements the `IPluginTool` interface
2. `inieditor.cpp`: Implements the methods of the `IniEditor` class

The plugin uses the `TextViewer` class from the Mod Organizer 2 UI Base library to display and edit the INI files. The `TextViewer` class provides a tabbed text editor with basic editing functionality.

### UI Components

The INI Editor plugin uses the following UI components:

1. **TextViewer**: A tabbed text editor from the Mod Organizer 2 UI Base library
2. **QMessageBox**: Used for displaying error messages
3. **QIcon**: Used for the tool icon

### Settings

The INI Editor plugin has the following settings:

1. `external`: Whether to use an external editor to open the files (default: false)
2. `associated`: When using an external editor, whether to use the application associated with INI files or the default editor (default: true)

## FNIS Tool Plugin

### Overview

The FNIS tool plugin provides integration with Fore's New Idles in Skyrim (FNIS), a tool used to generate animation data for Skyrim mods. The plugin allows users to run FNIS directly from Mod Organizer 2 and configure its settings.

### Implementation Details

The FNIS tool plugin is implemented in Python and consists of three main files:

1. `FNISTool.py`: Implements the main FNIS tool functionality
2. `FNISToolReset.py`: Implements a tool to reset the FNIS tool settings
3. `FNISPatches.py`: Implements a tool to configure FNIS patches

The plugin uses the Mod Organizer 2 API to interact with the virtual file system (VFS) and run FNIS within it. It also uses Qt for its UI components.

### Multiple Tool Entries

The FNIS tool plugin demonstrates how to create multiple tool entries in the tools menu. It does this by implementing three separate classes that each implement the `IPluginTool` interface:

1. `FNISTool`: The main FNIS tool
2. `FNISToolReset`: A tool to reset the FNIS tool settings
3. `FNISPatches`: A tool to configure FNIS patches

The `FNISToolReset` and `FNISPatches` classes specify `FNISTool` as their master plugin using the `master()` method, which causes them to appear as sub-items under the main FNIS tool in the menu.

```python
def master(self):
    return "FNIS Integration Tool"
```

### Settings

The FNIS tool plugin has several settings:

1. `fnis-path`: Path to the FNIS executable
2. `output-to-mod`: Whether to output FNIS files to a separate mod
3. `output-path`: Path to the mod to output FNIS files to
4. `output-logs-to-mod`: Whether to output FNIS logs to a separate mod
5. `output-logs-path`: Path to the mod to output FNIS logs to
6. `initialised`: Whether the plugin has been initialized

### Python vs C++

The FNIS tool plugin demonstrates how to implement a tool plugin in Python, which offers several advantages:

1. **Ease of Development**: Python is generally easier to develop with than C++
2. **Rapid Iteration**: Python plugins can be modified without recompiling
3. **Access to Python Libraries**: Python plugins can use the extensive Python ecosystem

However, Python plugins also have some disadvantages:

1. **Performance**: Python is generally slower than C++
2. **Dependency Management**: Python plugins may require additional dependencies
3. **Version Compatibility**: Python plugins may be sensitive to Python version changes

## Common Patterns

### Tool Organization

Both the INI Editor and FNIS tool plugins follow a similar organization:

1. **Plugin Class**: A class that implements the `IPluginTool` interface
2. **Initialization**: The `init()` method stores the Mod Organizer instance for later use
3. **Display Method**: The `display()` method implements the main functionality of the tool
4. **Settings**: The `settings()` method defines the settings for the tool

### Settings Management

Both plugins use the Mod Organizer settings system to store and retrieve settings:

```cpp
// C++ (INI Editor)
QList<PluginSetting> IniEditor::settings() const
{
  QList<PluginSetting> result;
  result.push_back(PluginSetting("external", "Use an external editor to open the files", QVariant(false)));
  result.push_back(PluginSetting("associated", "When using an external editor, use the application associated with \"INI\" files. "
                                 "If false, uses the \"edit\" command which usually invokes regular notepad.", QVariant(true)));
  return result;
}
```

```python
# Python (FNIS Tool)
def settings(self):
    return [
        mobase.PluginSetting("fnis-path", self.tr("Path to GenerateFNISforUsers.exe"), ""),
        mobase.PluginSetting("output-to-mod", self.tr("Whether or not to direct the FNIS output to a mod folder."), True),
        mobase.PluginSetting("output-path", self.tr("When output-to-mod is enabled, the path to the mod to use."), ""),
        mobase.PluginSetting("initialised", self.tr("Settings have been initialised.  Set to False to reinitialise them."), False),
        mobase.PluginSetting("output-logs-to-mod", self.tr("Whether or not to direct any new FNIS logs to a mod folder."), True),
        mobase.PluginSetting("output-logs-path", self.tr("When output-logs-to-mod is enabled, the path to the mod to use."), ""),
    ]
```

### UI Integration

Both plugins integrate with the Mod Organizer UI in different ways:

1. **INI Editor**: Uses the `TextViewer` class from the Mod Organizer 2 UI Base library
2. **FNIS Tool**: Uses Qt directly to create dialogs and other UI components

### Error Handling

Both plugins handle errors in a user-friendly way:

1. **INI Editor**: Uses `QMessageBox` to display error messages
2. **FNIS Tool**: Uses custom exceptions and `QMessageBox` to display error messages

## Best Practices

### User Experience

1. **Clear Feedback**: Provide clear feedback to the user about what the tool is doing
2. **Error Handling**: Handle errors gracefully and provide helpful error messages
3. **Settings**: Use the Mod Organizer settings system to store and retrieve settings
4. **Localization**: Use the Qt translation system to support multiple languages

### Performance

1. **Asynchronous Operations**: Use asynchronous operations for long-running tasks
2. **Resource Management**: Properly manage resources like file handles and memory
3. **UI Responsiveness**: Keep the UI responsive during long-running operations

### Compatibility

1. **Version Checking**: Check for compatibility with the current version of Mod Organizer
2. **Game Support**: Specify which games the tool supports
3. **Dependency Management**: Properly manage dependencies on other plugins or libraries

## Conclusion

Tool plugins are a powerful way to extend the functionality of Mod Organizer 2. They can be implemented in either C++ or Python, and they can use both the Mod Organizer 2 API and Qt directly for their UI components. By following the patterns and best practices outlined in this document, you can create effective and user-friendly tool plugins for Mod Organizer 2.
