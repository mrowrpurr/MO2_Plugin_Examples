# MO2 Game Features Diagrams

This document provides visual representations of the MO2 Game Features system to help understand its architecture and relationships.

## Table of Contents

- [MO2 Game Features Diagrams](#mo2-game-features-diagrams)
  - [Table of Contents](#table-of-contents)
  - [Class Hierarchy](#class-hierarchy)
  - [Game Features Registration](#game-features-registration)
  - [Feature Type Relationships](#feature-type-relationships)
  - [Feature Interaction with MO2](#feature-interaction-with-mo2)
  - [Feature Priority and Overriding](#feature-priority-and-overriding)
  - [Game Feature Implementation Example](#game-feature-implementation-example)

## Class Hierarchy

```mermaid
classDiagram
    class GameFeature {
        <<abstract>>
        +virtual ~GameFeature() = 0
        +virtual const std::type_info& typeInfo() const = 0
    }
    
    class GameFeatureCRTP~T~ {
        +const std::type_info& typeInfo() const
    }
    
    GameFeature <|-- GameFeatureCRTP
    
    class BSAInvalidation {
        <<interface>>
        +bool isInvalidationBSA(const QString& bsaName)
        +void deactivate(IProfile* profile)
        +void activate(IProfile* profile)
        +bool prepareProfile(IProfile* profile)
    }
    
    class DataArchives {
        <<interface>>
        +QStringList vanillaArchives() const
        +QStringList archives(const IProfile* profile) const
        +void addArchive(IProfile* profile, int index, const QString& archiveName)
        +void removeArchive(IProfile* profile, const QString& archiveName)
    }
    
    class GamePlugins {
        <<interface>>
        +void writePluginLists(const IPluginList* pluginList)
        +void readPluginLists(IPluginList* pluginList)
        +QStringList getLoadOrder()
        +bool lightPluginsAreSupported()
        +bool mediumPluginsAreSupported()
        +bool blueprintPluginsAreSupported()
    }
    
    class LocalSavegames {
        <<interface>>
        +MappingType mappings(const QDir& profileSaveDir) const
        +bool prepareProfile(IProfile* profile)
    }
    
    class ModDataChecker {
        <<interface>>
        +enum CheckReturn
        +CheckReturn dataLooksValid(std::shared_ptr~const IFileTree~ fileTree) const
        +std::shared_ptr~IFileTree~ fix(std::shared_ptr~IFileTree~ fileTree) const
    }
    
    class ModDataContent {
        <<interface>>
        +struct Content
        +std::vector~Content~ getAllContents() const
        +std::vector~int~ getContentsFor(std::shared_ptr~const IFileTree~ fileTree) const
    }
    
    class SaveGameInfo {
        <<interface>>
        +typedef QStringList ProvidingModules
        +typedef QMap~QString, ProvidingModules~ MissingAssets
        +MissingAssets getMissingAssets(ISaveGame const& save) const
        +ISaveGameInfoWidget* getSaveGameWidget(QWidget* parent) const
    }
    
    class ScriptExtender {
        <<interface>>
        +QString BinaryName() const
        +QString PluginPath() const
        +QString loaderName() const
        +QString loaderPath() const
        +QString savegameExtension() const
        +bool isInstalled() const
        +QString getExtenderVersion() const
        +WORD getArch() const
    }
    
    class UnmanagedMods {
        <<interface>>
        +QStringList mods(bool onlyOfficial) const
        +QString displayName(const QString& modName) const
        +QFileInfo referenceFile(const QString& modName) const
        +QStringList secondaryFiles(const QString& modName) const
    }
    
    GameFeatureCRTP <|-- BSAInvalidation
    GameFeatureCRTP <|-- DataArchives
    GameFeatureCRTP <|-- GamePlugins
    GameFeatureCRTP <|-- LocalSavegames
    GameFeatureCRTP <|-- ModDataChecker
    GameFeatureCRTP <|-- ModDataContent
    GameFeatureCRTP <|-- SaveGameInfo
    GameFeatureCRTP <|-- ScriptExtender
    GameFeatureCRTP <|-- UnmanagedMods
```

## Game Features Registration

```mermaid
sequenceDiagram
    participant GamePlugin as Game Plugin
    participant IOrganizer as IOrganizer
    participant IGameFeatures as IGameFeatures
    participant FeatureRegistry as Feature Registry
    
    GamePlugin->>GamePlugin: Create feature implementation
    GamePlugin->>IOrganizer: Get gameFeatures()
    IOrganizer-->>GamePlugin: Return IGameFeatures
    GamePlugin->>IGameFeatures: registerFeature(game, feature, priority)
    IGameFeatures->>FeatureRegistry: Store feature with metadata
    FeatureRegistry-->>IGameFeatures: Registration result
    IGameFeatures-->>GamePlugin: Registration result
```

## Feature Type Relationships

```mermaid
graph TD
    GF[GameFeature] --> BSA[BSAInvalidation]
    GF --> DA[DataArchives]
    GF --> GP[GamePlugins]
    GF --> LS[LocalSavegames]
    GF --> MDC[ModDataChecker]
    GF --> MDCo[ModDataContent]
    GF --> SGI[SaveGameInfo]
    GF --> SE[ScriptExtender]
    GF --> UM[UnmanagedMods]
    
    BSA --> BSA_Impl[Game-specific BSA Invalidation]
    DA --> DA_Impl[Game-specific Data Archives]
    GP --> GP_Impl[Game-specific Game Plugins]
    LS --> LS_Impl[Game-specific Local Savegames]
    MDC --> MDC_Impl[Game-specific Mod Data Checker]
    MDCo --> MDCo_Impl[Game-specific Mod Data Content]
    SGI --> SGI_Impl[Game-specific Save Game Info]
    SE --> SE_Impl[Game-specific Script Extender]
    UM --> UM_Impl[Game-specific Unmanaged Mods]
    
    subgraph "Game Plugin A"
        BSA_Impl
        DA_Impl
        GP_Impl
    end
    
    subgraph "Game Plugin B"
        LS_Impl
        MDC_Impl
        MDCo_Impl
    end
    
    subgraph "Game Plugin C"
        SGI_Impl
        SE_Impl
        UM_Impl
    end
```

## Feature Interaction with MO2

```mermaid
graph TD
    MO2[Mod Organizer 2] --> IGameFeatures
    
    IGameFeatures --> |"gameFeature<BSAInvalidation>()"| BSA[BSAInvalidation]
    IGameFeatures --> |"gameFeature<DataArchives>()"| DA[DataArchives]
    IGameFeatures --> |"gameFeature<GamePlugins>()"| GP[GamePlugins]
    IGameFeatures --> |"gameFeature<LocalSavegames>()"| LS[LocalSavegames]
    IGameFeatures --> |"gameFeature<ModDataChecker>()"| MDC[ModDataChecker]
    IGameFeatures --> |"gameFeature<ModDataContent>()"| MDCo[ModDataContent]
    IGameFeatures --> |"gameFeature<SaveGameInfo>()"| SGI[SaveGameInfo]
    IGameFeatures --> |"gameFeature<ScriptExtender>()"| SE[ScriptExtender]
    IGameFeatures --> |"gameFeature<UnmanagedMods>()"| UM[UnmanagedMods]
    
    BSA --> |"isInvalidationBSA()"| BSA_Use[BSA Invalidation Usage]
    DA --> |"archives()"| DA_Use[Data Archives Usage]
    GP --> |"writePluginLists()"| GP_Use[Game Plugins Usage]
    LS --> |"mappings()"| LS_Use[Local Savegames Usage]
    MDC --> |"dataLooksValid()"| MDC_Use[Mod Data Checker Usage]
    MDCo --> |"getContentsFor()"| MDCo_Use[Mod Data Content Usage]
    SGI --> |"getMissingAssets()"| SGI_Use[Save Game Info Usage]
    SE --> |"isInstalled()"| SE_Use[Script Extender Usage]
    UM --> |"mods()"| UM_Use[Unmanaged Mods Usage]
    
    subgraph "MO2 Core Functionality"
        BSA_Use
        DA_Use
        GP_Use
        LS_Use
        MDC_Use
        MDCo_Use
        SGI_Use
        SE_Use
        UM_Use
    end
```

## Feature Priority and Overriding

```mermaid
graph TD
    subgraph "Feature Registration"
        F1[Feature 1: Priority 50]
        F2[Feature 2: Priority 100]
        F3[Feature 3: Priority 75]
    end
    
    subgraph "Feature Selection"
        FS[Feature Selector]
        F1 --> FS
        F2 --> FS
        F3 --> FS
        FS --> |"Highest Priority"| F2
    end
    
    subgraph "Feature Combination"
        FC[Feature Combiner]
        F1 --> |"Priority Order"| FC
        F2 --> |"Priority Order"| FC
        F3 --> |"Priority Order"| FC
        FC --> |"Combined Result"| CR[Combined Features]
    end
    
    subgraph "Feature Usage"
        MO2[Mod Organizer 2]
        F2 --> |"Non-combinable Features"| MO2
        CR --> |"Combinable Features"| MO2
    end
```

## Game Feature Implementation Example

```mermaid
classDiagram
    class BSAInvalidation {
        <<interface>>
        +bool isInvalidationBSA(const QString& bsaName)
        +void deactivate(IProfile* profile)
        +void activate(IProfile* profile)
        +bool prepareProfile(IProfile* profile)
    }
    
    class SkyrimBSAInvalidation {
        +bool isInvalidationBSA(const QString& bsaName)
        +void deactivate(IProfile* profile)
        +void activate(IProfile* profile)
        +bool prepareProfile(IProfile* profile)
    }
    
    class FalloutBSAInvalidation {
        +bool isInvalidationBSA(const QString& bsaName)
        +void deactivate(IProfile* profile)
        +void activate(IProfile* profile)
        +bool prepareProfile(IProfile* profile)
    }
    
    BSAInvalidation <|-- SkyrimBSAInvalidation
    BSAInvalidation <|-- FalloutBSAInvalidation
    
    class GamePlugins {
        <<interface>>
        +void writePluginLists(const IPluginList* pluginList)
        +void readPluginLists(IPluginList* pluginList)
        +QStringList getLoadOrder()
        +bool lightPluginsAreSupported()
    }
    
    class SkyrimGamePlugins {
        +void writePluginLists(const IPluginList* pluginList)
        +void readPluginLists(IPluginList* pluginList)
        +QStringList getLoadOrder()
        +bool lightPluginsAreSupported()
    }
    
    class FalloutGamePlugins {
        +void writePluginLists(const IPluginList* pluginList)
        +void readPluginLists(IPluginList* pluginList)
        +QStringList getLoadOrder()
        +bool lightPluginsAreSupported()
    }
    
    GamePlugins <|-- SkyrimGamePlugins
    GamePlugins <|-- FalloutGamePlugins
