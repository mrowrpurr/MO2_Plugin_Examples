# Mod Organizer 2 Gamebryo Support Documentation

This document provides an overview of the classes and interfaces in the Mod Organizer 2 Gamebryo support library, which extends the UI Base functionality to support Gamebryo and Creation Engine based games like Skyrim, Oblivion, Fallout 3, Fallout New Vegas, and Fallout 4.

See also:
- [Diagrams](DIAGRAMS.md)
- [Plugin Development Guide](GUIDE.md)

## Table of Contents

- [Mod Organizer 2 Gamebryo Support Documentation](#mod-organizer-2-gamebryo-support-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Directory Structure](#directory-structure)
  - [Core Classes](#core-classes)
    - [GameGamebryo](#gamegamebryo)
  - [Game Features](#game-features)
    - [GamebryoBSAInvalidation](#gamebryobsainvalidation)
    - [GamebryoDataArchives](#gamebryodataarchives)
    - [GamebryoGamePlugins](#gamebryogameplugins)
    - [GamebryoLocalSaveGames](#gamebryolocalsavegames)
    - [GamebryoModDataChecker](#gamebryomoddatachecker)
    - [GamebryoModDataContent](#gamebryomoddatacontent)
    - [GamebryoSaveGame](#gamebryosavegame)
    - [GamebryoSaveGameInfo](#gamebryosavegameinfo)
    - [GamebryoScriptExtender](#gamebryoscriptextender)
    - [GamebryoUnmanagedMods](#gamebryounmanagedmods)
  - [Creation Engine Specific Classes](#creation-engine-specific-classes)
    - [CreationGamePlugins](#creationgameplugins)
  - [Utility Classes](#utility-classes)
    - [DummyBSA](#dummybsa)
    - [VDF Parser](#vdf-parser)

## Introduction

The Gamebryo support library provides base implementations for supporting Gamebryo and Creation Engine based games in Mod Organizer 2. It extends the UI Base interfaces with game-specific functionality for handling BSA files, plugin management, save games, and other features specific to these game engines.

The library is organized into two main components:
1. **Gamebryo** - Base implementation for Gamebryo engine games (Oblivion, Fallout 3, New Vegas, Skyrim LE)
2. **Creation** - Extensions for Creation Engine games (Skyrim SE, Fallout 4)

Game plugins for specific games (like Skyrim, Oblivion, etc.) inherit from these base classes and customize them as needed.

## Directory Structure

The library is organized into the following directories:

- `gamebryo/` - Contains the base implementation for Gamebryo engine games
- `creation/` - Contains extensions for Creation Engine games

## Core Classes

### GameGamebryo

`GameGamebryo` is the base class for all Gamebryo-based game plugins. It implements both `IPluginGame` and `IPluginFileMapper` interfaces from the UI Base library.

**Header**: `gamegamebryo.h`

**Key Methods**:
- `detectGame()` - Detects the game installation
- `init(MOBase::IOrganizer* moInfo)` - Initializes the game plugin
- `isInstalled() const` - Checks if the game is installed
- `gameDirectory() const` - Gets the game directory
- `dataDirectory() const` - Gets the data directory
- `setGamePath(const QString& path)` - Sets the game path
- `documentsDirectory() const` - Gets the documents directory
- `savesDirectory() const` - Gets the saves directory
- `gameVersion() const` - Gets the game version
- `getLauncherName() const` - Gets the launcher name
- `mappings() const` - Gets the file mappings for the virtual file system

**Protected Methods**:
- `savegameExtension() const` - Gets the save game extension (must be implemented by derived classes)
- `savegameSEExtension() const` - Gets the script extender save game extension (must be implemented by derived classes)
- `makeSaveGame(QString filepath) const` - Creates a save game object (must be implemented by derived classes)
- `identifyGamePath() const` - Identifies the game installation path
- `prepareIni(const QString& exec)` - Prepares INI files before running the game
- `registerFeature(std::shared_ptr<MOBase::GameFeature> feature)` - Registers a game feature

**Static Utility Methods**:
- `findInRegistry(HKEY baseKey, LPCWSTR path, LPCWSTR value)` - Finds a value in the Windows registry
- `getKnownFolderPath(REFKNOWNFOLDERID folderId, bool useDefault)` - Gets a known folder path
- `getSpecialPath(const QString& name)` - Gets a special path
- `determineMyGamesPath(const QString& gameName)` - Determines the "My Games" path
- `parseEpicGamesLocation(const QStringList& manifests)` - Parses the Epic Games location
- `parseSteamLocation(const QString& appid, const QString& directoryName)` - Parses the Steam location

## Game Features

### GamebryoBSAInvalidation

`GamebryoBSAInvalidation` implements the `BSAInvalidation` interface for Gamebryo games. It handles BSA invalidation, which is a technique used to make the game load loose files instead of BSA archives.

**Header**: `gamebryobsainvalidation.h`

**Key Methods**:
- `isInvalidationBSA(const QString& bsaName)` - Checks if a BSA is an invalidation BSA
- `deactivate(MOBase::IProfile* profile)` - Deactivates BSA invalidation
- `activate(MOBase::IProfile* profile)` - Activates BSA invalidation
- `prepareProfile(MOBase::IProfile* profile)` - Prepares a profile for BSA invalidation

**Protected Methods**:
- `invalidationBSAName() const` - Gets the name of the invalidation BSA (must be implemented by derived classes)
- `bsaVersion() const` - Gets the BSA version (must be implemented by derived classes)

### GamebryoDataArchives

`GamebryoDataArchives` implements the `DataArchives` interface for Gamebryo games. It handles the management of data archives (BSA files).

**Header**: `gamebryodataarchives.h`

**Key Methods**:
- `addArchive(MOBase::IProfile* profile, int index, const QString& archiveName)` - Adds an archive to the list
- `removeArchive(MOBase::IProfile* profile, const QString& archiveName)` - Removes an archive from the list

**Protected Methods**:
- `gameDirectory() const` - Gets the game directory
- `localGameDirectory() const` - Gets the local game directory
- `getArchivesFromKey(const QString& iniFile, const QString& key, int size = 256) const` - Gets archives from an INI key
- `setArchivesToKey(const QString& iniFile, const QString& key, const QString& value)` - Sets archives to an INI key
- `writeArchiveList(MOBase::IProfile* profile, const QStringList& before)` - Writes the archive list (must be implemented by derived classes)

### GamebryoGamePlugins

`GamebryoGamePlugins` implements the `GamePlugins` interface for Gamebryo games. It handles the management of game plugins (ESPs, ESMs, etc.).

**Header**: `gamebryogameplugins.h`

**Key Methods**:
- `writePluginLists(const MOBase::IPluginList* pluginList)` - Writes the plugin lists
- `readPluginLists(MOBase::IPluginList* pluginList)` - Reads the plugin lists
- `getLoadOrder()` - Gets the load order

**Protected Methods**:
- `writePluginList(const MOBase::IPluginList* pluginList, const QString& filePath)` - Writes the plugin list
- `writeLoadOrderList(const MOBase::IPluginList* pluginList, const QString& filePath)` - Writes the load order list
- `readLoadOrderList(MOBase::IPluginList* pluginList, const QString& filePath)` - Reads the load order list
- `readPluginList(MOBase::IPluginList* pluginList)` - Reads the plugin list

### GamebryoLocalSaveGames

`GamebryoLocalSaveGames` implements the `LocalSavegames` interface for Gamebryo games. It handles the management of local save games.

**Header**: `gamebryolocalsavegames.h`

**Key Methods**:
- `mappings(const QDir& profileSaveDir) const` - Gets the file mappings for save games
- `prepareProfile(MOBase::IProfile* profile)` - Prepares a profile for local save games

### GamebryoModDataChecker

`GamebryoModDataChecker` implements the `ModDataChecker` interface for Gamebryo games. It checks if mod data is valid for the game.

**Header**: `gamebryomoddatachecker.h`

**Key Methods**:
- `dataLooksValid(std::shared_ptr<const MOBase::IFileTree> fileTree) const` - Checks if the mod data looks valid
- `fix(std::shared_ptr<MOBase::IFileTree> fileTree) const` - Tries to fix invalid mod data

### GamebryoModDataContent

`GamebryoModDataContent` implements the `ModDataContent` interface for Gamebryo games. It determines the content of mods.

**Header**: `gamebryomoddatacontent.h`

**Key Methods**:
- `getAllContents() const` - Gets all possible content types
- `getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const` - Gets the content types in a mod

### GamebryoSaveGame

`GamebryoSaveGame` implements the `ISaveGame` interface for Gamebryo games. It represents a save game file.

**Header**: `gamebryosavegame.h`

**Key Methods**:
- `getCreationTime() const` - Gets the creation time of the save
- `getFilename() const` - Gets the filename of the save
- `getSaveGroupIdentifier() const` - Gets the save group identifier
- `allFiles() const` - Gets all files related to the save

### GamebryoSaveGameInfo

`GamebryoSaveGameInfo` implements the `SaveGameInfo` interface for Gamebryo games. It provides information about save games.

**Header**: `gamebryosavegameinfo.h`

**Key Methods**:
- `getMissingAssets(MOBase::ISaveGame const& save) const` - Gets missing assets from a save
- `getSaveGameWidget(QWidget* parent = 0) const` - Gets a widget to display save game information

### GamebryoScriptExtender

`GamebryoScriptExtender` implements the `ScriptExtender` interface for Gamebryo games. It handles script extenders like SKSE, OBSE, etc.

**Header**: `gamebryoscriptextender.h`

**Key Methods**:
- `BinaryName() const` - Gets the name of the script extender binary
- `PluginPath() const` - Gets the script extender plugin path
- `loaderName() const` - Gets the loader name
- `loaderPath() const` - Gets the loader path
- `savegameExtension() const` - Gets the savegame extension
- `isInstalled() const` - Checks if the extender is installed
- `getExtenderVersion() const` - Gets the extender version
- `getArch() const` - Gets the CPU platform of the extender

### GamebryoUnmanagedMods

`GamebryoUnmanagedMods` implements the `UnmanagedMods` interface for Gamebryo games. It handles unmanaged mods (like DLCs).

**Header**: `gamebryounmanagedmods.h`

**Key Methods**:
- `mods(bool onlyOfficial) const` - Gets the list of unmanaged mods
- `displayName(const QString& modName) const` - Gets the display name of an unmanaged mod
- `referenceFile(const QString& modName) const` - Gets the reference file for an unmanaged mod
- `secondaryFiles(const QString& modName) const` - Gets the secondary files for an unmanaged mod

## Creation Engine Specific Classes

### CreationGamePlugins

`CreationGamePlugins` extends `GamebryoGamePlugins` for Creation Engine games. It handles the management of game plugins for Creation Engine games, which have a different plugin format than Gamebryo games.

**Header**: `creationgameplugins.h`

**Key Methods**:
- `writePluginList(const MOBase::IPluginList* pluginList, const QString& filePath)` - Writes the plugin list
- `readPluginList(MOBase::IPluginList* pluginList)` - Reads the plugin list
- `getLoadOrder()` - Gets the load order
- `lightPluginsAreSupported()` - Checks if light plugins are supported

## Utility Classes

### DummyBSA

`DummyBSA` is a utility class for creating dummy BSA files for BSA invalidation.

**Header**: `dummybsa.h`

**Key Methods**:
- `write(const QString& fileName)` - Writes a dummy BSA file

### VDF Parser

`VDF_Parser` is a utility for parsing Valve Data Format (VDF) files, which are used by Steam.

**Header**: `vdf_parser.h`

**Key Methods**:
- `read(std::istream& stream)` - Reads a VDF file
