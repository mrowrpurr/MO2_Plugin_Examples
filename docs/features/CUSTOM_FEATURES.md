# Creating Custom Game Features in MO2

This guide explains how to create custom game features in Mod Organizer 2 and associate them with specific games.

## Table of Contents

- [Creating Custom Game Features in MO2](#creating-custom-game-features-in-mo2)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Understanding Game Features](#understanding-game-features)
  - [Creating a Custom Game Feature](#creating-a-custom-game-feature)
    - [Step 1: Choose a Base Feature Type](#step-1-choose-a-base-feature-type)
    - [Step 2: Implement the Feature Interface](#step-2-implement-the-feature-interface)
    - [Step 3: Register the Feature](#step-3-register-the-feature)
      - [Option 1: From a Game Plugin](#option-1-from-a-game-plugin)
      - [Option 2: From Any Plugin](#option-2-from-any-plugin)
  - [Example: Custom ModDataContent Feature](#example-custom-moddatacontent-feature)
  - [Registering Features with Games](#registering-features-with-games)
    - [From a Game Plugin](#from-a-game-plugin)
    - [From a Regular Plugin](#from-a-regular-plugin)
    - [Priority and Replacement](#priority-and-replacement)
  - [Python Support](#python-support)
  - [Best Practices](#best-practices)

## Introduction

Game features in MO2 are specialized components that provide game-specific functionality. These features can be:

1. **Built into a game plugin**: Implemented directly in the game plugin class
2. **Registered by a separate plugin**: Created by any plugin and registered for specific games
3. **Custom implementations**: Created by you to extend or replace existing features

This guide focuses on creating custom game features and registering them with specific games.

## Understanding Game Features

MO2 provides several base game feature types:

- **BSAInvalidation**: Handles BSA invalidation for games that use BSA files
- **DataArchives**: Manages game archives (BSA, BA2, etc.)
- **GamePlugins**: Handles plugin management (ESP, ESM, ESL files)
- **LocalSavegames**: Manages save game handling
- **ModDataChecker**: Validates mod structure and content
- **ModDataContent**: Identifies and displays mod content types
- **SaveGameInfo**: Extracts information from save games
- **ScriptExtender**: Handles script extender integration
- **UnmanagedMods**: Manages DLCs and other unmanaged mods

Each feature has a specific interface that defines its functionality.

## Creating a Custom Game Feature

### Step 1: Choose a Base Feature Type

First, decide which base feature type you want to extend or replace. For example, if you want to create a custom mod content detector, you would extend `ModDataContent`.

### Step 2: Implement the Feature Interface

Create a class that inherits from the appropriate feature interface. For example:

```cpp
#include <game_features/moddatacontent.h>

class MyCustomModDataContent : public MOBase::ModDataContent
{
public:
    // Implement required methods
    std::vector<Content> getAllContents() const override;
    std::vector<int> getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const override;
};

std::vector<MOBase::ModDataContent::Content> MyCustomModDataContent::getAllContents() const
{
    // Define content types for your game
    std::vector<Content> contents;
    
    // Add content types with unique IDs, names, and icons
    contents.push_back(Content(1, "Custom Content 1", ":/MO/gui/content/plugin"));
    contents.push_back(Content(2, "Custom Content 2", ":/MO/gui/content/mesh"));
    
    return contents;
}

std::vector<int> MyCustomModDataContent::getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const
{
    std::vector<int> result;
    
    // Check for specific files or directories to determine content types
    if (fileTree->exists("meshes", MOBase::IFileTree::DIRECTORY)) {
        result.push_back(2); // Custom Content 2 (meshes)
    }
    
    if (fileTree->exists("plugins", MOBase::IFileTree::DIRECTORY)) {
        result.push_back(1); // Custom Content 1 (plugins)
    }
    
    return result;
}
```

### Step 3: Register the Feature

There are two main ways to register a game feature:

#### Option 1: From a Game Plugin

If you're creating a game plugin, you can register features in the `init` method:

```cpp
bool MyGamePlugin::init(MOBase::IOrganizer* organizer)
{
    // Call parent init
    IPluginGame::init(organizer);
    
    // Create and register features
    auto myContentFeature = std::make_shared<MyCustomModDataContent>();
    organizer->gameFeatures()->registerFeature(this, myContentFeature, 100);
    
    return true;
}
```

#### Option 2: From Any Plugin

Any plugin can register features for specific games:

```cpp
bool MyPlugin::init(MOBase::IOrganizer* organizer)
{
    // Create the feature
    auto myContentFeature = std::make_shared<MyCustomModDataContent>();
    
    // Register for specific games by name
    QStringList games = {"Skyrim", "Skyrim Special Edition"};
    organizer->gameFeatures()->registerFeature(games, myContentFeature, 100);
    
    return true;
}
```

## Example: Custom ModDataContent Feature

Here's a complete example of a custom `ModDataContent` feature for a hypothetical game:

```cpp
#include <game_features/moddatacontent.h>
#include <ifiletree.h>

class MyGameModDataContent : public MOBase::ModDataContent
{
public:
    // Define content types
    enum ContentType {
        TYPE_PLUGIN = 1,
        TYPE_TEXTURE = 2,
        TYPE_MESH = 3,
        TYPE_SOUND = 4,
        TYPE_SCRIPT = 5
    };
    
    std::vector<Content> getAllContents() const override
    {
        std::vector<Content> contents;
        
        // Define content types with IDs, names, and icons
        contents.push_back(Content(TYPE_PLUGIN, "Plugins", ":/MO/gui/content/plugin"));
        contents.push_back(Content(TYPE_TEXTURE, "Textures", ":/MO/gui/content/texture"));
        contents.push_back(Content(TYPE_MESH, "Meshes", ":/MO/gui/content/mesh"));
        contents.push_back(Content(TYPE_SOUND, "Sounds", ":/MO/gui/content/sound"));
        contents.push_back(Content(TYPE_SCRIPT, "Scripts", ":/MO/gui/content/script"));
        
        return contents;
    }
    
    std::vector<int> getContentsFor(std::shared_ptr<const MOBase::IFileTree> fileTree) const override
    {
        std::vector<int> result;
        
        // Check for specific directories or file patterns
        if (fileTree->exists("plugins", MOBase::IFileTree::DIRECTORY) ||
            !fileTree->find("*.plugin", MOBase::IFileTree::FILE).empty()) {
            result.push_back(TYPE_PLUGIN);
        }
        
        if (fileTree->exists("textures", MOBase::IFileTree::DIRECTORY)) {
            result.push_back(TYPE_TEXTURE);
        }
        
        if (fileTree->exists("meshes", MOBase::IFileTree::DIRECTORY)) {
            result.push_back(TYPE_MESH);
        }
        
        if (fileTree->exists("sounds", MOBase::IFileTree::DIRECTORY) ||
            fileTree->exists("music", MOBase::IFileTree::DIRECTORY)) {
            result.push_back(TYPE_SOUND);
        }
        
        if (fileTree->exists("scripts", MOBase::IFileTree::DIRECTORY) ||
            !fileTree->find("*.script", MOBase::IFileTree::FILE).empty()) {
            result.push_back(TYPE_SCRIPT);
        }
        
        return result;
    }
};
```

## Registering Features with Games

When registering a feature, you need to specify:

1. **Target games**: Which games should use this feature
2. **Priority**: Higher priority features override lower priority ones
3. **Replace flag**: Whether to replace existing features of the same type

### From a Game Plugin

In a game plugin, features are automatically associated with that game:

```cpp
bool MyGamePlugin::init(MOBase::IOrganizer* organizer)
{
    // Register features for this game
    auto myContentFeature = std::make_shared<MyGameModDataContent>();
    organizer->gameFeatures()->registerFeature(this, myContentFeature, 100);
    
    auto mySaveGameFeature = std::make_shared<MyGameSaveGameInfo>();
    organizer->gameFeatures()->registerFeature(this, mySaveGameFeature, 100);
    
    return true;
}
```

### From a Regular Plugin

Regular plugins can register features for specific games:

```cpp
bool MyPlugin::init(MOBase::IOrganizer* organizer)
{
    // Create features
    auto myContentFeature = std::make_shared<MyGameModDataContent>();
    
    // Register for specific games by name
    QStringList games = {"MyGame", "MyGameSpecialEdition"};
    organizer->gameFeatures()->registerFeature(games, myContentFeature, 100);
    
    // Register for all games (use with caution)
    auto myGenericFeature = std::make_shared<MyGenericFeature>();
    organizer->gameFeatures()->registerFeature(myGenericFeature, 50);
    
    // Register for a specific game plugin
    auto gamePlugin = organizer->getGame("MyGame");
    if (gamePlugin) {
        auto mySpecificFeature = std::make_shared<MySpecificFeature>();
        organizer->gameFeatures()->registerFeature(gamePlugin, mySpecificFeature, 100);
    }
    
    return true;
}
```

### Priority and Replacement

When registering features, you can control how they interact with existing features:

```cpp
// Register with high priority (will be used over lower priority features)
organizer->gameFeatures()->registerFeature(games, myFeature, 200);

// Replace existing features of the same type registered by this plugin
organizer->gameFeatures()->registerFeature(games, myFeature, 100, true);
```

## Python Support

Currently, game features can only be implemented in C++. Python plugins cannot create custom game features directly. However, Python plugins can still use the features provided by C++ plugins.

## Best Practices

1. **Use Unique IDs**: When creating content types or other identifiers, use unique values that won't conflict with other plugins.

2. **Check for Existing Features**: Before registering a feature, check if a similar feature already exists and consider whether you need to replace it or complement it.

3. **Appropriate Priority**: Use appropriate priority values:
   - 0-50: Low priority (fallback features)
   - 51-100: Normal priority (standard features)
   - 101-200: High priority (specialized features)
   - 201+: Very high priority (override features)

4. **Feature Compatibility**: Make sure your custom features are compatible with the games they target. Test thoroughly with different game versions and configurations.

5. **Documentation**: Document your custom features, especially if they're meant to be used by other plugins or shared with the community.

6. **Error Handling**: Implement proper error handling in your features to avoid crashes or unexpected behavior.

7. **Performance**: Be mindful of performance, especially for features that are called frequently, like ModDataContent's getContentsFor method.
