# Mod Organizer 2 UI Base Documentation

This document provides an overview of the interfaces and classes available in the Mod Organizer 2 UI Base library that are relevant for plugin development.

See also:
- [Diagrams](DIAGRAMS.md)
- [Plugin Development Guide](GUIDE.md)

## Table of Contents

- [Mod Organizer 2 UI Base Documentation](#mod-organizer-2-ui-base-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Core Plugin Interfaces](#core-plugin-interfaces)
    - [IPlugin](#iplugin)
    - [Plugin Settings](#plugin-settings)
  - [Plugin Types](#plugin-types)
    - [IPluginTool](#iplugintool)
    - [IPluginGame](#iplugingame)
    - [IPluginInstaller](#iplugininstaller)
      - [IPluginInstallerSimple](#iplugininstallersimple)
      - [IPluginInstallerCustom](#iplugininstallercustom)
    - [IPluginDiagnose](#iplugindiagnose)
    - [IPluginModPage](#ipluginmodpage)
    - [IPluginPreview](#ipluginpreview)
    - [IPluginFileMapper](#ipluginfilemapper)
  - [Organizer Interface](#organizer-interface)
    - [IOrganizer](#iorganizer)
  - [Mod Management](#mod-management)
    - [IModInterface](#imodinterface)
    - [IModList](#imodlist)
  - [Plugin Management](#plugin-management)
    - [IPluginList](#ipluginlist)
  - [Profile Management](#profile-management)
    - [IProfile](#iprofile)
  - [Installation Management](#installation-management)
    - [IInstallationManager](#iinstallationmanager)
    - [IFileTree](#ifiletree)
  - [Download Management](#download-management)
    - [IDownloadManager](#idownloadmanager)
  - [Repository Integration](#repository-integration)
    - [IModRepositoryBridge](#imodrepositorybridge)
  - [Game Features](#game-features)
    - [IGameFeatures](#igamefeatures)
    - [Game Feature Types](#game-feature-types)

## Introduction

Mod Organizer 2 (MO2) provides a plugin system that allows developers to extend its functionality. The UI Base library contains the interfaces that plugins can implement to integrate with MO2. This document provides an overview of these interfaces and how they can be used to develop plugins for MO2.

## Core Plugin Interfaces

### IPlugin

`IPlugin` is the base interface for all plugins in Mod Organizer 2. All plugin types inherit from this interface.

Key methods:
- `bool init(IOrganizer* organizer)`: Initialize the plugin with the organizer interface
- `QString name() const`: Get the internal name of the plugin
- `QString localizedName() const`: Get the localized name of the plugin
- `QString master() const`: Get the name of the master plugin (if any)
- `std::vector<std::shared_ptr<const IPluginRequirement>> requirements() const`: Get the requirements for the plugin
- `QString author() const`: Get the author of the plugin
- `QString description() const`: Get the description of the plugin
- `VersionInfo version() const`: Get the version of the plugin
- `QList<PluginSetting> settings() const`: Get the list of configurable settings for the plugin
- `bool enabledByDefault() const`: Check if the plugin should be enabled by default

### Plugin Settings

The `PluginSetting` struct is used to define user-configurable settings for plugins:

```cpp
struct PluginSetting {
  QString key;
  QString description;
  QVariant defaultValue;
};
```

## Plugin Types

### IPluginTool

`IPluginTool` is the interface for plugins that provide tools accessible from the UI.

Key methods:
- `QString displayName() const`: Get the name of the tool as displayed in the UI
- `QString tooltip() const`: Get the tooltip for the tool
- `QIcon icon() const`: Get the icon for the tool
- `void display() const`: Called when the user clicks to start the tool

### IPluginGame

`IPluginGame` is the interface for plugins that add support for specific games to Mod Organizer 2.

Key methods:
- `QString gameName() const`: Get the name of the game
- `QString displayGameName() const`: Get the display name of the game
- `void detectGame()`: Detect the game
- `void initializeProfile(const QDir& directory, ProfileSettings settings) const`: Initialize a profile for this game
- `bool isInstalled() const`: Check if the game is installed
- `QIcon gameIcon() const`: Get the icon for the game
- `QDir gameDirectory() const`: Get the directory to the game installation
- `QDir dataDirectory() const`: Get the directory where the game expects to find its data files
- `void setGamePath(const QString& path)`: Set the path to the managed game
- `QDir documentsDirectory() const`: Get the directory of the documents folder for this game
- `QDir savesDirectory() const`: Get the path to where save games are stored
- `QList<ExecutableInfo> executables() const`: Get the list of automatically discovered executables
- `QString steamAPPId() const`: Get the Steam app ID for this game
- `QStringList primaryPlugins() const`: Get the list of plugins that are part of the game
- `QStringList enabledPlugins() const`: Get the list of plugins enabled by the game
- `QStringList gameVariants() const`: Get the list of game variants
- `void setGameVariant(const QString& variant)`: Set the game variant
- `QString binaryName() const`: Get the name of the executable that gets run
- `QString gameShortName() const`: Get the 'short' name of the game
- `QString lootGameName() const`: Get the game name that's passed to the LOOT CLI
- `QStringList primarySources() const`: Get any primary alternative 'short' name for the game
- `QStringList validShortNames() const`: Get any valid 'short' name for the game
- `QString gameNexusName() const`: Get the 'short' name of the game for Nexus
- `QStringList iniFiles() const`: Get the list of .ini files this game uses
- `QStringList DLCPlugins() const`: Get a list of esp/esm files that are part of known DLCs
- `QStringList CCPlugins() const`: Get the current list of active Creation Club plugins
- `LoadOrderMechanism loadOrderMechanism() const`: Determine the load order mechanism used by this game
- `SortMechanism sortMechanism() const`: Determine the sorting mechanism
- `int nexusModOrganizerID() const`: Get the Nexus ID of Mod Organizer
- `int nexusGameID() const`: Get the Nexus Game ID
- `bool looksValid(QDir const&) const`: Check if the supplied directory looks like a valid game
- `QString gameVersion() const`: Get the version of the game
- `QString getLauncherName() const`: Get the name of the game launcher
- `QString getSupportURL() const`: Get a URL for the support page for the game

### IPluginInstaller

`IPluginInstaller` is the base interface for plugins that can install mods from archives.

Key methods:
- `unsigned int priority() const`: Get the priority of this installer
- `bool isManualInstaller() const`: Check if this plugin should be treated as a manual installer
- `void onInstallationStart(QString const& archive, bool reinstallation, IModInterface* currentMod)`: Called at the start of the installation process
- `void onInstallationEnd(EInstallResult result, IModInterface* newMod)`: Called at the end of the installation process
- `bool isArchiveSupported(std::shared_ptr<const IFileTree> tree) const`: Test if the archive can be installed through this installer

#### IPluginInstallerSimple

`IPluginInstallerSimple` is the interface for simple installer plugins that only need to restructure the file tree.

Key methods:
- `EInstallResult install(GuessedValue<QString>& modName, std::shared_ptr<IFileTree>& tree, QString& version, int& nexusID)`: Install the mod by restructuring the tree

#### IPluginInstallerCustom

`IPluginInstallerCustom` is the interface for custom installer plugins that need to handle the archive extraction themselves.

Key methods:
- `bool isArchiveSupported(const QString& archiveName) const`: Test if the archive can be installed through this installer
- `std::set<QString> supportedExtensions() const`: Get the list of file extensions that may be supported
- `EInstallResult install(GuessedValue<QString>& modName, QString gameName, const QString& archiveName, const QString& version, int nexusID)`: Install the mod

### IPluginDiagnose

`IPluginDiagnose` is the interface for plugins that can diagnose problems and provide solutions.

Key methods:
- `std::vector<unsigned int> activeProblems() const`: Get a list of keys of active problems
- `QString shortDescription(unsigned int key) const`: Get a short description for the specified problem
- `QString fullDescription(unsigned int key) const`: Get the full description for the specified problem
- `bool hasGuidedFix(unsigned int key) const`: Check if this plugin provides a guide to fix the issue
- `void startGuidedFix(unsigned int key) const`: Start the guided fix for the specified problem

### IPluginModPage

`IPluginModPage` is the interface for plugins that add support for mod hosting websites.

Key methods:
- `QString displayName() const`: Get the name of the page as displayed in the UI
- `QIcon icon() const`: Get the icon to be displayed with the page
- `QUrl pageURL() const`: Get the URL to open when the user wants to visit this mod page
- `bool useIntegratedBrowser() const`: Check if the page should be opened in the integrated browser
- `bool handlesDownload(const QUrl& pageURL, const QUrl& downloadURL, ModRepositoryFileInfo& fileInfo) const`: Test if the plugin handles a download

### IPluginPreview

`IPluginPreview` is the interface for plugins that can generate previews for files.

Key methods:
- `std::set<QString> supportedExtensions() const`: Get the set of file extensions that may be supported
- `bool supportsArchives() const`: Check if the preview supports raw data previews
- `QWidget* genFilePreview(const QString& fileName, const QSize& maxSize) const`: Generate a preview widget for the specified file
- `QWidget* genDataPreview(const QByteArray& fileData, const QString& fileName, const QSize& maxSize) const`: Generate a preview widget from an archive file loaded into memory

### IPluginFileMapper

`IPluginFileMapper` is the interface for plugins that add virtual file links.

Key methods:
- `MappingType mappings() const`: Get a list of file maps

## Organizer Interface

### IOrganizer

`IOrganizer` is the interface to the running session of Mod Organizer, providing access to various functionality.

Key methods:
- `IModRepositoryBridge* createNexusBridge() const`: Create a new Nexus interface class
- `QString profileName() const`: Get the name of the active profile
- `QString profilePath() const`: Get the path to the active profile
- `QString downloadsPath() const`: Get the path to the download directory
- `QString overwritePath() const`: Get the path to the overwrite directory
- `QString basePath() const`: Get the path to the base directory
- `QString modsPath() const`: Get the path to the mods directory
- `VersionInfo appVersion() const`: Get the running version of Mod Organizer
- `IModInterface* createMod(GuessedValue<QString>& name)`: Create a new mod with the specified name
- `IPluginGame* getGame(const QString& gameName) const`: Get the game plugin matching the specified game
- `void modDataChanged(IModInterface* mod)`: Let the organizer know that a mod has changed
- `bool isPluginEnabled(IPlugin* plugin) const`: Check if a plugin is enabled
- `bool isPluginEnabled(QString const& pluginName) const`: Check if a plugin is enabled by name
- `QVariant pluginSetting(const QString& pluginName, const QString& key) const`: Retrieve a plugin setting
- `void setPluginSetting(const QString& pluginName, const QString& key, const QVariant& value)`: Set a plugin setting
- `QVariant persistent(const QString& pluginName, const QString& key, const QVariant& def = QVariant()) const`: Retrieve a persistent value for a plugin
- `void setPersistent(const QString& pluginName, const QString& key, const QVariant& value, bool sync = true)`: Set a persistent value for a plugin
- `QString pluginDataPath() const`: Get the path to the plugin data directory
- `IModInterface* installMod(const QString& fileName, const QString& nameSuggestion = QString())`: Install a mod archive
- `QString resolvePath(const QString& fileName) const`: Resolve a path relative to the virtual data directory
- `QStringList listDirectories(const QString& directoryName) const`: Get a list of virtual subdirectories
- `QStringList findFiles(const QString& path, const std::function<bool(const QString&)>& filter) const`: Find files in the virtual directory matching a filter
- `QStringList findFiles(const QString& path, const QStringList& filters) const`: Find files in the virtual directory matching filters
- `QStringList getFileOrigins(const QString& fileName) const`: Get the file origins for the specified file
- `QList<FileInfo> findFileInfos(const QString& path, const std::function<bool(const FileInfo&)>& filter) const`: Find files in the virtual directory matching a complex filter
- `std::shared_ptr<const MOBase::IFileTree> virtualFileTree() const`: Get the virtual file tree
- `IDownloadManager* downloadManager() const`: Get the download manager interface
- `IPluginList* pluginList() const`: Get the plugin list interface
- `IModList* modList() const`: Get the mod list interface
- `IProfile* profile() const`: Get the active profile interface
- `IGameFeatures* gameFeatures() const`: Get the game features interface
- `HANDLE startApplication(const QString& executable, const QStringList& args = QStringList(), const QString& cwd = "", const QString& profile = "", const QString& forcedCustomOverwrite = "", bool ignoreCustomOverwrite = false)`: Run a program using the virtual filesystem
- `bool waitForApplication(HANDLE handle, bool refresh = true, LPDWORD exitCode = nullptr) const`: Block until the given process has completed
- `void refresh(bool saveChanges = true)`: Refresh the internal mods file structure from disk
- `MOBase::IPluginGame const* managedGame() const`: Get the currently managed game info
- Various callback registration methods for events like application run, UI initialization, profile changes, etc.

## Mod Management

### IModInterface

`IModInterface` is the interface for interacting with mods.

Key methods:
- `QString name() const`: Get the name of the mod
- `QString absolutePath() const`: Get the absolute path to the mod
- `QString comments() const`: Get the comments for this mod
- `QString notes() const`: Get the notes for this mod
- `QString gameName() const`: Get the name of the game associated with this mod
- `QString repository() const`: Get the name of the repository from which this mod was installed
- `int nexusId() const`: Get the Nexus ID of this mod
- `VersionInfo version() const`: Get the current version of this mod
- `VersionInfo newestVersion() const`: Get the newest version of this mod
- `VersionInfo ignoredVersion() const`: Get the ignored version of this mod
- `QString installationFile() const`: Get the absolute path to the file that was used to install this mod
- `std::set<std::pair<int, int>> installedFiles() const`: Get the installed files
- `bool converted() const`: Check if this mod was marked as converted
- `bool validated() const`: Check if this mod was marked as containing valid game data
- `QColor color() const`: Get the color of the 'Notes' column
- `QString url() const`: Get the URL of this mod
- `int primaryCategory() const`: Get the ID of the primary category of this mod
- `QStringList categories() const`: Get the list of categories this mod belongs to
- `TrackedState trackedState() const`: Get the tracked state of this mod
- `EndorsedState endorsedState() const`: Get the endorsement state of this mod
- `std::shared_ptr<const MOBase::IFileTree> fileTree() const`: Get a file tree for this mod
- `bool isOverwrite() const`: Check if this object represents the overwrite mod
- `bool isBackup() const`: Check if this object represents a backup
- `bool isSeparator() const`: Check if this object represents a separator
- `bool isForeign() const`: Check if this object represents a foreign mod
- Various setter methods for mod properties
- Plugin setting methods for storing and retrieving plugin-specific settings for the mod

### IModList

`IModList` is the interface for interacting with the list of mods.

Key methods:
- `QString displayName(const QString& internalName) const`: Get the display name of a mod from its internal name
- `QStringList allMods() const`: Get a list of all installed mod names
- `QStringList allModsByProfilePriority(MOBase::IProfile* profile = nullptr) const`: Get the list of installed mod names, sorted by priority
- `IModInterface* getMod(const QString& name) const`: Get the mod with the given name
- `bool removeMod(MOBase::IModInterface* mod)`: Remove a mod
- `MOBase::IModInterface* renameMod(MOBase::IModInterface* mod, const QString& name)`: Rename a mod
- `ModStates state(const QString& name) const`: Get the state of a mod
- `bool setActive(const QString& name, bool active)`: Enable or disable a mod
- `int setActive(const QStringList& names, bool active)`: Enable or disable a list of mods
- `int priority(const QString& name) const`: Get the priority of a mod
- `bool setPriority(const QString& name, int newPriority)`: Change the priority of a mod
- Various callback registration methods for mod-related events

## Plugin Management

### IPluginList

`IPluginList` is the interface for interacting with the list of game plugins (ESPs, ESMs, etc.).

Key methods:
- `QStringList pluginNames() const`: Get the list of plugin names
- `PluginStates state(const QString& name) const`: Get the state of a plugin
- `void setState(const QString& name, PluginStates state)`: Set the state of a plugin
- `int priority(const QString& name) const`: Get the priority of a plugin
- `bool setPriority(const QString& name, int newPriority)`: Change the priority of a plugin
- `int loadOrder(const QString& name) const`: Get the load order of a plugin
- `void setLoadOrder(const QStringList& pluginList)`: Set the load order of the plugin list
- `bool isMaster(const QString& name) const`: Check if a plugin is a master file (deprecated)
- `QStringList masters(const QString& name) const`: Get the list of masters required for this plugin
- `QString origin(const QString& name) const`: Get the name of the origin of a plugin
- `bool hasMasterExtension(const QString& name) const`: Check if a plugin has the .esm extension
- `bool hasLightExtension(const QString& name) const`: Check if a plugin has the .esl extension
- `bool isMasterFlagged(const QString& name) const`: Check if a plugin is flagged as master
- `bool isMediumFlagged(const QString& name) const`: Check if a plugin is flagged as medium
- `bool isLightFlagged(const QString& name) const`: Check if a plugin is flagged as light
- `bool isBlueprintFlagged(const QString& name) const`: Check if a plugin is flagged as blueprint
- `bool hasNoRecords(const QString& name) const`: Check if a plugin has no records
- `int formVersion(const QString& name) const`: Get the form version of a plugin
- `float headerVersion(const QString& name) const`: Get the header version of a plugin
- `QString author(const QString& name) const`: Get the author of a plugin
- `QString description(const QString& name) const`: Get the description of a plugin
- Various callback registration methods for plugin-related events

## Profile Management

### IProfile

`IProfile` is the interface for interacting with profiles.

Key methods:
- `QString name() const`: Get the name of the profile
- `QString absolutePath() const`: Get the absolute path to the profile
- `bool localSavesEnabled() const`: Check if local saves are enabled for this profile
- `bool localSettingsEnabled() const`: Check if local settings are enabled for this profile
- `bool invalidationActive(bool* supported) const`: Check if invalidation is active for this profile
- `QString absoluteIniFilePath(QString iniFile) const`: Get the absolute file path to the corresponding INI file for this profile

## Installation Management

### IInstallationManager

`IInstallationManager` is the interface for interacting with the installation manager.

Key methods:
- `QStringList getSupportedExtensions() const`: Get the extensions of archives supported by this installation manager
- `QString extractFile(std::shared_ptr<const FileTreeEntry> entry, bool silent = false)`: Extract a file from the currently opened archive to a temporary location
- `QStringList extractFiles(std::vector<std::shared_ptr<const FileTreeEntry>> const& entries, bool silent = false)`: Extract multiple files from the currently opened archive
- `QString createFile(std::shared_ptr<const MOBase::FileTreeEntry> entry)`: Create a new file on the disk corresponding to the given entry
- `IPluginInstaller::EInstallResult installArchive(MOBase::GuessedValue<QString>& modName, const QString& archiveFile, int modID = 0)`: Install an archive

### IFileTree

`IFileTree` is the interface for interacting with file trees, which represent virtual file systems.

Key methods:
- `bool exists(QString path, FileTreeEntry::FileTypes type = FileTreeEntry::FILE_OR_DIRECTORY) const`: Check if an entry exists
- `std::shared_ptr<FileTreeEntry> find(QString path, FileTypes type = FILE_OR_DIRECTORY)`: Find an entry
- `std::shared_ptr<IFileTree> findDirectory(QString path)`: Find a directory
- `QString pathTo(std::shared_ptr<const FileTreeEntry> entry, QString sep = "\\") const`: Get the path from this tree to an entry
- `void walk(std::function<WalkReturn(QString const&, std::shared_ptr<const FileTreeEntry>)> callback, QString sep = "\\") const`: Walk the tree, calling a function for each entry
- `std::shared_ptr<IFileTree> createOrphanTree(QString name = "") const`: Create a new orphan empty tree
- `std::shared_ptr<FileTreeEntry> addFile(QString path, bool replaceIfExists = false)`: Create a new file
- `std::shared_ptr<IFileTree> addDirectory(QString path)`: Create a new directory tree
- `iterator insert(std::shared_ptr<FileTreeEntry> entry, InsertPolicy insertPolicy = InsertPolicy::FAIL_IF_EXISTS)`: Insert an entry
- `std::size_t merge(std::shared_ptr<IFileTree> source, OverwritesType* overwrites = nullptr)`: Merge a tree with this tree
- `bool move(std::shared_ptr<FileTreeEntry> entry, QString path = "", InsertPolicy insertPolicy = InsertPolicy::FAIL_IF_EXISTS)`: Move an entry
- `std::shared_ptr<FileTreeEntry> copy(std::shared_ptr<const FileTreeEntry> entry, QString path = "", InsertPolicy insertPolicy = InsertPolicy::FAIL_IF_EXISTS)`: Copy an entry
- `iterator erase(std::shared_ptr<FileTreeEntry> entry)`: Delete an entry
- `std::pair<iterator, std::shared_ptr<FileTreeEntry>> erase(QString name)`: Delete an entry by name
- `bool clear()`: Delete all entries
- `std::size_t removeAll(QStringList names)`: Delete entries by name
- `std::size_t removeIf(std::function<bool(std::shared_ptr<FileTreeEntry> const& entry)> predicate)`: Delete entries that match a predicate

## Download Management

### IDownloadManager

`IDownloadManager` is the interface for interacting with the download manager.

Key methods:
- `int startDownloadURLs(const QStringList& urls)`: Download a file by URL
- `int startDownloadNexusFile(int modID, int fileID)`: Download a file from Nexus Mods
- `int startDownloadNexusFileForGame(const QString& gameName, int modID, int fileID)`: Download a file from Nexus Mods for a specific game
- `QString downloadPath(int id)`: Get the file path of a download
- Various callback registration methods for download-related events

## Repository Integration

### IModRepositoryBridge

`IModRepositoryBridge` is the interface for interacting with mod repositories like Nexus Mods.

Key methods:
- `void requestDescription(QString gameName, int modID, QVariant userData)`: Request description for a mod
- `void requestFiles(QString gameName, int modID, QVariant userData)`: Request a list of files for a mod
- `void requestFileInfo(QString game, int modID, int fileID, QVariant userData)`: Request info about a file
- `void requestDownloadURL(QString gameName, int modID, int fileID, QVariant userData)`: Request the download URL of a file
- `void requestToggleEndorsement(QString gameName, int modID, QString modVersion, bool endorse, QVariant userData)`: Request to toggle endorsement for a mod
- Various signals for repository-related events

## Game Features

### IGameFeatures

`IGameFeatures` is the interface for accessing game-specific features.

Key methods:
- `bool registerFeature(QStringList const& games, std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`: Register a game feature for specific games
- `bool registerFeature(IPluginGame* game, std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`: Register a game feature for a specific game
- `bool registerFeature(std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`: Register a game feature for all games
- `bool unregisterFeature(std::shared_ptr<GameFeature> feature)`: Unregister a game feature
- `template <BaseGameFeature Feature> int unregisterFeatures()`: Unregister all features of a given type
- `template <BaseGameFeature T> std::shared_ptr<T> gameFeature() const`: Get a game feature of a specific type

### Game Feature Types

Mod Organizer 2 provides several game feature interfaces that can be implemented to add game-specific functionality:

- `BSAInvalidation`: For handling BSA invalidation
  - `bool isInvalidationBSA(const QString& bsaName)`: Check if a BSA is an invalidation BSA
  - `void deactivate(MOBase::IProfile* profile)`: Deactivate BSA invalidation
  - `void activate(MOBase::IProfile* profile)`: Activate BSA invalidation
  - `bool prepareProfile(MOBase::IProfile* profile)`: Prepare a profile for BSA invalidation

- `DataArchives`: For managing data archives
  - `QStringList vanillaArchives() const`: Get the list of vanilla archives
  - `QStringList archives(const MOBase::IProfile* profile) const`: Get the list of archives for a profile
  - `void addArchive(MOBase::IProfile* profile, int index, const QString& archiveName)`: Add an archive
  - `void removeArchive(MOBase::IProfile* profile, const QString& archiveName)`: Remove an archive

- `GamePlugins`: For managing game plugins
  - `void writePluginLists(const MOBase::IPluginList* pluginList)`: Write plugin lists
  - `void readPluginLists(MOBase::IPluginList* pluginList)`: Read plugin lists
  - `QStringList getLoadOrder()`: Get the load order
  - `bool lightPluginsAreSupported()`: Check if light plugins are supported
  - `bool mediumPluginsAreSupported()`: Check if medium plugins are supported
  - `bool blueprintPluginsAreSupported()`: Check if blueprint plugins are supported

- `LocalSavegames`: For handling local savegames
  - `MappingType mappings(const QDir& profileSaveDir) const`: Get mappings for local savegames
  - `bool prepareProfile(MOBase::IProfile* profile)`: Prepare a profile for local savegames

- `ModDataChecker`: For checking mod data validity
  - `CheckReturn dataLooksValid(std::shared_ptr<const MOBase::IFileTree> fileTree) const`: Check if mod data looks valid
  - `std::shared_ptr<MOBase::IFileTree> fix(std::shared_ptr<MOBase::IFileTree> fileTree) const`: Try to fix invalid mod data

- `ModDataContent`: For determining mod content
  - `std::vector<Content> getAllContents() const`: Get all possible content types
  - `std::vector<int> getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const`: Get the content types in a mod

- `SaveGameInfo`: For handling savegame information
  - `MissingAssets getMissingAssets(MOBase::ISaveGame const& save) const`: Get missing assets from a save
  - `MOBase::ISaveGameInfoWidget* getSaveGameWidget(QWidget* parent = 0) const`: Get a widget to display save game information

- `ScriptExtender`: For handling script extenders
  - `QString BinaryName() const`: Get the name of the script extender binary
  - `QString PluginPath() const`: Get the script extender plugin path
  - `QString loaderName() const`: Get the loader name
  - `QString loaderPath() const`: Get the loader path
  - `QString savegameExtension() const`: Get the savegame extension
  - `bool isInstalled() const`: Check if the extender is installed
  - `QString getExtenderVersion() const`: Get the extender version
  - `WORD getArch() const`: Get the CPU platform of the extender

- `UnmanagedMods`: For handling unmanaged mods
  - `QStringList mods(bool onlyOfficial) const`: Get the list of unmanaged mods
  - `QString displayName(const QString& modName) const`: Get the display name of an unmanaged mod
  - `QFileInfo referenceFile(const QString& modName) const`: Get the reference file for an unmanaged mod
  - `QStringList secondaryFiles(const QString& modName) const`: Get the secondary files for an unmanaged mod
