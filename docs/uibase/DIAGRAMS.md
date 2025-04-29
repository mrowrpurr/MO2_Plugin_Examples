# Mod Organizer 2 UI Base Diagrams

This document provides visual diagrams of the interfaces and classes in the Mod Organizer 2 UI Base library to help understand their relationships.

## Plugin Interface Hierarchy

The following diagram shows the inheritance hierarchy of the plugin interfaces in Mod Organizer 2:

```mermaid
classDiagram
    IPlugin <|-- IPluginTool
    IPlugin <|-- IPluginGame
    IPlugin <|-- IPluginInstaller
    IPlugin <|-- IPluginModPage
    IPlugin <|-- IPluginPreview
    
    IPluginInstaller <|-- IPluginInstallerSimple
    IPluginInstaller <|-- IPluginInstallerCustom
    
    class IPlugin {
        +init(IOrganizer* organizer)
        +name() const
        +localizedName() const
        +master() const
        +requirements() const
        +author() const
        +description() const
        +version() const
        +settings() const
        +enabledByDefault() const
    }
    
    class IPluginTool {
        +displayName() const
        +tooltip() const
        +icon() const
        +display() const
    }
    
    class IPluginGame {
        +gameName() const
        +displayGameName() const
        +detectGame()
        +initializeProfile()
        +isInstalled() const
        +gameIcon() const
        +gameDirectory() const
        +dataDirectory() const
        +setGamePath()
        +...()
    }
    
    class IPluginInstaller {
        +priority() const
        +isManualInstaller() const
        +isArchiveSupported() const
        +onInstallationStart()
        +onInstallationEnd()
    }
    
    class IPluginInstallerSimple {
        +install()
    }
    
    class IPluginInstallerCustom {
        +isArchiveSupported() const
        +supportedExtensions() const
        +install()
    }
    
    class IPluginModPage {
        +displayName() const
        +icon() const
        +pageURL() const
        +useIntegratedBrowser() const
        +handlesDownload() const
    }
    
    class IPluginPreview {
        +supportedExtensions() const
        +supportsArchives() const
        +genFilePreview() const
        +genDataPreview() const
    }
```

## Additional Plugin Interfaces

Some plugin interfaces don't inherit directly from `IPlugin` to prevent multiple inheritance issues:

```mermaid
classDiagram
    class IPluginDiagnose {
        +activeProblems() const
        +shortDescription() const
        +fullDescription() const
        +hasGuidedFix() const
        +startGuidedFix() const
    }
    
    class IPluginFileMapper {
        +mappings() const
    }
```

## Core Interfaces Relationships

The following diagram shows the relationships between the core interfaces in Mod Organizer 2:

```mermaid
classDiagram
    IOrganizer --> IModList : provides
    IOrganizer --> IPluginList : provides
    IOrganizer --> IDownloadManager : provides
    IOrganizer --> IModRepositoryBridge : creates
    IOrganizer --> IProfile : provides
    IOrganizer --> IGameFeatures : provides
    IOrganizer --> IFileTree : provides
    
    IModList --> IModInterface : manages
    IPluginList --> GamePlugins : manages
    
    class IOrganizer {
        +createNexusBridge() const
        +profileName() const
        +profilePath() const
        +downloadsPath() const
        +overwritePath() const
        +basePath() const
        +modsPath() const
        +appVersion() const
        +createMod()
        +getGame() const
        +modDataChanged()
        +isPluginEnabled() const
        +pluginSetting() const
        +setPluginSetting()
        +persistent() const
        +setPersistent()
        +pluginDataPath() const
        +installMod()
        +resolvePath() const
        +listDirectories() const
        +findFiles() const
        +getFileOrigins() const
        +findFileInfos() const
        +virtualFileTree() const
        +downloadManager() const
        +pluginList() const
        +modList() const
        +profile() const
        +gameFeatures() const
        +startApplication()
        +waitForApplication() const
        +refresh()
        +managedGame() const
    }
    
    class IModList {
        +displayName() const
        +allMods() const
        +allModsByProfilePriority() const
        +getMod() const
        +removeMod()
        +renameMod()
        +state() const
        +setActive()
        +priority() const
        +setPriority()
    }
    
    class IPluginList {
        +pluginNames() const
        +state() const
        +setState()
        +priority() const
        +setPriority()
        +loadOrder() const
        +setLoadOrder()
        +isMaster() const
        +masters() const
        +origin() const
    }
    
    class IModInterface {
        +name() const
        +absolutePath() const
        +comments() const
        +notes() const
        +gameName() const
        +repository() const
        +nexusId() const
        +version() const
        +newestVersion() const
        +ignoredVersion() const
        +installationFile() const
        +installedFiles() const
        +converted() const
        +validated() const
        +color() const
        +url() const
        +primaryCategory() const
        +categories() const
        +trackedState() const
        +endorsedState() const
        +fileTree() const
        +isOverwrite() const
        +isBackup() const
        +isSeparator() const
        +isForeign() const
    }
    
    class IProfile {
        +name() const
        +absolutePath() const
        +localSavesEnabled() const
        +localSettingsEnabled() const
        +invalidationActive() const
        +absoluteIniFilePath() const
    }
    
    class IDownloadManager {
        +startDownloadURLs()
        +startDownloadNexusFile()
        +startDownloadNexusFileForGame()
        +downloadPath()
    }
    
    class IModRepositoryBridge {
        +requestDescription()
        +requestFiles()
        +requestFileInfo()
        +requestDownloadURL()
        +requestToggleEndorsement()
    }
    
    class IFileTree {
        +exists()
        +find()
        +findDirectory()
        +pathTo()
        +walk()
        +createOrphanTree()
        +addFile()
        +addDirectory()
        +insert()
        +merge()
        +move()
        +copy()
        +erase()
        +clear()
        +removeAll()
        +removeIf()
    }
    
    class IGameFeatures {
        +registerFeature()
        +unregisterFeature()
        +gameFeature()
    }
```

## Game Features Hierarchy

The following diagram shows the game feature interfaces in Mod Organizer 2:

```mermaid
classDiagram
    GameFeature <|-- BSAInvalidation
    GameFeature <|-- DataArchives
    GameFeature <|-- GamePlugins
    GameFeature <|-- LocalSavegames
    GameFeature <|-- ModDataChecker
    GameFeature <|-- ModDataContent
    GameFeature <|-- SaveGameInfo
    GameFeature <|-- ScriptExtender
    GameFeature <|-- UnmanagedMods
    
    class GameFeature {
        +typeInfo() const
    }
    
    class BSAInvalidation {
        +isInvalidationBSA()
        +deactivate()
        +activate()
        +prepareProfile()
    }
    
    class DataArchives {
        +vanillaArchives() const
        +archives() const
        +addArchive()
        +removeArchive()
    }
    
    class GamePlugins {
        +writePluginLists()
        +readPluginLists()
        +getLoadOrder()
        +lightPluginsAreSupported()
        +mediumPluginsAreSupported()
        +blueprintPluginsAreSupported()
    }
    
    class LocalSavegames {
        +mappings() const
        +prepareProfile()
    }
    
    class ModDataChecker {
        +dataLooksValid() const
        +fix() const
    }
    
    class ModDataContent {
        +getAllContents() const
        +getContentsFor() const
    }
    
    class SaveGameInfo {
        +getMissingAssets() const
        +getSaveGameWidget() const
    }
    
    class ScriptExtender {
        +BinaryName() const
        +PluginPath() const
        +loaderName() const
        +loaderPath() const
        +savegameExtension() const
        +isInstalled() const
        +getExtenderVersion() const
        +getArch() const
    }
    
    class UnmanagedMods {
        +mods() const
        +displayName() const
        +referenceFile() const
        +secondaryFiles() const
    }
```

## Plugin Development Flow

The following diagram shows the typical flow of a plugin in Mod Organizer 2:

```mermaid
flowchart TD
    A[Plugin Creation] --> B[Implement IPlugin Interface]
    B --> C{Choose Plugin Type}
    C --> D[IPluginTool]
    C --> E[IPluginGame]
    C --> F[IPluginInstaller]
    C --> G[IPluginModPage]
    C --> H[IPluginPreview]
    C --> I[IPluginDiagnose]
    C --> J[IPluginFileMapper]
    
    D & E & F & G & H & I & J --> K[Implement Required Methods]
    K --> L[Register Plugin]
    L --> M[Plugin Initialization]
    M --> N[Plugin Usage]
    
    M -- IOrganizer* --> O[Access MO2 Functionality]
    O --> P[Access Mods]
    O --> Q[Access Game Plugins]
    O --> R[Access Profiles]
    O --> S[Access Downloads]
    O --> T[Access Game Features]
```

## Plugin Type Decision Tree

The following diagram helps decide which plugin type to implement based on the desired functionality:

```mermaid
flowchart TD
    A[What functionality do you need?] --> B{Add a new game?}
    B -- Yes --> C[Implement IPluginGame]
    
    B -- No --> D{Add a tool to the toolbar?}
    D -- Yes --> E[Implement IPluginTool]
    
    D -- No --> F{Install mods in a custom way?}
    F -- Yes --> G{Need full control over extraction?}
    G -- Yes --> H[Implement IPluginInstallerCustom]
    G -- No --> I[Implement IPluginInstallerSimple]
    
    F -- No --> J{Add support for a mod website?}
    J -- Yes --> K[Implement IPluginModPage]
    
    J -- No --> L{Preview file types?}
    L -- Yes --> M[Implement IPluginPreview]
    
    L -- No --> N{Diagnose problems?}
    N -- Yes --> O[Implement IPluginDiagnose]
    
    N -- No --> P{Map virtual files?}
    P -- Yes --> Q[Implement IPluginFileMapper]
    
    P -- No --> R[Consider a custom plugin combining interfaces]
```

These diagrams should help visualize the relationships between the different interfaces in Mod Organizer 2 and make it easier to understand how to develop plugins for it.
