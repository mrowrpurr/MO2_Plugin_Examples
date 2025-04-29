# MO2 Events Available to Python Plugins

This document lists all the events that Python plugins can register to listen to in Mod Organizer 2. These events allow plugins to respond to various actions and changes within MO2.

## Table of Contents

- [IPluginList Events](#ipluginlist-events)
- [IModList Events](#imodlist-events)
- [IOrganizer Events](#iorganizer-events)
- [IDownloadManager Events](#idownloadmanager-events)

## IPluginList Events

These events are related to game plugins (ESPs, ESMs, ESLs) and can be accessed through `organizer.pluginList()`.

### onRefreshed

Triggered when the plugin list is refreshed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.pluginList().onRefreshed(self.onPluginListRefreshed)
    return True

def onPluginListRefreshed(self):
    # Handle plugin list refresh
    print("Plugin list was refreshed")
```

### onPluginMoved

Triggered when a plugin is moved in the load order.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.pluginList().onPluginMoved(self.onPluginMoved)
    return True

def onPluginMoved(self, name, oldPriority, newPriority):
    # Handle plugin move
    print(f"Plugin {name} moved from priority {oldPriority} to {newPriority}")
```

### onPluginStateChanged

Triggered when a plugin's state changes (enabled/disabled).

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.pluginList().onPluginStateChanged(self.onPluginStateChanged)
    return True

def onPluginStateChanged(self, pluginStates):
    # Handle plugin state changes
    for plugin, state in pluginStates.items():
        print(f"Plugin {plugin} state changed to {state}")
```

## IModList Events

These events are related to mods and can be accessed through `organizer.modList()`.

### onModInstalled

Triggered when a mod is installed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.modList().onModInstalled(self.onModInstalled)
    return True

def onModInstalled(self, mod):
    # Handle mod installation
    print(f"Mod installed: {mod.name()}")
```

### onModRemoved

Triggered when a mod is removed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.modList().onModRemoved(self.onModRemoved)
    return True

def onModRemoved(self, modName):
    # Handle mod removal
    print(f"Mod removed: {modName}")
```

### onModStateChanged

Triggered when a mod's state changes (enabled/disabled).

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.modList().onModStateChanged(self.onModStateChanged)
    return True

def onModStateChanged(self, modStates):
    # Handle mod state changes
    for mod, state in modStates.items():
        print(f"Mod {mod} state changed to {state}")
```

### onModMoved

Triggered when a mod is moved in the priority list.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.modList().onModMoved(self.onModMoved)
    return True

def onModMoved(self, modName, oldPriority, newPriority):
    # Handle mod move
    print(f"Mod {modName} moved from priority {oldPriority} to {newPriority}")
```

## IOrganizer Events

These events are related to the main MO2 organizer and can be accessed directly through the `organizer` object.

### onAboutToRun

Triggered just before an application is run through MO2. There are two overloads:

1. Simple version (returns application path only):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onAboutToRun(self.onAboutToRunSimple)
    return True

def onAboutToRunSimple(self, executable):
    # Handle application about to run
    print(f"About to run: {executable}")
    return True  # Return True to allow the application to run, False to prevent it
```

2. Detailed version (returns application path, working directory, and arguments):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onAboutToRun(self.onAboutToRunDetailed)
    return True

def onAboutToRunDetailed(self, executable, cwd, args):
    # Handle application about to run with more details
    print(f"About to run: {executable}")
    print(f"Working directory: {cwd}")
    print(f"Arguments: {args}")
    return True  # Return True to allow the application to run, False to prevent it
```

### onFinishedRun

Triggered when an application that was run through MO2 has finished.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onFinishedRun(self.onFinishedRun)
    return True

def onFinishedRun(self, executable, exitCode):
    # Handle application finished running
    print(f"Finished running: {executable} with exit code {exitCode}")
```

### onUserInterfaceInitialized

Triggered when the MO2 user interface has been initialized.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onUserInterfaceInitialized(self.onUserInterfaceInitialized)
    return True

def onUserInterfaceInitialized(self, mainWindow):
    # Handle UI initialization
    print("UI initialized")
    # mainWindow is the main QMainWindow of MO2
```

### onNextRefresh

Triggered after the next refresh of MO2's virtual file system.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onNextRefresh(self.onNextRefresh)
    return True

def onNextRefresh(self):
    # Handle refresh
    print("MO2 refreshed")
```

### onProfileCreated

Triggered when a new profile is created.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onProfileCreated(self.onProfileCreated)
    return True

def onProfileCreated(self, profile):
    # Handle profile creation
    print(f"Profile created: {profile.name()}")
```

### onProfileRenamed

Triggered when a profile is renamed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onProfileRenamed(self.onProfileRenamed)
    return True

def onProfileRenamed(self, profile, oldName, newName):
    # Handle profile rename
    print(f"Profile renamed from {oldName} to {newName}")
```

### onProfileRemoved

Triggered when a profile is removed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onProfileRemoved(self.onProfileRemoved)
    return True

def onProfileRemoved(self, profileName):
    # Handle profile removal
    print(f"Profile removed: {profileName}")
```

### onProfileChanged

Triggered when the current profile is changed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onProfileChanged(self.onProfileChanged)
    return True

def onProfileChanged(self, oldProfile, newProfile):
    # Handle profile change
    oldName = oldProfile.name() if oldProfile else "None"
    print(f"Profile changed from {oldName} to {newProfile.name()}")
```

### onPluginSettingChanged

Triggered when a plugin setting is changed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onPluginSettingChanged(self.onPluginSettingChanged)
    return True

def onPluginSettingChanged(self, pluginName, key, oldValue, newValue):
    # Handle plugin setting change
    print(f"Plugin {pluginName} setting {key} changed from {oldValue} to {newValue}")
```

### onPluginEnabled

Triggered when a plugin is enabled. There are two overloads:

1. General version (provides the plugin object):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onPluginEnabled(self.onPluginEnabled)
    return True

def onPluginEnabled(self, plugin):
    # Handle plugin being enabled
    print(f"Plugin enabled: {plugin.name()}")
```

2. Specific version (for a named plugin):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onPluginEnabled("SomePluginName", self.onSpecificPluginEnabled)
    return True

def onSpecificPluginEnabled(self):
    # Handle specific plugin being enabled
    print("SomePluginName was enabled")
```

### onPluginDisabled

Triggered when a plugin is disabled. There are two overloads:

1. General version (provides the plugin object):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onPluginDisabled(self.onPluginDisabled)
    return True

def onPluginDisabled(self, plugin):
    # Handle plugin being disabled
    print(f"Plugin disabled: {plugin.name()}")
```

2. Specific version (for a named plugin):

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.onPluginDisabled("SomePluginName", self.onSpecificPluginDisabled)
    return True

def onSpecificPluginDisabled(self):
    # Handle specific plugin being disabled
    print("SomePluginName was disabled")
```

## IDownloadManager Events

These events are related to downloads and can be accessed through `organizer.downloadManager()`.

### onDownloadComplete

Triggered when a download completes.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.downloadManager().onDownloadComplete(self.onDownloadComplete)
    return True

def onDownloadComplete(self, downloadId):
    # Handle download completion
    path = self._organizer.downloadManager().downloadPath(downloadId)
    print(f"Download completed: {path}")
```

### onDownloadPaused

Triggered when a download is paused.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.downloadManager().onDownloadPaused(self.onDownloadPaused)
    return True

def onDownloadPaused(self, downloadId):
    # Handle download pause
    path = self._organizer.downloadManager().downloadPath(downloadId)
    print(f"Download paused: {path}")
```

### onDownloadFailed

Triggered when a download fails.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.downloadManager().onDownloadFailed(self.onDownloadFailed)
    return True

def onDownloadFailed(self, downloadId):
    # Handle download failure
    path = self._organizer.downloadManager().downloadPath(downloadId)
    print(f"Download failed: {path}")
```

### onDownloadRemoved

Triggered when a download is removed.

```python
def init(self, organizer):
    self._organizer = organizer
    self._organizer.downloadManager().onDownloadRemoved(self.onDownloadRemoved)
    return True

def onDownloadRemoved(self, downloadId):
    # Handle download removal
    print(f"Download removed: {downloadId}")
```

## Conclusion

These are all the events that Python plugins can register to listen to in Mod Organizer 2. By using these events, plugins can respond to various actions and changes within MO2, allowing for powerful integrations and automations.

Note that while C++ plugins may have access to additional events, the events listed in this document are the ones that have explicit Python bindings and are therefore available to Python plugins.
