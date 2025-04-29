# Recommendations for Creating an Oblivion Remastered Plugin

This document provides recommendations for creating a plugin for Oblivion Remastered based on the existing Oblivion plugin. It outlines the changes needed to adapt the Oblivion plugin to work with Oblivion Remastered.

## Table of Contents

- [Recommendations for Creating an Oblivion Remastered Plugin](#recommendations-for-creating-an-oblivion-remastered-plugin)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Setup](#project-setup)
  - [Core Class Modifications](#core-class-modifications)
    - [GameOblivionRemastered](#gameoblivionremastered)
  - [Game Feature Modifications](#game-feature-modifications)
    - [BSA Invalidation](#bsa-invalidation)
    - [Data Archives](#data-archives)
    - [Mod Data Checker](#mod-data-checker)
    - [Mod Data Content](#mod-data-content)
    - [Save Game Handling](#save-game-handling)
    - [Script Extender Support](#script-extender-support)
  - [Potential Challenges](#potential-challenges)
  - [Testing Strategy](#testing-strategy)
  - [Implementation Checklist](#implementation-checklist)

## Introduction

Oblivion Remastered is a remastered version of The Elder Scrolls IV: Oblivion that uses the original Oblivion data files (.esm/.esp) and archives (.bsa). Creating a plugin for Oblivion Remastered involves forking the existing Oblivion plugin and making the necessary modifications to support the remastered version.

The key differences between Oblivion and Oblivion Remastered that may affect the plugin implementation include:

1. Different installation paths and registry entries
2. Potentially different executable names and versions
3. Potentially different save game formats
4. Potentially different INI file structures or settings
5. Potentially different BSA handling
6. Potentially different script extender requirements

This document provides recommendations for adapting the Oblivion plugin to work with Oblivion Remastered, focusing on the areas that are most likely to need changes.

## Project Setup

To create a plugin for Oblivion Remastered, follow these steps:

1. Fork the existing Oblivion plugin repository
2. Rename the project and files to reflect Oblivion Remastered
3. Update the CMakeLists.txt files to build the new plugin
4. Modify the source code as outlined in the following sections

Here's a suggested directory structure for the new plugin:

```
modorganizer-game_oblivionremastered/
├── CMakeLists.txt
└── src/
    ├── CMakeLists.txt
    ├── gameoblivionremastered.cpp
    ├── gameoblivionremastered.h
    ├── gameoblivionremastered.json
    ├── oblivionremasteredbsainvalidation.cpp
    ├── oblivionremasteredbsainvalidation.h
    ├── oblivionremastereddataarchives.cpp
    ├── oblivionremastereddataarchives.h
    ├── oblivionremasteredmoddatachecker.cpp
    ├── oblivionremasteredmoddatachecker.h
    ├── oblivionremasteredmoddatacontent.h
    ├── oblivionremasteredsavegame.cpp
    ├── oblivionremasteredsavegame.h
    ├── oblivionremasteredscriptextender.cpp
    └── oblivionremasteredscriptextender.h
```

## Core Class Modifications

### GameOblivionRemastered

The main class of the plugin should be renamed from `GameOblivion` to `GameOblivionRemastered`. This class will need several modifications:

1. **Plugin Metadata**: Update the plugin metadata to reflect Oblivion Remastered
   ```cpp
   Q_PLUGIN_METADATA(IID "org.yourusername.GameOblivionRemastered" FILE "gameoblivionremastered.json")
   ```

2. **Game Name and Display Name**: Update the game name and display name
   ```cpp
   QString GameOblivionRemastered::gameName() const
   {
     return "Oblivion Remastered";
   }
   
   QString GameOblivionRemastered::localizedName() const
   {
     return tr("Oblivion Remastered Support Plugin");
   }
   ```

3. **Game Path Detection**: Update the method to detect the game installation path
   ```cpp
   QString GameOblivionRemastered::identifyGamePath() const
   {
     // Try to find the game in the registry
     QString path = "Software\\Bethesda Softworks\\Oblivion Remastered";
     QString result = findInRegistry(HKEY_LOCAL_MACHINE, path.toStdWString().c_str(), L"Installed Path");
     if (!result.isEmpty()) {
       return result;
     }
     
     // Try to find the game in Steam
     result = parseSteamLocation("STEAM_APP_ID_HERE", "Oblivion Remastered");
     if (!result.isEmpty()) {
       return result;
     }
     
     // Try to find the game in Epic Games
     result = parseEpicGamesLocation({"OblivionRemastered"});
     if (!result.isEmpty()) {
       return result;
     }
     
     return "";
   }
   ```

4. **Executables**: Update the list of executables
   ```cpp
   QList<ExecutableInfo> GameOblivionRemastered::executables() const
   {
     return QList<ExecutableInfo>()
            << ExecutableInfo("Oblivion Remastered", findInGameFolder(binaryName()))
            << ExecutableInfo("Oblivion Remastered Launcher", findInGameFolder(getLauncherName()))
            << ExecutableInfo("LOOT", QFileInfo(getLootPath()))
                   .withArgument("--game=\"Oblivion\"");
   }
   ```

5. **Binary Name**: Update the binary name if it's different
   ```cpp
   QString GameOblivionRemastered::binaryName() const
   {
     return "OblivionRemastered.exe"; // Replace with actual binary name
   }
   
   QString GameOblivionRemastered::getLauncherName() const
   {
     return "OblivionRemasteredLauncher.exe"; // Replace with actual launcher name
   }
   ```

6. **Steam App ID**: Update the Steam App ID
   ```cpp
   QString GameOblivionRemastered::steamAPPId() const
   {
     return "STEAM_APP_ID_HERE"; // Replace with actual Steam App ID
   }
   ```

7. **Game Short Name**: Update the game short name
   ```cpp
   QString GameOblivionRemastered::gameShortName() const
   {
     return "OblivionRemastered";
   }
   
   QStringList GameOblivionRemastered::validShortNames() const
   {
     return { "OblivionRemastered", "Oblivion" };
   }
   ```

8. **Nexus Name**: Update the Nexus name if different
   ```cpp
   QString GameOblivionRemastered::gameNexusName() const
   {
     return "OblivionRemastered"; // Or "Oblivion" if it uses the same Nexus site
   }
   ```

9. **INI Files**: Update the INI files if they have different names
   ```cpp
   QStringList GameOblivionRemastered::iniFiles() const
   {
     return { "OblivionRemastered.ini", "OblivionRemasteredPrefs.ini" };
   }
   ```

10. **Feature Registration**: Update the feature registration to use the Oblivion Remastered-specific implementations
    ```cpp
    bool GameOblivionRemastered::init(IOrganizer* moInfo)
    {
      if (!GameGamebryo::init(moInfo)) {
        return false;
      }
    
      auto dataArchives = std::make_shared<OblivionRemasteredDataArchives>(this);
      registerFeature(std::make_shared<OblivionRemasteredScriptExtender>(this));
      registerFeature(dataArchives);
      registerFeature(std::make_shared<OblivionRemasteredBSAInvalidation>(dataArchives.get(), this));
      registerFeature(std::make_shared<GamebryoSaveGameInfo>(this));
      registerFeature(std::make_shared<GamebryoLocalSaveGames>(this, "OblivionRemastered.ini"));
      registerFeature(std::make_shared<OblivionRemasteredModDataChecker>(this));
      registerFeature(std::make_shared<OblivionRemasteredModDataContent>(m_Organizer->gameFeatures()));
      registerFeature(std::make_shared<GamebryoGamePlugins>(moInfo));
      registerFeature(std::make_shared<GamebryoUnmanagedMods>(this));
      return true;
    }
    ```

## Game Feature Modifications

### BSA Invalidation

The BSA invalidation feature may need to be updated if Oblivion Remastered handles BSA files differently:

1. **BSA Name**: Update the invalidation BSA name if needed
   ```cpp
   QString OblivionRemasteredBSAInvalidation::invalidationBSAName() const
   {
     return "OblivionRemastered - Invalidation.bsa";
   }
   ```

2. **BSA Version**: Update the BSA version if needed
   ```cpp
   unsigned long OblivionRemasteredBSAInvalidation::bsaVersion() const
   {
     return 0x67; // Or a different version if Oblivion Remastered uses a different BSA format
   }
   ```

### Data Archives

The data archives feature may need to be updated if Oblivion Remastered uses different BSA files or handles them differently:

1. **Vanilla Archives**: Update the list of vanilla BSA archives
   ```cpp
   QStringList OblivionRemasteredDataArchives::vanillaArchives() const
   {
     return { "OblivionRemastered - Misc.bsa",    "OblivionRemastered - Textures - Compressed.bsa",
              "OblivionRemastered - Meshes.bsa",  "OblivionRemastered - Sounds.bsa",
              "OblivionRemastered - Voices1.bsa", "OblivionRemastered - Voices2.bsa" };
   }
   ```

2. **Archive List**: Update the method to get the list of archives from the INI file
   ```cpp
   QStringList OblivionRemasteredDataArchives::archives(const MOBase::IProfile* profile) const
   {
     QStringList result;
   
     QString iniFile = profile->localSettingsEnabled()
                           ? QDir(profile->absolutePath()).absoluteFilePath("OblivionRemastered.ini")
                           : localGameDirectory().absoluteFilePath("OblivionRemastered.ini");
     result.append(getArchivesFromKey(iniFile, "SArchiveList"));
   
     return result;
   }
   ```

3. **Archive List Writing**: Update the method to write the list of archives to the INI file
   ```cpp
   void OblivionRemasteredDataArchives::writeArchiveList(MOBase::IProfile* profile,
                                               const QStringList& before)
   {
     QString list = before.join(", ");
   
     QString iniFile = profile->localSettingsEnabled()
                           ? QDir(profile->absolutePath()).absoluteFilePath("OblivionRemastered.ini")
                           : localGameDirectory().absoluteFilePath("OblivionRemastered.ini");
     setArchivesToKey(iniFile, "SArchiveList", list);
   }
   ```

### Mod Data Checker

The mod data checker feature may need to be updated if Oblivion Remastered supports different mod folder structures:

1. **Possible Folder Names**: Update the list of possible folder names
   ```cpp
   virtual const FileNameSet& possibleFolderNames() const override
   {
     static FileNameSet result{"fonts",      "interface",     "menus",
                               "meshes",     "music",         "scripts",
                               "shaders",    "sound",         "strings",
                               "textures",   "trees",         "video",
                               "facegen",    "obse",          "distantlod",
                               "asi",        "distantland",   "mits",
                               "dllplugins", "CalienteTools", "NetScriptFramework",
                               "remastered"}; // Add any Oblivion Remastered specific folders
     return result;
   }
   ```

2. **Possible File Extensions**: Update the list of possible file extensions
   ```cpp
   virtual const FileNameSet& possibleFileExtensions() const override
   {
     static FileNameSet result{"esp", "esm", "bsa", "modgroups", "ini", "json"}; // Add any Oblivion Remastered specific extensions
     return result;
   }
   ```

### Mod Data Content

The mod data content feature may need to be updated if Oblivion Remastered supports different mod content types:

```cpp
OblivionRemasteredModDataContent::OblivionRemasteredModDataContent(const MOBase::IGameFeatures* gameFeatures)
    : GamebryoModDataContent(gameFeatures)
{
  // Disable content types that are not applicable to Oblivion Remastered
  m_Enabled[CONTENT_MCM]     = false;
  m_Enabled[CONTENT_SKYPROC] = false;
  
  // Enable content types that are specific to Oblivion Remastered
  // m_Enabled[CONTENT_REMASTERED] = true;
}
```

### Save Game Handling

The save game handling feature may need to be updated if Oblivion Remastered uses a different save game format:

1. **Save Game Extension**: Update the save game extension if needed
   ```cpp
   QString GameOblivionRemastered::savegameExtension() const
   {
     return "esr"; // Or "ess" if it uses the same format as Oblivion
   }
   
   QString GameOblivionRemastered::savegameSEExtension() const
   {
     return "obser"; // Or "obse" if it uses the same format as Oblivion
   }
   ```

2. **Save Game Format**: Update the save game format handling if needed
   ```cpp
   OblivionRemasteredSaveGame::OblivionRemasteredSaveGame(QString const& fileName, GameOblivionRemastered const* game)
       : GamebryoSaveGame(fileName, game)
   {
     FileWrapper file(getFilepath(), "TES4RSAVEGAME"); // Or "TES4SAVEGAME" if it uses the same format as Oblivion
     file.setPluginString(GamebryoSaveGame::StringType::TYPE_BSTRING);
   
     SYSTEMTIME creationTime;
     fetchInformationFields(file, m_SaveNumber, m_PCName, m_PCLevel, m_PCLocation,
                            creationTime);
     setCreationTime(creationTime);
   }
   ```

### Script Extender Support

The script extender support feature may need to be updated if Oblivion Remastered uses a different script extender:

1. **Binary Name**: Update the script extender binary name
   ```cpp
   QString OblivionRemasteredScriptExtender::BinaryName() const
   {
     return "obser_loader.exe"; // Or "obse_loader.exe" if it uses the same script extender as Oblivion
   }
   ```

2. **Plugin Path**: Update the script extender plugin path
   ```cpp
   QString OblivionRemasteredScriptExtender::PluginPath() const
   {
     return "obser/plugins"; // Or "obse/plugins" if it uses the same script extender as Oblivion
   }
   ```

## Potential Challenges

When creating a plugin for Oblivion Remastered, you may encounter the following challenges:

1. **Game Detection**: Oblivion Remastered may use different registry entries or installation paths than Oblivion. You'll need to update the `identifyGamePath` method to correctly detect the game.

2. **Save Game Format**: Oblivion Remastered may use a different save game format than Oblivion. You'll need to update the `OblivionRemasteredSaveGame` class to handle the new format.

3. **BSA Handling**: Oblivion Remastered may handle BSA files differently than Oblivion. You'll need to update the `OblivionRemasteredBSAInvalidation` and `OblivionRemasteredDataArchives` classes to handle the new BSA format.

4. **Script Extender**: Oblivion Remastered may use a different script extender than Oblivion. You'll need to update the `OblivionRemasteredScriptExtender` class to handle the new script extender.

5. **INI Settings**: Oblivion Remastered may use different INI settings than Oblivion. You'll need to update the `initializeProfile` method to handle the new INI settings.

6. **Mod Compatibility**: Some mods designed for Oblivion may not work with Oblivion Remastered. You'll need to update the `OblivionRemasteredModDataChecker` class to handle this.

## Testing Strategy

To ensure that your Oblivion Remastered plugin works correctly, follow this testing strategy:

1. **Game Detection**: Test that the plugin correctly detects the Oblivion Remastered installation.

2. **Profile Initialization**: Test that the plugin correctly initializes a profile for Oblivion Remastered.

3. **Mod Installation**: Test that the plugin correctly installs mods for Oblivion Remastered.

4. **Plugin Management**: Test that the plugin correctly manages plugins (ESPs, ESMs) for Oblivion Remastered.

5. **BSA Handling**: Test that the plugin correctly handles BSA files for Oblivion Remastered.

6. **Save Game Handling**: Test that the plugin correctly handles save games for Oblivion Remastered.

7. **Script Extender Support**: Test that the plugin correctly supports the script extender for Oblivion Remastered.

## Implementation Checklist

Use this checklist to ensure that you've made all the necessary changes to adapt the Oblivion plugin for Oblivion Remastered:

- [ ] Fork the Oblivion plugin repository
- [ ] Rename the project and files to reflect Oblivion Remastered
- [ ] Update the CMakeLists.txt files
- [ ] Update the plugin metadata
- [ ] Update the game name and display name
- [ ] Update the game path detection
- [ ] Update the list of executables
- [ ] Update the binary name and launcher name
- [ ] Update the Steam App ID
- [ ] Update the game short name and valid short names
- [ ] Update the Nexus name
- [ ] Update the INI files
- [ ] Update the feature registration
- [ ] Update the BSA invalidation feature
- [ ] Update the data archives feature
- [ ] Update the mod data checker feature
- [ ] Update the mod data content feature
- [ ] Update the save game handling feature
- [ ] Update the script extender support feature
- [ ] Test the plugin with Oblivion Remastered
