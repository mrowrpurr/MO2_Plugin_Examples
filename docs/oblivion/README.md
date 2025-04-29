# Mod Organizer 2 Oblivion Plugin Documentation

This document provides a detailed overview of the Oblivion plugin for Mod Organizer 2, explaining its structure, implementation, and how it extends the Gamebryo framework.

See also:
- [Diagrams](DIAGRAMS.md)

Miscellaneous note for someone forking this for the Oblivion Remaster (note this does not consider UE5):
- [Oblivion Remaster Recommendations / Notes](OBLIVION_REMASTER_RECOMMENDATIONS.md)

## Table of Contents

- [Mod Organizer 2 Oblivion Plugin Documentation](#mod-organizer-2-oblivion-plugin-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Plugin Structure](#plugin-structure)
  - [Core Classes](#core-classes)
    - [GameOblivion](#gameoblivion)
  - [Game Feature Implementations](#game-feature-implementations)
    - [OblivionBSAInvalidation](#oblivionbsainvalidation)
    - [OblivionDataArchives](#obliviondataarchives)
    - [OblivionModDataChecker](#oblivionmoddatachecker)
    - [OblivionModDataContent](#oblivionmoddatacontent)
    - [OblivionSaveGame](#oblivionsavegame)
    - [OblivionScriptExtender](#oblivionscriptextender)
  - [Gamebryo Features Used Directly](#gamebryo-features-used-directly)
    - [GamebryoGamePlugins](#gamebryogameplugins)
    - [GamebryoLocalSaveGames](#gamebryolocalsavegames)
    - [GamebryoSaveGameInfo](#gamebryosavegameinfo)
    - [GamebryoUnmanagedMods](#gamebryounmanagedmods)
  - [Build System](#build-system)
  - [Plugin Registration](#plugin-registration)

## Introduction

The Oblivion plugin for Mod Organizer 2 provides support for The Elder Scrolls IV: Oblivion. It extends the Gamebryo framework to handle Oblivion-specific features and file formats. The plugin is responsible for:

1. Detecting the Oblivion installation
2. Managing Oblivion plugins (ESPs, ESMs)
3. Handling Oblivion BSA archives
4. Managing Oblivion save games
5. Supporting the Oblivion Script Extender (OBSE)
6. Validating mod data for Oblivion
7. Identifying mod content types for Oblivion

## Plugin Structure

The Oblivion plugin is structured as a set of classes that extend the Gamebryo framework. The main class is `GameOblivion`, which inherits from `GameGamebryo` and implements the `IPluginGame` interface. The plugin also includes several Oblivion-specific implementations of game features, such as `OblivionBSAInvalidation`, `OblivionDataArchives`, etc.

The plugin uses a mix of custom implementations and direct usage of Gamebryo features. For example, it implements its own BSA invalidation and data archives features, but uses the Gamebryo implementations for game plugins and local save games.

## Core Classes

### GameOblivion

`GameOblivion` is the main class of the Oblivion plugin. It inherits from `GameGamebryo` and implements the `IPluginGame` interface. This class is responsible for initializing the plugin and registering all the game features.

**Key Methods:**
- `init(IOrganizer* moInfo)`: Initializes the plugin and registers all the game features
- `gameName() const`: Returns the name of the game ("Oblivion")
- `executables() const`: Returns a list of executables associated with Oblivion
- `executableForcedLoads() const`: Returns a list of DLLs that should be force-loaded with certain executables
- `initializeProfile(const QDir& path, ProfileSettings settings) const`: Initializes a profile for Oblivion
- `steamAPPId() const`: Returns the Steam App ID for Oblivion ("22330")
- `primaryPlugins() const`: Returns a list of primary plugins for Oblivion ("oblivion.esm", "update.esm")
- `gameShortName() const`: Returns the short name of the game ("Oblivion")
- `validShortNames() const`: Returns a list of valid short names for the game (includes "Nehrim" if enabled)
- `gameNexusName() const`: Returns the name of the game on Nexus Mods ("Oblivion")
- `iniFiles() const`: Returns a list of INI files used by Oblivion ("oblivion.ini", "oblivionprefs.ini")
- `DLCPlugins() const`: Returns a list of DLC plugins for Oblivion
- `savegameExtension() const`: Returns the extension for Oblivion save games ("ess")
- `savegameSEExtension() const`: Returns the extension for OBSE save games ("obse")
- `makeSaveGame(QString filePath) const`: Creates a save game object for Oblivion

**Plugin Registration:**
In the `init` method, the plugin registers the following game features:
- `OblivionScriptExtender`
- `OblivionDataArchives`
- `OblivionBSAInvalidation`
- `GamebryoSaveGameInfo`
- `GamebryoLocalSaveGames`
- `OblivionModDataChecker`
- `OblivionModDataContent`
- `GamebryoGamePlugins`
- `GamebryoUnmanagedMods`

## Game Feature Implementations

### OblivionBSAInvalidation

`OblivionBSAInvalidation` extends `GamebryoBSAInvalidation` to provide Oblivion-specific BSA invalidation. BSA invalidation is a technique used to make the game load loose files instead of BSA archives.

**Key Methods:**
- `invalidationBSAName() const`: Returns the name of the invalidation BSA for Oblivion ("Oblivion - Invalidation.bsa")
- `bsaVersion() const`: Returns the BSA version for Oblivion (0x67)

### OblivionDataArchives

`OblivionDataArchives` extends `GamebryoDataArchives` to provide Oblivion-specific data archive management. This class is responsible for managing the list of BSA archives that Oblivion loads.

**Key Methods:**
- `vanillaArchives() const`: Returns a list of vanilla BSA archives for Oblivion
- `archives(const MOBase::IProfile* profile) const`: Returns a list of BSA archives for a profile
- `writeArchiveList(MOBase::IProfile* profile, const QStringList& before)`: Writes the list of BSA archives to the INI file

### OblivionModDataChecker

`OblivionModDataChecker` extends `GamebryoModDataChecker` to provide Oblivion-specific mod data validation. This class is responsible for checking if mod data is valid for Oblivion.

**Key Methods:**
- `dataLooksValid(std::shared_ptr<const MOBase::IFileTree> fileTree) const`: Checks if mod data looks valid for Oblivion
- `fix(std::shared_ptr<MOBase::IFileTree> fileTree) const`: Tries to fix invalid mod data
- `possibleFolderNames() const`: Returns a list of possible folder names for Oblivion mods
- `possibleFileExtensions() const`: Returns a list of possible file extensions for Oblivion mods

The `dataLooksValid` method first checks with the Gamebryo implementation, and if that fails, it checks for OBSE files. If all files start with "OBSE", it returns `FIXABLE`.

The `fix` method creates a new file tree with an "OBSE/Plugins" directory and moves all files there.

### OblivionModDataContent

`OblivionModDataContent` extends `GamebryoModDataContent` to provide Oblivion-specific mod content identification. This class is responsible for determining the content types of mods for Oblivion.

The class simply disables some content types that are not applicable to Oblivion:
- `CONTENT_MCM` (Mod Configuration Menu, used in Skyrim)
- `CONTENT_SKYPROC` (SkyProc patchers, used in Skyrim)

### OblivionSaveGame

`OblivionSaveGame` extends `GamebryoSaveGame` to provide Oblivion-specific save game handling. This class is responsible for reading Oblivion save game files.

**Key Methods:**
- `fetchInformationFields(FileWrapper& wrapper, unsigned long& saveNumber, QString& playerName, unsigned short& playerLevel, QString& playerLocation, SYSTEMTIME& creationTime) const`: Fetches basic information from the save game
- `fetchDataFields() const`: Fetches additional data from the save game, including the screenshot and plugin list

The class reads the Oblivion save game format, which starts with the header "TES4SAVEGAME".

### OblivionScriptExtender

`OblivionScriptExtender` extends `GamebryoScriptExtender` to provide Oblivion-specific script extender support. This class is responsible for handling the Oblivion Script Extender (OBSE).

**Key Methods:**
- `BinaryName() const`: Returns the name of the OBSE binary ("obse_loader.exe")
- `PluginPath() const`: Returns the path to OBSE plugins ("obse/plugins")

## Gamebryo Features Used Directly

The Oblivion plugin uses some Gamebryo features directly, without extending them:

### GamebryoGamePlugins

The Oblivion plugin uses `GamebryoGamePlugins` directly for managing game plugins (ESPs, ESMs). This class is responsible for reading and writing the plugins.txt and loadorder.txt files.

### GamebryoLocalSaveGames

The Oblivion plugin uses `GamebryoLocalSaveGames` directly for managing local save games. This class is responsible for mapping save game files between the game directory and the profile directory.

### GamebryoSaveGameInfo

The Oblivion plugin uses `GamebryoSaveGameInfo` directly for providing save game information. This class is responsible for getting information about save games, such as missing assets.

### GamebryoUnmanagedMods

The Oblivion plugin uses `GamebryoUnmanagedMods` directly for handling unmanaged mods. This class is responsible for identifying and managing mods that are installed outside of Mod Organizer 2, such as DLCs.

## Build System

The Oblivion plugin uses CMake for its build system. The main CMakeLists.txt file includes the common MO2 CMake file and adds the src subdirectory. The src/CMakeLists.txt file configures the plugin with the `mo2_configure_plugin` macro, specifying that it depends on the gamebryo library.

## Plugin Registration

The Oblivion plugin is registered with Mod Organizer 2 using the Qt plugin system. The `GameOblivion` class has the `Q_PLUGIN_METADATA` macro with the IID "org.tannin.GameOblivion" and the file "gameoblivion.json". The JSON file is empty, as all the plugin information is provided by the `GameOblivion` class methods.
