# MO2 Game Features Guide

This guide provides practical instructions for using and implementing game features in Mod Organizer 2 (MO2). It's intended for plugin developers who want to add or customize game-specific functionality.

## Table of Contents

- [MO2 Game Features Guide](#mo2-game-features-guide)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [When to Use Game Features](#when-to-use-game-features)
  - [Implementing Game Features](#implementing-game-features)
    - [Step 1: Choose the Feature Type](#step-1-choose-the-feature-type)
    - [Step 2: Create the Feature Implementation](#step-2-create-the-feature-implementation)
    - [Step 3: Register the Feature](#step-3-register-the-feature)
    - [Step 4: Test the Feature](#step-4-test-the-feature)
  - [Feature Implementation Examples](#feature-implementation-examples)
    - [BSA Invalidation Example](#bsa-invalidation-example)
    - [Data Archives Example](#data-archives-example)
    - [Game Plugins Example](#game-plugins-example)
    - [Mod Data Content Example](#mod-data-content-example)
  - [Advanced Topics](#advanced-topics)
    - [Feature Priorities](#feature-priorities)
    - [Feature Replacement](#feature-replacement)
    - [Combining Features](#combining-features)
    - [Feature Dependencies](#feature-dependencies)
  - [Troubleshooting](#troubleshooting)
    - [Feature Not Being Used](#feature-not-being-used)
    - [Feature Not Working Correctly](#feature-not-working-correctly)
  - [Best Practices](#best-practices)
    - [Use Existing Features as a Reference](#use-existing-features-as-a-reference)
    - [Handle Errors Gracefully](#handle-errors-gracefully)
    - [Document Your Implementation](#document-your-implementation)
    - [Test Your Implementation](#test-your-implementation)
    - [Keep It Simple](#keep-it-simple)
    - [Follow MO2 Conventions](#follow-mo2-conventions)

## Introduction

Game Features in MO2 are specialized components that provide game-specific functionality. They allow MO2 to support different games by abstracting game-specific operations into well-defined interfaces. Each game plugin can implement these features to provide the necessary functionality for a specific game.

This guide will walk you through the process of implementing and registering game features for your game plugin.

## When to Use Game Features

You should implement game features when:

1. **Adding Support for a New Game**: If you're creating a plugin to add support for a new game, you'll need to implement the relevant game features for that game.

2. **Extending Existing Game Support**: If you want to add or modify functionality for a game that's already supported, you can implement specific game features to override or extend the existing ones.

3. **Creating Shared Functionality**: If you have functionality that can be shared across multiple games, you can implement it as a game feature and register it for multiple games.

## Implementing Game Features

### Step 1: Choose the Feature Type

First, decide which feature type(s) you need to implement. MO2 provides several built-in feature types:

- **BSAInvalidation**: For managing BSA invalidation.
- **DataArchives**: For managing data archives (BSA files).
- **GamePlugins**: For managing game plugins (ESP, ESM, ESL files).
- **LocalSavegames**: For managing local save games.
- **ModDataChecker**: For validating and fixing mod data structures.
- **ModDataContent**: For providing information about mod content.
- **SaveGameInfo**: For providing information about save games.
- **ScriptExtender**: For managing script extenders.
- **UnmanagedMods**: For managing unmanaged mods (DLCs, etc.).

Choose the feature type(s) that are relevant to your game and that you want to customize.

### Step 2: Create the Feature Implementation

Create a class that inherits from the appropriate feature interface and implements all the required methods. For example, to implement BSA invalidation:

```cpp
#include <bsainvalidation.h>

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

### Step 3: Register the Feature

Register your feature implementation with the Game Features Manager in your game plugin's `init` method:

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

### Step 4: Test the Feature

Test your feature implementation to ensure it works correctly. This may involve:

- Testing with different profiles
- Testing with different mod configurations
- Testing with different game versions
- Testing with different MO2 versions

## Feature Implementation Examples

### BSA Invalidation Example

BSA Invalidation is used to ensure that loose files (files not in a BSA) are loaded before the contents of BSA files. This is necessary for some games to allow mods to override the contents of BSA files.

```cpp
class SkyrimBSAInvalidation : public MOBase::BSAInvalidation
{
public:
    bool isInvalidationBSA(const QString& bsaName) override
    {
        return bsaName.compare("Skyrim - Invalidation.bsa", Qt::CaseInsensitive) == 0;
    }

    void deactivate(MOBase::IProfile* profile) override
    {
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (QFile::exists(iniPath)) {
            QSettings ini(iniPath, QSettings::IniFormat);
            ini.setValue("Archive/bInvalidateOlderFiles", false);
            ini.sync();
        }
    }

    void activate(MOBase::IProfile* profile) override
    {
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (QFile::exists(iniPath)) {
            QSettings ini(iniPath, QSettings::IniFormat);
            ini.setValue("Archive/bInvalidateOlderFiles", true);
            ini.sync();
        }
    }

    bool prepareProfile(MOBase::IProfile* profile) override
    {
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (!QFile::exists(iniPath)) {
            return false;
        }
        return true;
    }
};
```

### Data Archives Example

Data Archives manages the list of data archives (BSA files) that are loaded by the game. This includes both the vanilla archives (those that come with the base game) and any additional archives added by mods.

```cpp
class SkyrimDataArchives : public MOBase::DataArchives
{
public:
    QStringList vanillaArchives() const override
    {
        return {
            "Skyrim - Misc.bsa",
            "Skyrim - Shaders.bsa",
            "Skyrim - Textures.bsa",
            "Skyrim - Interface.bsa",
            "Skyrim - Animations.bsa",
            "Skyrim - Meshes.bsa",
            "Skyrim - Sounds.bsa",
            "Skyrim - Voices.bsa",
            "Skyrim - VoicesExtra.bsa"
        };
    }

    QStringList archives(const MOBase::IProfile* profile) const override
    {
        QStringList result;
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (QFile::exists(iniPath)) {
            QSettings ini(iniPath, QSettings::IniFormat);
            QString archiveList = ini.value("Archive/sResourceArchiveList").toString();
            result = archiveList.split(", ", Qt::SkipEmptyParts);
        }
        return result;
    }

    void addArchive(MOBase::IProfile* profile, int index, const QString& archiveName) override
    {
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (QFile::exists(iniPath)) {
            QSettings ini(iniPath, QSettings::IniFormat);
            QString archiveList = ini.value("Archive/sResourceArchiveList").toString();
            QStringList archives = archiveList.split(", ", Qt::SkipEmptyParts);
            if (!archives.contains(archiveName, Qt::CaseInsensitive)) {
                archives.insert(index, archiveName);
                ini.setValue("Archive/sResourceArchiveList", archives.join(", "));
                ini.sync();
            }
        }
    }

    void removeArchive(MOBase::IProfile* profile, const QString& archiveName) override
    {
        QString iniPath = profile->absoluteIniFilePath("Skyrim.ini");
        if (QFile::exists(iniPath)) {
            QSettings ini(iniPath, QSettings::IniFormat);
            QString archiveList = ini.value("Archive/sResourceArchiveList").toString();
            QStringList archives = archiveList.split(", ", Qt::SkipEmptyParts);
            archives.removeAll(archiveName);
            ini.setValue("Archive/sResourceArchiveList", archives.join(", "));
            ini.sync();
        }
    }
};
```

### Game Plugins Example

Game Plugins manages the game's plugin system, including reading and writing plugin lists and determining the load order.

```cpp
class SkyrimGamePlugins : public MOBase::GamePlugins
{
public:
    void writePluginLists(const MOBase::IPluginList* pluginList) override
    {
        QStringList plugins;
        QStringList loadOrder;
        
        // Get enabled plugins
        for (const QString& pluginName : pluginList->pluginNames()) {
            if (pluginList->state(pluginName) == MOBase::IPluginList::STATE_ACTIVE) {
                plugins.append(pluginName);
            }
        }
        
        // Get load order
        loadOrder = pluginList->pluginNames();
        
        // Write plugins.txt
        QString pluginsPath = QDir::fromNativeSeparators(qApp->property("dataPath").toString() + "/plugins.txt");
        QFile pluginsFile(pluginsPath);
        if (pluginsFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream out(&pluginsFile);
            for (const QString& plugin : plugins) {
                out << plugin << "\n";
            }
            pluginsFile.close();
        }
        
        // Write loadorder.txt
        QString loadOrderPath = QDir::fromNativeSeparators(qApp->property("dataPath").toString() + "/loadorder.txt");
        QFile loadOrderFile(loadOrderPath);
        if (loadOrderFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream out(&loadOrderFile);
            for (const QString& plugin : loadOrder) {
                out << plugin << "\n";
            }
            loadOrderFile.close();
        }
    }

    void readPluginLists(MOBase::IPluginList* pluginList) override
    {
        // Read plugins.txt
        QString pluginsPath = QDir::fromNativeSeparators(qApp->property("dataPath").toString() + "/plugins.txt");
        QFile pluginsFile(pluginsPath);
        QStringList plugins;
        if (pluginsFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
            QTextStream in(&pluginsFile);
            while (!in.atEnd()) {
                QString line = in.readLine().trimmed();
                if (!line.isEmpty() && !line.startsWith("#")) {
                    plugins.append(line);
                }
            }
            pluginsFile.close();
        }
        
        // Read loadorder.txt
        QString loadOrderPath = QDir::fromNativeSeparators(qApp->property("dataPath").toString() + "/loadorder.txt");
        QFile loadOrderFile(loadOrderPath);
        QStringList loadOrder;
        if (loadOrderFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
            QTextStream in(&loadOrderFile);
            while (!in.atEnd()) {
                QString line = in.readLine().trimmed();
                if (!line.isEmpty() && !line.startsWith("#")) {
                    loadOrder.append(line);
                }
            }
            loadOrderFile.close();
        }
        
        // Set plugin states and load order
        for (const QString& pluginName : pluginList->pluginNames()) {
            MOBase::IPluginList::PluginState state = plugins.contains(pluginName) ? 
                MOBase::IPluginList::STATE_ACTIVE : MOBase::IPluginList::STATE_INACTIVE;
            pluginList->setState(pluginName, state);
        }
        
        pluginList->setLoadOrder(loadOrder);
    }

    QStringList getLoadOrder() override
    {
        QStringList result;
        QString loadOrderPath = QDir::fromNativeSeparators(qApp->property("dataPath").toString() + "/loadorder.txt");
        QFile loadOrderFile(loadOrderPath);
        if (loadOrderFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
            QTextStream in(&loadOrderFile);
            while (!in.atEnd()) {
                QString line = in.readLine().trimmed();
                if (!line.isEmpty() && !line.startsWith("#")) {
                    result.append(line);
                }
            }
            loadOrderFile.close();
        }
        return result;
    }

    bool lightPluginsAreSupported() override
    {
        return false; // Skyrim LE doesn't support light plugins
    }
};
```

### Mod Data Content Example

Mod Data Content provides information about the content of mods, such as whether they contain textures, meshes, scripts, etc. This information is displayed in the "Content" column of the mod list.

```cpp
class SkyrimModDataContent : public MOBase::ModDataContent
{
public:
    std::vector<Content> getAllContents() const override
    {
        return {
            Content(1, "Plugin", ":/MO/gui/content/plugin"),
            Content(2, "Texture", ":/MO/gui/content/texture"),
            Content(3, "Mesh", ":/MO/gui/content/mesh"),
            Content(4, "BSA", ":/MO/gui/content/bsa"),
            Content(5, "Script", ":/MO/gui/content/script"),
            Content(6, "SKSE Plugin", ":/MO/gui/content/skse"),
            Content(7, "Sound", ":/MO/gui/content/sound"),
            Content(8, "Interface", ":/MO/gui/content/interface")
        };
    }

    std::vector<int> getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const override
    {
        std::vector<int> result;
        
        // Check for plugins
        for (const auto& entry : fileTree->find("*.esp", MOBase::IFileTree::FILE_ONLY)) {
            result.push_back(1); // Plugin
            break;
        }
        
        // Check for textures
        if (fileTree->exists("textures")) {
            result.push_back(2); // Texture
        }
        
        // Check for meshes
        if (fileTree->exists("meshes")) {
            result.push_back(3); // Mesh
        }
        
        // Check for BSAs
        for (const auto& entry : fileTree->find("*.bsa", MOBase::IFileTree::FILE_ONLY)) {
            result.push_back(4); // BSA
            break;
        }
        
        // Check for scripts
        if (fileTree->exists("scripts")) {
            result.push_back(5); // Script
        }
        
        // Check for SKSE plugins
        if (fileTree->exists("SKSE/Plugins")) {
            result.push_back(6); // SKSE Plugin
        }
        
        // Check for sounds
        if (fileTree->exists("sound")) {
            result.push_back(7); // Sound
        }
        
        // Check for interface files
        if (fileTree->exists("interface")) {
            result.push_back(8); // Interface
        }
        
        return result;
    }
};
```

## Advanced Topics

### Feature Priorities

When registering a feature, you can specify a priority value. This value determines the order in which features are applied (for features that can be combined) or which feature is used (for features that cannot be combined).

Higher priority values take precedence. For example, if two plugins register a BSA Invalidation feature for the same game, the one with the higher priority will be used.

```cpp
// Register with high priority (100)
organizer->gameFeatures()->registerFeature(this, bsaInvalidation, 100);

// Register with low priority (50)
organizer->gameFeatures()->registerFeature(this, bsaInvalidation, 50);
```

### Feature Replacement

When registering a feature, you can specify whether it should replace existing features of the same type registered by the same plugin. If `true`, existing features are removed before the new feature is registered.

```cpp
// Replace existing features
organizer->gameFeatures()->registerFeature(this, bsaInvalidation, 100, true);

// Don't replace existing features (default)
organizer->gameFeatures()->registerFeature(this, bsaInvalidation, 100, false);
```

### Combining Features

Some features can be combined, while others cannot. For features that can be combined (like ModDataContent), all registered features are used, with the priority determining the order in which they are applied. For features that cannot be combined (like BSAInvalidation), only the feature with the highest priority is used.

### Feature Dependencies

Some features may depend on other features. For example, a feature that provides information about save games may depend on a feature that provides information about the game's plugin system.

When implementing features with dependencies, you should check if the required features are available and handle the case where they are not.

```cpp
bool MyGamePlugin::init(MOBase::IOrganizer* organizer)
{
    // Check if required features are available
    auto gamePlugins = organizer->gameFeatures()->gameFeature<MOBase::GamePlugins>();
    if (!gamePlugins) {
        qWarning() << "GamePlugins feature not available, some functionality may be limited";
    }
    
    // Register features
    // ...
    
    return true;
}
```

## Troubleshooting

### Feature Not Being Used

If your feature is not being used, check the following:

1. **Registration**: Make sure you're registering the feature correctly.
2. **Priority**: Make sure your feature has a high enough priority to be selected.
3. **Game Association**: Make sure you're registering the feature for the correct game.
4. **Plugin Enabled**: Make sure your plugin is enabled in MO2.

### Feature Not Working Correctly

If your feature is being used but not working correctly, check the following:

1. **Implementation**: Make sure your feature implementation is correct.
2. **Dependencies**: Make sure any required dependencies are available.
3. **Game Configuration**: Make sure the game is configured correctly.
4. **MO2 Configuration**: Make sure MO2 is configured correctly.

## Best Practices

### Use Existing Features as a Reference

When implementing a new feature, look at existing implementations for similar games as a reference. This can help you understand how the feature should be implemented and what conventions to follow.

### Handle Errors Gracefully

Your feature implementation should handle errors gracefully and provide meaningful error messages. This will help users understand what went wrong and how to fix it.

```cpp
bool MyFeature::someMethod()
{
    try {
        // Implementation
        return true;
    } catch (const std::exception& e) {
        qWarning() << "Error in MyFeature::someMethod:" << e.what();
        return false;
    }
}
```

### Document Your Implementation

Document your feature implementation, especially any non-obvious behavior or requirements. This will help other developers understand your code and make it easier to maintain.

```cpp
/**
 * @brief Check if a BSA file is an invalidation BSA.
 * 
 * An invalidation BSA is a special BSA file that is used to force the game to reload
 * loose files. This is necessary for some games to allow mods to override the contents
 * of BSA files.
 * 
 * @param bsaName The name of the BSA file to check.
 * @return True if the BSA file is an invalidation BSA, false otherwise.
 */
bool isInvalidationBSA(const QString& bsaName) override;
```

### Test Your Implementation

Test your feature implementation thoroughly to ensure it works correctly in all scenarios. This includes testing with different profiles, mod configurations, game versions, and MO2 versions.

### Keep It Simple

Keep your feature implementation as simple as possible while still meeting the requirements. This will make it easier to maintain and less likely to contain bugs.

### Follow MO2 Conventions

Follow MO2's coding conventions and design patterns. This will make your code more consistent with the rest of MO2 and easier for other developers to understand.
