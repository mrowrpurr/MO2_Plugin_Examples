# Basic Games Plugin Diagrams

This document provides visual diagrams of the architecture and relationships of the Basic Games plugin for Mod Organizer 2.

## Table of Contents

- [Basic Games Plugin Diagrams](#basic-games-plugin-diagrams)
  - [Table of Contents](#table-of-contents)
  - [Plugin Architecture](#plugin-architecture)
  - [Component Relationships](#component-relationships)
  - [Plugin Inheritance](#plugin-inheritance)
  - [Game Detection Process](#game-detection-process)
  - [Game Initialization Process](#game-initialization-process)
  - [Save Game Handling](#save-game-handling)
  - [Game Implementation](#game-implementation)
  - [Plugin Registration](#plugin-registration)

## Plugin Architecture

The following diagram shows the overall architecture of the Basic Games plugin:

```mermaid
flowchart TD
    subgraph MO2[Mod Organizer 2]
        IOrganizer
        PluginSystem
    end
    
    subgraph BasicGames[Basic Games Plugin]
        BasicGame
        BasicGameMapping
        BasicGameOptionsMapping
        BasicGameMappings
        BasicIniGame
    end
    
    subgraph GameFeatures[Game Features]
        BasicGameSaveGameInfo
        BasicGameSaveGame
    end
    
    subgraph GameImplementations[Game Implementations]
        PythonGames[Python Games]
        IniGames[INI Games]
    end
    
    subgraph GameDetection[Game Detection]
        SteamGames[Steam Games]
        GOGGames[GOG Games]
        OriginGames[Origin Games]
        EpicGames[Epic Games]
        EADesktopGames[EA Desktop Games]
    end
    
    MO2 --> BasicGames
    BasicGames --> GameFeatures
    BasicGames --> GameImplementations
    BasicGames --> GameDetection
    GameImplementations --> MO2
```

## Component Relationships

The following diagram shows the relationships between the components of the Basic Games plugin:

```mermaid
classDiagram
    class BasicGame {
        -string _fromName
        -IOrganizer _organizer
        -string _gamePath
        -BasicGameMappings _mappings
        +setup(): void
        +init(organizer: IOrganizer): bool
        +name(): string
        +author(): string
        +description(): string
        +version(): VersionInfo
        +isActive(): bool
        +settings(): List~PluginSetting~
        +detectGame(): void
        +gameName(): string
        +gameShortName(): string
        +gameIcon(): QIcon
        +validShortNames(): List~string~
        +gameNexusName(): string
        +nexusModOrganizerID(): int
        +nexusGameID(): int
        +steamAPPId(): string
        +gogAPPId(): string
        +epicAPPId(): string
        +eaDesktopContentId(): string
        +binaryName(): string
        +getLauncherName(): string
        +getSupportURL(): string
        +iniFiles(): List~string~
        +executables(): List~ExecutableInfo~
        +executableForcedLoads(): List~ExecutableForcedLoadSetting~
        +listSaves(folder: QDir): List~ISaveGame~
        +initializeProfile(directory: QDir, settings: ProfileSetting): void
        +setGameVariant(variant: string): void
        +gameVersion(): string
        +looksValid(directory: QDir): bool
        +isInstalled(): bool
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +setGamePath(path: Path | string): void
        +documentsDirectory(): QDir
        +savesDirectory(): QDir
    }
    
    class BasicGameMapping~T~ {
        -BasicGame _game
        -string _exposed_name
        -string _internal_method_name
        -bool _required
        -Callable _default
        -Callable _apply_fn
        +get(): T
    }
    
    class BasicGameOptionsMapping~T~ {
        -int _index
        +set_index(index: int): void
        +set_value(value: T): void
        +has_value(): bool
        +current(): T
    }
    
    class BasicGameMappings {
        -BasicGame _game
        +name: BasicGameMapping~string~
        +author: BasicGameMapping~string~
        +version: BasicGameMapping~VersionInfo~
        +description: BasicGameMapping~string~
        +gameName: BasicGameMapping~string~
        +gameShortName: BasicGameMapping~string~
        +gameNexusName: BasicGameMapping~string~
        +validShortNames: BasicGameMapping~List~string~~
        +nexusGameId: BasicGameMapping~int~
        +binaryName: BasicGameMapping~string~
        +launcherName: BasicGameMapping~string~
        +dataDirectory: BasicGameMapping~string~
        +documentsDirectory: BasicGameMapping~QDir~
        +iniFiles: BasicGameMapping~List~string~~
        +savesDirectory: BasicGameMapping~QDir~
        +savegameExtension: BasicGameMapping~string~
        +steamAPPId: BasicGameOptionsMapping~string~
        +gogAPPId: BasicGameOptionsMapping~string~
        +originManifestIds: BasicGameOptionsMapping~string~
        +originWatcherExecutables: BasicGameMapping~List~string~~
        +epicAPPId: BasicGameOptionsMapping~string~
        +eaDesktopContentId: BasicGameOptionsMapping~string~
        +supportURL: BasicGameMapping~string~
    }
    
    class BasicIniGame {
        +__init__(path: string): void
    }
    
    class BasicGameSaveGameInfo {
        +__init__(get_preview_image: Callable): void
        +getSaveGameWidget(parent: QWidget): QWidget
        +setSaveGame(save: ISaveGame): void
        +displayName(): string
    }
    
    class BasicGameSaveGame {
        -Path _filepath
        +__init__(filepath: Path): void
        +getFilepath(): string
        +getName(): string
        +getSaveGroupIdentifier(): string
        +allFiles(): List~string~
    }
    
    BasicGame --> BasicGameMappings
    BasicGameMappings --> BasicGameMapping
    BasicGameMappings --> BasicGameOptionsMapping
    BasicGameMapping <|-- BasicGameOptionsMapping
    BasicGame <|-- BasicIniGame
    BasicGame --> BasicGameSaveGameInfo
    BasicGameSaveGameInfo --> BasicGameSaveGame
```

## Plugin Inheritance

The following diagram shows the inheritance hierarchy of the Basic Games plugin:

```mermaid
classDiagram
    class IPlugin {
        +init(organizer: IOrganizer): bool
        +name(): string
        +author(): string
        +description(): string
        +version(): VersionInfo
        +isActive(): bool
        +settings(): List~PluginSetting~
    }
    
    class IPluginGame {
        +detectGame(): void
        +gameName(): string
        +gameShortName(): string
        +gameIcon(): QIcon
        +validShortNames(): List~string~
        +gameNexusName(): string
        +nexusModOrganizerID(): int
        +nexusGameID(): int
        +steamAPPId(): string
        +gogAPPId(): string
        +epicAPPId(): string
        +eaDesktopContentId(): string
        +binaryName(): string
        +getLauncherName(): string
        +getSupportURL(): string
        +iniFiles(): List~string~
        +executables(): List~ExecutableInfo~
        +executableForcedLoads(): List~ExecutableForcedLoadSetting~
        +listSaves(folder: QDir): List~ISaveGame~
        +initializeProfile(directory: QDir, settings: ProfileSetting): void
        +setGameVariant(variant: string): void
        +gameVersion(): string
        +looksValid(directory: QDir): bool
        +isInstalled(): bool
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +setGamePath(path: Path | string): void
        +documentsDirectory(): QDir
        +savesDirectory(): QDir
    }
    
    class ISaveGame {
        +getFilepath(): string
        +getName(): string
        +getSaveGroupIdentifier(): string
        +allFiles(): List~string~
    }
    
    class ISaveGameInfoWidget {
        +getSaveGameWidget(parent: QWidget): QWidget
        +setSaveGame(save: ISaveGame): void
        +displayName(): string
    }
    
    class BasicGame {
        +setup(): void
        +init(organizer: IOrganizer): bool
        +name(): string
        +author(): string
        +description(): string
        +version(): VersionInfo
        +isActive(): bool
        +settings(): List~PluginSetting~
        +detectGame(): void
        +gameName(): string
        +gameShortName(): string
        +gameIcon(): QIcon
        +validShortNames(): List~string~
        +gameNexusName(): string
        +nexusModOrganizerID(): int
        +nexusGameID(): int
        +steamAPPId(): string
        +gogAPPId(): string
        +epicAPPId(): string
        +eaDesktopContentId(): string
        +binaryName(): string
        +getLauncherName(): string
        +getSupportURL(): string
        +iniFiles(): List~string~
        +executables(): List~ExecutableInfo~
        +executableForcedLoads(): List~ExecutableForcedLoadSetting~
        +listSaves(folder: QDir): List~ISaveGame~
        +initializeProfile(directory: QDir, settings: ProfileSetting): void
        +setGameVariant(variant: string): void
        +gameVersion(): string
        +looksValid(directory: QDir): bool
        +isInstalled(): bool
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +setGamePath(path: Path | string): void
        +documentsDirectory(): QDir
        +savesDirectory(): QDir
    }
    
    class BasicIniGame {
        +__init__(path: string): void
    }
    
    class BasicGameSaveGame {
        +__init__(filepath: Path): void
        +getFilepath(): string
        +getName(): string
        +getSaveGroupIdentifier(): string
        +allFiles(): List~string~
    }
    
    class BasicGameSaveGameInfo {
        +__init__(get_preview_image: Callable): void
        +getSaveGameWidget(parent: QWidget): QWidget
        +setSaveGame(save: ISaveGame): void
        +displayName(): string
    }
    
    class GameImplementation {
        +Name: string
        +Author: string
        +Version: string
        +GameName: string
        +GameShortName: string
        +GameNexusName: string
        +GameNexusId: int
        +GameSteamId: List~string~
        +GameGogId: List~string~
        +GameBinary: string
        +GameDataPath: string
        +GameSaveExtension: string
        +GameDocumentsDirectory: string
        +GameSavesDirectory: string
    }
    
    IPlugin <|-- IPluginGame
    IPluginGame <|-- BasicGame
    BasicGame <|-- BasicIniGame
    BasicGame <|-- GameImplementation
    ISaveGame <|-- BasicGameSaveGame
    ISaveGameInfoWidget <|-- BasicGameSaveGameInfo
```

## Game Detection Process

The following sequence diagram shows the game detection process of the Basic Games plugin:

```mermaid
sequenceDiagram
    participant MO2 as Mod Organizer 2
    participant BasicGame
    participant SteamGames
    participant GOGGames
    participant OriginGames
    participant EpicGames
    participant EADesktopGames
    
    MO2->>BasicGame: detectGame()
    
    loop for each Steam App ID
        BasicGame->>SteamGames: check if game is installed
        SteamGames-->>BasicGame: game path or null
        alt game found
            BasicGame->>BasicGame: setGamePath(path)
            BasicGame-->>MO2: return
        end
    end
    
    loop for each GOG App ID
        BasicGame->>GOGGames: check if game is installed
        GOGGames-->>BasicGame: game path or null
        alt game found
            BasicGame->>BasicGame: setGamePath(path)
            BasicGame-->>MO2: return
        end
    end
    
    loop for each Origin Manifest ID
        BasicGame->>OriginGames: check if game is installed
        OriginGames-->>BasicGame: game path or null
        alt game found
            BasicGame->>BasicGame: setGamePath(path)
            BasicGame-->>MO2: return
        end
    end
    
    loop for each Epic App ID
        BasicGame->>EpicGames: check if game is installed
        EpicGames-->>BasicGame: game path or null
        alt game found
            BasicGame->>BasicGame: setGamePath(path)
            BasicGame-->>MO2: return
        end
    end
    
    loop for each EA Desktop Content ID
        BasicGame->>EADesktopGames: check if game is installed
        EADesktopGames-->>BasicGame: game path or null
        alt game found
            BasicGame->>BasicGame: setGamePath(path)
            BasicGame-->>MO2: return
        end
    end
    
    BasicGame-->>MO2: return (game not found)
```

## Game Initialization Process

The following sequence diagram shows the game initialization process of the Basic Games plugin:

```mermaid
sequenceDiagram
    participant MO2 as Mod Organizer 2
    participant BasicGame
    participant GameFeatures
    
    MO2->>BasicGame: init(organizer)
    BasicGame->>BasicGame: store organizer
    
    BasicGame->>GameFeatures: register BasicGameSaveGameInfo
    GameFeatures-->>BasicGame: registration result
    
    alt Origin Watcher Executables are defined
        BasicGame->>BasicGame: create Origin Watcher
        BasicGame->>MO2: register onAboutToRun callback
        MO2-->>BasicGame: registration result
        BasicGame->>MO2: register onFinishedRun callback
        MO2-->>BasicGame: registration result
    end
    
    BasicGame-->>MO2: true
```

## Save Game Handling

The following sequence diagram shows the save game handling process of the Basic Games plugin:

```mermaid
sequenceDiagram
    participant MO2 as Mod Organizer 2
    participant BasicGame
    participant BasicGameSaveGame
    
    MO2->>BasicGame: listSaves(folder)
    BasicGame->>BasicGame: get save game extension
    
    loop for each save file in folder
        BasicGame->>BasicGameSaveGame: create save game object
        BasicGameSaveGame-->>BasicGame: save game object
    end
    
    BasicGame-->>MO2: list of save game objects
```

## Game Implementation

The following diagram shows the structure of a game implementation:

```mermaid
classDiagram
    class BasicGame {
        +setup(): void
        +init(organizer: IOrganizer): bool
        +name(): string
        +author(): string
        +description(): string
        +version(): VersionInfo
        +isActive(): bool
        +settings(): List~PluginSetting~
        +detectGame(): void
        +gameName(): string
        +gameShortName(): string
        +gameIcon(): QIcon
        +validShortNames(): List~string~
        +gameNexusName(): string
        +nexusModOrganizerID(): int
        +nexusGameID(): int
        +steamAPPId(): string
        +gogAPPId(): string
        +epicAPPId(): string
        +eaDesktopContentId(): string
        +binaryName(): string
        +getLauncherName(): string
        +getSupportURL(): string
        +iniFiles(): List~string~
        +executables(): List~ExecutableInfo~
        +executableForcedLoads(): List~ExecutableForcedLoadSetting~
        +listSaves(folder: QDir): List~ISaveGame~
        +initializeProfile(directory: QDir, settings: ProfileSetting): void
        +setGameVariant(variant: string): void
        +gameVersion(): string
        +looksValid(directory: QDir): bool
        +isInstalled(): bool
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +setGamePath(path: Path | string): void
        +documentsDirectory(): QDir
        +savesDirectory(): QDir
    }
    
    class GameImplementation {
        +Name: string
        +Author: string
        +Version: string
        +GameName: string
        +GameShortName: string
        +GameNexusName: string
        +GameNexusId: int
        +GameSteamId: List~string~
        +GameGogId: List~string~
        +GameBinary: string
        +GameDataPath: string
        +GameSaveExtension: string
        +GameDocumentsDirectory: string
        +GameSavesDirectory: string
        +init(organizer: IOrganizer): bool
        +iniFiles(): List~string~
        +listSaves(folder: QDir): List~ISaveGame~
    }
    
    class GameSaveGame {
        +__init__(filepath: Path): void
        +allFiles(): List~string~
    }
    
    BasicGame <|-- GameImplementation
    BasicGameSaveGame <|-- GameSaveGame
```

## Plugin Registration

The following flowchart shows the plugin registration process of the Basic Games plugin:

```mermaid
flowchart TD
    Start([Start]) --> SetupBasicGame[Setup BasicGame]
    SetupBasicGame --> CreatePlugins[Create empty plugin list]
    
    CreatePlugins --> FindIniFiles[Find all .ini files in games directory]
    FindIniFiles --> ProcessIniFiles[Process each .ini file]
    ProcessIniFiles --> AddIniGames[Add BasicIniGame instances to plugin list]
    
    AddIniGames --> FindPyFiles[Find all .py files in games directory]
    FindPyFiles --> ProcessPyFiles[Process each .py file]
    ProcessPyFiles --> ImportModule[Import module]
    
    ImportModule --> FindClasses[Find all classes in module]
    FindClasses --> CheckClass{Is class a BasicGame subclass?}
    CheckClass -->|Yes| InstantiateClass[Instantiate class]
    CheckClass -->|No| NextClass[Check next class]
    
    InstantiateClass --> AddPyGames[Add instance to plugin list]
    NextClass --> CheckMoreClasses{More classes?}
    CheckMoreClasses -->|Yes| FindClasses
    CheckMoreClasses -->|No| NextFile[Process next .py file]
    
    NextFile --> CheckMoreFiles{More .py files?}
    CheckMoreFiles -->|Yes| ProcessPyFiles
    CheckMoreFiles -->|No| ReturnPlugins[Return plugin list]
    
    AddPyGames --> NextFile
    
    ReturnPlugins --> End([End])
```

These diagrams should help visualize the architecture and relationships of the Basic Games plugin for Mod Organizer 2.
