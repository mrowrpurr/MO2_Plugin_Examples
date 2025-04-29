# MO2 Game Features Documentation

## Table of Contents

- [MO2 Game Features Documentation](#mo2-game-features-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Game Feature Architecture](#game-feature-architecture)
  - [Game Feature Types](#game-feature-types)
    - [BSA Invalidation](#bsa-invalidation)
    - [Data Archives](#data-archives)
    - [Game Plugins](#game-plugins)
    - [Local Savegames](#local-savegames)
    - [Mod Data Checker](#mod-data-checker)
    - [Mod Data Content](#mod-data-content)
    - [Save Game Info](#save-game-info)
    - [Script Extender](#script-extender)
    - [Unmanaged Mods](#unmanaged-mods)
  - [Game Features Manager](#game-features-manager)
  - [Implementing Game Features](#implementing-game-features)
  - [Registering Game Features](#registering-game-features)

## Introduction

Game Features in Mod Organizer 2 (MO2) are specialized components that provide game-specific functionality. They allow MO2 to support different games by abstracting game-specific operations into well-defined interfaces. Each game plugin can implement these features to provide the necessary functionality for a specific game.

Game Features are designed to be modular and extensible, allowing for easy addition of new features and customization of existing ones. They are also designed to be shareable between games, so that common functionality can be reused.

## Game Feature Architecture

The Game Features system is built around a few key components:

1. **GameFeature**: The base class for all game features. It's an abstract class that provides the basic interface for all game features.

2. **GameFeatureCRTP**: A template class that uses the Curiously Recurring Template Pattern (CRTP) to provide type information for derived classes.

3. **IGameFeatures**: The interface for managing game features. It provides methods for registering and retrieving game features.

4. **Specific Feature Classes**: Concrete classes that implement specific game features, such as BSAInvalidation, DataArchives, etc.

The architecture uses a type-based system to identify and retrieve game features. Each feature class has a unique type, and the IGameFeatures interface uses this type information to manage and retrieve features.

## Game Feature Types

MO2 provides several built-in game feature types, each serving a specific purpose:

### BSA Invalidation

**Interface**: `BSAInvalidation`

BSA Invalidation is used to manage the invalidation of BSA (Bethesda Softworks Archive) files. This is necessary for some games to ensure that loose files (files not in a BSA) are loaded before the contents of BSA files.

Key methods:
- `isInvalidationBSA`: Checks if a BSA file is an invalidation BSA.
- `deactivate`: Deactivates BSA invalidation for a profile.
- `activate`: Activates BSA invalidation for a profile.
- `prepareProfile`: Prepares a profile for BSA invalidation.

### Data Archives

**Interface**: `DataArchives`

Data Archives manages the list of data archives (BSA files) that are loaded by the game. This includes both the vanilla archives (those that come with the base game) and any additional archives added by mods.

Key methods:
- `vanillaArchives`: Returns the list of vanilla archives.
- `archives`: Returns the list of archives for a profile.
- `addArchive`: Adds an archive to the list.
- `removeArchive`: Removes an archive from the list.

### Game Plugins

**Interface**: `GamePlugins`

Game Plugins manages the game's plugin system, including reading and writing plugin lists and determining the load order.

Key methods:
- `writePluginLists`: Writes the plugin list to the game's configuration.
- `readPluginLists`: Reads the plugin list from the game's configuration.
- `getLoadOrder`: Returns the load order of plugins.
- `lightPluginsAreSupported`: Checks if light plugins (ESL files) are supported.
- `mediumPluginsAreSupported`: Checks if medium plugins are supported.
- `blueprintPluginsAreSupported`: Checks if blueprint plugins are supported.

### Local Savegames

**Interface**: `LocalSavegames`

Local Savegames manages the game's save files, including mapping them between the game's save directory and MO2's profile-specific save directory.

Key methods:
- `mappings`: Returns the mappings between the game's save directory and the profile's save directory.
- `prepareProfile`: Prepares a profile for local save games.

### Mod Data Checker

**Interface**: `ModDataChecker`

Mod Data Checker is used to validate and fix mod data structures. It checks if a mod's file structure is valid for the game and can attempt to fix invalid structures.

Key methods:
- `dataLooksValid`: Checks if the mod data looks valid.
- `fix`: Attempts to fix invalid mod data.

### Mod Data Content

**Interface**: `ModDataContent`

Mod Data Content provides information about the content of mods, such as whether they contain textures, meshes, scripts, etc. This information is displayed in the "Content" column of the mod list.

Key methods:
- `getAllContents`: Returns all possible content types.
- `getContentsFor`: Returns the content types present in a mod.

### Save Game Info

**Interface**: `SaveGameInfo`

Save Game Info provides information about save games, including missing assets and a widget for displaying save game information.

Key methods:
- `getMissingAssets`: Returns a list of assets that are missing from a save game.
- `getSaveGameWidget`: Returns a widget for displaying save game information.

### Script Extender

**Interface**: `ScriptExtender`

Script Extender provides information about the game's script extender, such as SKSE for Skyrim or F4SE for Fallout 4.

Key methods:
- `BinaryName`: Returns the name of the script extender binary.
- `PluginPath`: Returns the path to the script extender plugins.
- `loaderName`: Returns the name of the loader used to run the game with the script extender.
- `loaderPath`: Returns the path to the loader.
- `savegameExtension`: Returns the extension used for script extender save games.
- `isInstalled`: Checks if the script extender is installed.
- `getExtenderVersion`: Returns the version of the script extender.
- `getArch`: Returns the architecture (32-bit or 64-bit) of the script extender.

### Unmanaged Mods

**Interface**: `UnmanagedMods`

Unmanaged Mods provides information about mods that are installed outside of MO2's management, such as DLCs or mods installed directly to the game's data directory.

Key methods:
- `mods`: Returns a list of unmanaged mods.
- `displayName`: Returns the display name of an unmanaged mod.
- `referenceFile`: Returns a reference file for an unmanaged mod.
- `secondaryFiles`: Returns a list of secondary files for an unmanaged mod.

## Game Features Manager

The Game Features Manager (`IGameFeatures`) is responsible for registering and retrieving game features. It provides methods for:

- Registering a feature for specific games or all games.
- Unregistering a feature.
- Retrieving a feature by type.

Features can be registered with different priorities, allowing for override or extension of existing features. For features that can be combined (like ModDataContent), the priority determines the order in which they are applied. For features that cannot be combined, the feature with the highest priority is used.

## Implementing Game Features

To implement a game feature, you need to:

1. Create a class that inherits from the appropriate feature interface (e.g., `BSAInvalidation`, `DataArchives`, etc.).
2. Implement all the required methods of the interface.
3. Register the feature with the Game Features Manager.

Here's an example of implementing a simple BSA Invalidation feature:

```cpp
class MyBSAInvalidation : public MOBase::BSAInvalidation
{
public:
    bool isInvalidationBSA(const QString& bsaName) override
    {
        // Implementation
        return bsaName.contains("Invalidation.bsa");
    }

    void deactivate(MOBase::IProfile* profile) override
    {
        // Implementation
    }

    void activate(MOBase::IProfile* profile) override
    {
        // Implementation
    }

    bool prepareProfile(MOBase::IProfile* profile) override
    {
        // Implementation
        return true;
    }
};
```

## Registering Game Features

Once you've implemented a game feature, you need to register it with the Game Features Manager. This is typically done in the `init` method of your game plugin:

```cpp
bool MyGamePlugin::init(MOBase::IOrganizer* organizer)
{
    // Create and register BSA Invalidation feature
    auto bsaInvalidation = std::make_shared<MyBSAInvalidation>();
    organizer->gameFeatures()->registerFeature(this, bsaInvalidation, 100);

    // Create and register other features...

    return true;
}
```

You can register a feature for:

- A specific game: `registerFeature(IPluginGame* game, std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`
- Multiple games: `registerFeature(QStringList const& games, std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`
- All games: `registerFeature(std::shared_ptr<GameFeature> feature, int priority, bool replace = false)`

The `priority` parameter determines the order in which features are applied (for features that can be combined) or which feature is used (for features that cannot be combined). Higher priority values take precedence.

The `replace` parameter determines whether the feature should replace existing features of the same type registered by the same plugin. If `true`, existing features are removed before the new feature is registered.
