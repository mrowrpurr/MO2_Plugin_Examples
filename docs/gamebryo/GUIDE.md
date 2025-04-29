# Mod Organizer 2 Gamebryo Plugin Development Guide

This guide provides practical recommendations and example code snippets for developing game plugins for Gamebryo and Creation Engine based games in Mod Organizer 2. It complements the documentation and diagrams with concrete advice to help you get started.

## Table of Contents

- [Mod Organizer 2 Gamebryo Plugin Development Guide](#mod-organizer-2-gamebryo-plugin-development-guide)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Setting Up Your Development Environment](#setting-up-your-development-environment)
    - [Basic Game Plugin Structure](#basic-game-plugin-structure)
  - [Implementing Game Features](#implementing-game-features)
    - [BSA Invalidation](#bsa-invalidation)
    - [Data Archives](#data-archives)
    - [Game Plugins](#game-plugins)
    - [Local Save Games](#local-save-games)
    - [Mod Data Checker](#mod-data-checker)
    - [Mod Data Content](#mod-data-content)
    - [Save Game Info](#save-game-info)
    - [Script Extender](#script-extender)
    - [Unmanaged Mods](#unmanaged-mods)
  - [Common Tasks](#common-tasks)
    - [Detecting the Game Installation](#detecting-the-game-installation)
    - [Handling Game Variants](#handling-game-variants)
    - [Working with INI Files](#working-with-ini-files)
    - [Working with Registry](#working-with-registry)
    - [Working with Steam](#working-with-steam)
    - [Working with Epic Games](#working-with-epic-games)
  - [Best Practices](#best-practices)
    - [Error Handling](#error-handling)
    - [Performance Considerations](#performance-considerations)
    - [Compatibility with Other Plugins](#compatibility-with-other-plugins)

## Getting Started

### Setting Up Your Development Environment

To develop game plugins for Mod Organizer 2, you'll need:

1. **C++ Development Environment**: Visual Studio (recommended for Windows) with C++17 support
2. **Qt Development Kit**: Qt 5.15 or compatible version
3. **Mod Organizer 2 Source Code**: For reference and headers

You can set up your project to build against the Mod Organizer 2 libraries:

```cmake
# Example CMakeLists.txt for a MO2 game plugin
cmake_minimum_required(VERSION 3.16)
project(MyGamePlugin)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt
find_package(Qt5 COMPONENTS Widgets REQUIRED)

# Set paths to MO2 includes and libraries
set(MO2_INCLUDE_DIR "path/to/modorganizer/include")
set(MO2_LIB_DIR "path/to/modorganizer/lib")

# Add source files
set(SOURCES
    src/main.cpp
    src/mygameplugin.cpp
    src/mygameplugin.h
    src/mygamebsainvalidation.cpp
    src/mygamebsainvalidation.h
    src/mygamedataarchives.cpp
    src/mygamedataarchives.h
    src/mygamegameplugins.cpp
    src/mygamegameplugins.h
    src/mygamelocalsavegames.cpp
    src/mygamelocalsavegames.h
    src/mygamemoddatachecker.cpp
    src/mygamemoddatachecker.h
    src/mygamemoddatacontent.cpp
    src/mygamemoddatacontent.h
    src/mygamesavegame.cpp
    src/mygamesavegame.h
    src/mygamesavegameinfo.cpp
    src/mygamesavegameinfo.h
    src/mygamescriptextender.cpp
    src/mygamescriptextender.h
    src/mygameunmanagedmods.cpp
    src/mygameunmanagedmods.h
)

# Create shared library
add_library(${PROJECT_NAME} SHARED ${SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    ${MO2_INCLUDE_DIR}
)

# Link libraries
target_link_libraries(${PROJECT_NAME}
    Qt5::Widgets
    ${MO2_LIB_DIR}/uibase.lib
    ${MO2_LIB_DIR}/game_gamebryo.lib
)

# Set output directory
set_target_properties(${PROJECT_NAME} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin"
)
```

### Basic Game Plugin Structure

All game plugins must inherit from `GameGamebryo` and implement the required methods. Here's a basic template for a game plugin:

```cpp
#include <gamegamebryo.h>
#include <imoinfo.h>

class MyGamePlugin : public GameGamebryo
{
    Q_OBJECT
    Q_INTERFACES(MOBase::IPlugin MOBase::IPluginGame)
    Q_PLUGIN_METADATA(IID "org.example.MyGamePlugin" FILE "mygameplugin.json")

public:
    MyGamePlugin();

    // IPluginGame interface
    virtual QString gameName() const override;
    virtual QString gameShortName() const override;
    virtual QString gameNexusName() const override;
    virtual QStringList validShortNames() const override;
    virtual QString gameVersion() const override;
    virtual QString getLauncherName() const override;
    virtual QStringList primaryPlugins() const override;
    virtual QStringList gameVariants() const override;
    virtual QStringList iniFiles() const override;
    virtual QStringList DLCPlugins() const override;
    virtual QStringList CCPlugins() const override;
    virtual int nexusModOrganizerID() const override;
    virtual int nexusGameID() const override;

protected:
    // GameGamebryo interface
    virtual QString savegameExtension() const override;
    virtual QString savegameSEExtension() const override;
    virtual std::shared_ptr<const GamebryoSaveGame> makeSaveGame(QString filepath) const override;
    virtual QString identifyGamePath() const override;
};

MyGamePlugin::MyGamePlugin()
{
}

QString MyGamePlugin::gameName() const
{
    return "My Game";
}

QString MyGamePlugin::gameShortName() const
{
    return "mygame";
}

QString MyGamePlugin::gameNexusName() const
{
    return "mygame";
}

QStringList MyGamePlugin::validShortNames() const
{
    return { "mygame" };
}

QString MyGamePlugin::gameVersion() const
{
    return GameGamebryo::gameVersion();
}

QString MyGamePlugin::getLauncherName() const
{
    return "MyGameLauncher.exe";
}

QStringList MyGamePlugin::primaryPlugins() const
{
    return { "MyGame.esm" };
}

QStringList MyGamePlugin::gameVariants() const
{
    return { "Regular", "Special Edition" };
}

QStringList MyGamePlugin::iniFiles() const
{
    return { "MyGame.ini", "MyGamePrefs.ini" };
}

QStringList MyGamePlugin::DLCPlugins() const
{
    return { "DLC01.esm", "DLC02.esm" };
}

QStringList MyGamePlugin::CCPlugins() const
{
    return {};
}

int MyGamePlugin::nexusModOrganizerID() const
{
    return 1234; // Replace with actual Nexus Mod Organizer ID
}

int MyGamePlugin::nexusGameID() const
{
    return 5678; // Replace with actual Nexus Game ID
}

QString MyGamePlugin::savegameExtension() const
{
    return "sav";
}

QString MyGamePlugin::savegameSEExtension() const
{
    return "skse";
}

std::shared_ptr<const GamebryoSaveGame> MyGamePlugin::makeSaveGame(QString filepath) const
{
    return std::make_shared<MyGameSaveGame>(filepath, this);
}

QString MyGamePlugin::identifyGamePath() const
{
    // Try to find the game in the registry
    QString path = "Software\\Bethesda Softworks\\MyGame";
    return findInRegistry(HKEY_LOCAL_MACHINE, path.toStdWString().c_str(), L"Installed Path");
}
```

You'll also need a JSON file (`mygameplugin.json`) with the following content:

```json
{
    "name": "My Game Plugin",
    "author": "Your Name",
    "version": "1.0.0",
    "description": "Support for My Game"
}
```

## Implementing Game Features

### BSA Invalidation

BSA invalidation is a technique used to make the game load loose files instead of BSA archives. Here's an example implementation:

```cpp
#include <gamebryobsainvalidation.h>

class MyGameBSAInvalidation : public GamebryoBSAInvalidation
{
public:
    MyGameBSAInvalidation(MOBase::DataArchives* dataArchives, const QString& iniFilename, MOBase::IPluginGame const* game)
        : GamebryoBSAInvalidation(dataArchives, iniFilename, game)
    {
    }

protected:
    virtual QString invalidationBSAName() const override
    {
        return "MyGame - Invalidation.bsa";
    }

    virtual unsigned long bsaVersion() const override
    {
        return 0x68; // 0x67 for Oblivion, 0x68 for everything else
    }
};
```

### Data Archives

Data archives handle the management of BSA files. Here's an example implementation:

```cpp
#include <gamebryodataarchives.h>

class MyGameDataArchives : public GamebryoDataArchives
{
public:
    MyGameDataArchives(const GameGamebryo* game)
        : GamebryoDataArchives(game)
    {
    }

    virtual QStringList vanillaArchives() const override
    {
        return { "MyGame - Main.bsa", "MyGame - Textures.bsa" };
    }

    virtual QStringList archives(const MOBase::IProfile* profile) const override
    {
        QStringList result;

        QString iniFile = profile->localSettingsEnabled()
            ? profile->absolutePath() + "/MyGame.ini"
            : m_Game->documentsDirectory().absolutePath() + "/MyGame.ini";

        result.append(getArchivesFromKey(iniFile, "SArchiveList"));

        return result;
    }

protected:
    virtual void writeArchiveList(MOBase::IProfile* profile, const QStringList& before) override
    {
        QString iniFile = profile->localSettingsEnabled()
            ? profile->absolutePath() + "/MyGame.ini"
            : m_Game->documentsDirectory().absolutePath() + "/MyGame.ini";

        QString list = before.join(", ");
        setArchivesToKey(iniFile, "SArchiveList", list);
    }
};
```

### Game Plugins

Game plugins handle the management of ESP, ESM, and ESL files. For Gamebryo games, you can use `GamebryoGamePlugins`:

```cpp
#include <gamebryogameplugins.h>

class MyGameGamePlugins : public GamebryoGamePlugins
{
public:
    MyGameGamePlugins(MOBase::IOrganizer* organizer)
        : GamebryoGamePlugins(organizer)
    {
    }
};
```

For Creation Engine games, you can use `CreationGamePlugins`:

```cpp
#include <creationgameplugins.h>

class MyGameGamePlugins : public CreationGamePlugins
{
public:
    MyGameGamePlugins(MOBase::IOrganizer* organizer)
        : CreationGamePlugins(organizer)
    {
    }
};
```

### Local Save Games

Local save games handle the management of save game files. Here's an example implementation:

```cpp
#include <gamebryolocalsavegames.h>

class MyGameLocalSaveGames : public GamebryoLocalSaveGames
{
public:
    MyGameLocalSaveGames(const GameGamebryo* game)
        : GamebryoLocalSaveGames(game)
    {
    }
};
```

### Mod Data Checker

Mod data checker checks if mod data is valid for the game. Here's an example implementation:

```cpp
#include <gamebryomoddatachecker.h>

class MyGameModDataChecker : public GamebryoModDataChecker
{
public:
    MyGameModDataChecker(const GameGamebryo* game)
        : GamebryoModDataChecker(game)
    {
    }
};
```

### Mod Data Content

Mod data content determines the content of mods. Here's an example implementation:

```cpp
#include <gamebryomoddatacontent.h>

class MyGameModDataContent : public GamebryoModDataContent
{
public:
    MyGameModDataContent(const GameGamebryo* game)
        : GamebryoModDataContent(game)
    {
    }

    virtual std::vector<Content> getAllContents() const override
    {
        return {
            Content(1, "Meshes", ":/MO/gui/content/mesh"),
            Content(2, "Textures", ":/MO/gui/content/texture"),
            Content(3, "Scripts", ":/MO/gui/content/script"),
            Content(4, "Sounds", ":/MO/gui/content/sound"),
            Content(5, "Music", ":/MO/gui/content/music"),
            Content(6, "Interface", ":/MO/gui/content/interface"),
            Content(7, "Plugins", ":/MO/gui/content/plugin")
        };
    }
};
```

### Save Game Info

Save game info provides information about save games. Here's an example implementation:

```cpp
#include <gamebryosavegameinfo.h>

class MyGameSaveGameInfo : public GamebryoSaveGameInfo
{
public:
    MyGameSaveGameInfo(GameGamebryo const* game)
        : GamebryoSaveGameInfo(game)
    {
    }

    virtual MOBase::ISaveGameInfoWidget* getSaveGameWidget(QWidget* parent = 0) const override
    {
        return new GamebryoSaveGameInfoWidget(this, parent);
    }
};
```

### Script Extender

Script extender handles script extenders like SKSE, OBSE, etc. Here's an example implementation:

```cpp
#include <gamebryoscriptextender.h>

class MyGameScriptExtender : public GamebryoScriptExtender
{
public:
    MyGameScriptExtender(GameGamebryo const* game)
        : GamebryoScriptExtender(game)
    {
    }

    virtual QString BinaryName() const override
    {
        return "mgse_loader.exe";
    }

    virtual QString PluginPath() const override
    {
        return "mgse/plugins";
    }

    virtual QString loaderName() const override
    {
        return "mgse_loader.exe";
    }

    virtual QString savegameExtension() const override
    {
        return "mgse";
    }

    virtual bool isInstalled() const override
    {
        return fileExists(loaderPath());
    }
};
```

### Unmanaged Mods

Unmanaged mods handle mods that are not managed by Mod Organizer 2, like DLCs. Here's an example implementation:

```cpp
#include <gamebryounmanagedmods.h>

class MyGameUnmanagedMods : public GamebryoUnmanagedMods
{
public:
    MyGameUnmanagedMods(const GameGamebryo* game)
        : GamebryoUnmanagedMods(game)
    {
    }

    virtual QStringList mods(bool onlyOfficial) const override
    {
        QStringList result;
        QDir dataDir(game()->dataDirectory());
        
        for (const QString& fileName : dataDir.entryList(QStringList() << "DLC*.esm", QDir::Files)) {
            result.append(fileName);
        }
        
        return result;
    }

    virtual QString displayName(const QString& modName) const override
    {
        if (modName == "DLC01.esm") {
            return "DLC 1: The First DLC";
        } else if (modName == "DLC02.esm") {
            return "DLC 2: The Second DLC";
        } else {
            return modName;
        }
    }

    virtual QFileInfo referenceFile(const QString& modName) const override
    {
        return QFileInfo(game()->dataDirectory().absoluteFilePath(modName));
    }

    virtual QStringList secondaryFiles(const QString& modName) const override
    {
        if (modName == "DLC01.esm") {
            return { "DLC01 - Main.bsa" };
        } else if (modName == "DLC02.esm") {
            return { "DLC02 - Main.bsa" };
        } else {
            return {};
        }
    }
};
```

## Common Tasks

### Detecting the Game Installation

The `identifyGamePath()` method is used to detect the game installation. Here are some common approaches:

```cpp
QString MyGamePlugin::identifyGamePath() const
{
    // Try to find the game in the registry
    QString path = "Software\\Bethesda Softworks\\MyGame";
    QString result = findInRegistry(HKEY_LOCAL_MACHINE, path.toStdWString().c_str(), L"Installed Path");
    if (!result.isEmpty()) {
        return result;
    }

    // Try to find the game in Steam
    result = parseSteamLocation("12345", "My Game");
    if (!result.isEmpty()) {
        return result;
    }

    // Try to find the game in Epic Games
    result = parseEpicGamesLocation({"MyGame"});
    if (!result.isEmpty()) {
        return result;
    }

    return "";
}
```

### Handling Game Variants

Some games have multiple variants, like regular and special editions. Here's how to handle them:

```cpp
QStringList MyGamePlugin::gameVariants() const
{
    return { "Regular", "Special Edition" };
}

void MyGamePlugin::setGameVariant(const QString& variant)
{
    m_GameVariant = variant;
}

QString MyGamePlugin::gameVersion() const
{
    if (m_GameVariant == "Special Edition") {
        // Special Edition specific version detection
        return "2.0.0";
    } else {
        // Regular version detection
        return GameGamebryo::gameVersion();
    }
}
```

### Working with INI Files

Gamebryo games use INI files for configuration. Here's how to work with them:

```cpp
bool MyGamePlugin::prepareIni(const QString& exec)
{
    MOBase::IProfile* profile = m_Organizer->profile();

    QString basePath = profile->localSettingsEnabled()
        ? profile->absolutePath()
        : documentsDirectory().absolutePath();

    if (!iniFiles().isEmpty()) {
        QString profileIni = basePath + "/" + iniFiles()[0];

        WCHAR setting[512];
        if (!GetPrivateProfileStringW(L"General", L"bEnableFileSelection", L"0", setting,
                                    512, profileIni.toStdWString().c_str()) ||
            wcstol(setting, nullptr, 10) != 1) {
            MOBase::WriteRegistryValue(L"General", L"bEnableFileSelection", L"1",
                                    profileIni.toStdWString().c_str());
        }
    }

    return true;
}
```

### Working with Registry

Gamebryo games often store information in the Windows registry. Here's how to work with it:

```cpp
QString findInRegistry(HKEY baseKey, LPCWSTR path, LPCWSTR value)
{
    DWORD size = 0;
    HKEY subKey;
    LONG res = ::RegOpenKeyExW(baseKey, path, 0, KEY_QUERY_VALUE | KEY_WOW64_32KEY, &subKey);
    if (res != ERROR_SUCCESS) {
        res = ::RegOpenKeyExW(baseKey, path, 0, KEY_QUERY_VALUE | KEY_WOW64_64KEY, &subKey);
        if (res != ERROR_SUCCESS)
            return QString();
    }
    res = ::RegGetValueW(subKey, L"", value, RRF_RT_REG_SZ | RRF_NOEXPAND, nullptr, nullptr, &size);
    if (res != ERROR_SUCCESS && res != ERROR_MORE_DATA) {
        return QString();
    }

    std::unique_ptr<BYTE[]> buffer(new BYTE[size]);
    res = ::RegGetValueW(subKey, L"", value, RRF_RT_REG_SZ | RRF_NOEXPAND, nullptr, buffer.get(), &size);
    if (res != ERROR_SUCCESS) {
        return QString();
    }

    return QString::fromUtf16(reinterpret_cast<const ushort*>(buffer.get()));
}
```

### Working with Steam

Gamebryo games are often distributed through Steam. Here's how to find a game in Steam:

```cpp
QString parseSteamLocation(const QString& appid, const QString& directoryName)
{
    QString path = "Software\\Valve\\Steam";
    QString steamLocation = findInRegistry(HKEY_CURRENT_USER, path.toStdWString().c_str(), L"SteamPath");
    if (!steamLocation.isEmpty()) {
        QString steamLibraryLocation;
        QString steamLibraries(steamLocation + "\\" + "config" + "\\" + "libraryfolders.vdf");
        if (QFile(steamLibraries).exists()) {
            std::ifstream file(steamLibraries.toStdString());
            auto root = tyti::vdf::read(file);
            for (auto child : root.childs) {
                tyti::vdf::object* library = child.second.get();
                auto apps = library->childs["apps"];
                if (apps->attribs.contains(appid.toStdString())) {
                    steamLibraryLocation = QString::fromStdString(library->attribs["path"]);
                    break;
                }
            }
        }
        if (!steamLibraryLocation.isEmpty()) {
            QString gameLocation = steamLibraryLocation + "\\" + "steamapps" + "\\" + "common" + "\\" + directoryName;
            if (QDir(gameLocation).exists())
                return gameLocation;
        }
    }
    return "";
}
```

### Working with Epic Games

Gamebryo games are also distributed through Epic Games. Here's how to find a game in Epic Games:

```cpp
QString parseEpicGamesLocation(const QStringList& manifests)
{
    // Use the registry entry to find the EGL Data dir first, just in case something changes
    QString manifestDir = findInRegistry(HKEY_LOCAL_MACHINE, L"Software\\Epic Games\\EpicGamesLauncher", L"AppDataPath");
    if (manifestDir.isEmpty())
        manifestDir = getKnownFolderPath(FOLDERID_ProgramData, false) + "\\Epic\\EpicGamesLauncher\\Data\\";
    manifestDir += "Manifests";
    QDir epicManifests(manifestDir, "*.item", QDir::SortFlags(QDir::Name | QDir::IgnoreCase), QDir::Files);
    if (epicManifests.exists()) {
        QDirIterator it(epicManifests);
        while (it.hasNext()) {
            QString manifestFile = it.next();
            QFile manifest(manifestFile);

            if (!manifest.open(QIODevice::ReadOnly)) {
                qWarning("Couldn't open Epic Games manifest file.");
                continue;
            }

            QByteArray manifestData = manifest.readAll();

            QJsonDocument manifestJson(QJsonDocument::fromJson(manifestData));

            if (manifests.contains(manifestJson["AppName"].toString())) {
                return manifestJson["InstallLocation"].toString();
            }
        }
    }
    return "";
}
```

## Best Practices

### Error Handling

Always check for null pointers and handle errors gracefully:

```cpp
bool MyGamePlugin::init(MOBase::IOrganizer* moInfo)
{
    if (!GameGamebryo::init(moInfo)) {
        return false;
    }

    // Register game features
    try {
        registerFeature<BSAInvalidation>(new MyGameBSAInvalidation(this, "MyGame.ini"));
        registerFeature<DataArchives>(new MyGameDataArchives(this));
        registerFeature<GamePlugins>(new MyGameGamePlugins(moInfo));
        registerFeature<LocalSavegames>(new MyGameLocalSaveGames(this));
        registerFeature<ModDataChecker>(new MyGameModDataChecker(this));
        registerFeature<ModDataContent>(new MyGameModDataContent(this));
        registerFeature<SaveGameInfo>(new MyGameSaveGameInfo(this));
        registerFeature<ScriptExtender>(new MyGameScriptExtender(this));
        registerFeature<UnmanagedMods>(new MyGameUnmanagedMods(this));
    } catch (const std::exception& e) {
        qCritical("Failed to register game features: %s", e.what());
        return false;
    }

    return true;
}
```

### Performance Considerations

Some operations, like reading from the registry or parsing VDF files, can be slow. Consider caching results:

```cpp
QString MyGamePlugin::gameVersion() const
{
    if (m_GameVersion.isEmpty()) {
        m_GameVersion = GameGamebryo::gameVersion();
    }
    return m_GameVersion;
}
```

### Compatibility with Other Plugins

Make sure your plugin is compatible with other plugins by following these guidelines:

1. Use the `registerFeature()` method to register game features, so they can be overridden by other plugins
2. Use the `m_Organizer->pluginSetting()` method to get plugin settings, so they can be configured by the user
3. Use the `m_Organizer->persistent()` method to store persistent data, so it can be shared with other plugins
4. Use the `m_Organizer->modList()` and `m_Organizer->pluginList()` methods to get mod and plugin lists, so they can be modified by other plugins
