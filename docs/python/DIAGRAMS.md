# Mod Organizer 2 Python Plugin System Diagrams

This document provides visual diagrams of the architecture and relationships of the Python plugin system for Mod Organizer 2.

## Table of Contents

- [Mod Organizer 2 Python Plugin System Diagrams](#mod-organizer-2-python-plugin-system-diagrams)
  - [Table of Contents](#table-of-contents)
  - [System Architecture](#system-architecture)
  - [Component Relationships](#component-relationships)
  - [Plugin Loading Sequence](#plugin-loading-sequence)
  - [Python Plugin Structure](#python-plugin-structure)
  - [Plugin Interface Hierarchy](#plugin-interface-hierarchy)
  - [Trampoline Class Hierarchy](#trampoline-class-hierarchy)
  - [Memory Management](#memory-management)

## System Architecture

The following diagram shows the overall architecture of the Python plugin system:

```mermaid
flowchart TD
    subgraph MO2[Mod Organizer 2]
        IOrganizer
        PluginSystem
    end
    
    subgraph PythonProxy[Python Proxy Plugin]
        ProxyPython
    end
    
    subgraph PythonRunner[Python Runner]
        Runner
        PythonInterpreter
    end
    
    subgraph PythonBindings[Python Bindings]
        mobase
        pybind11_qt
        pybind11_utils
    end
    
    subgraph PythonPlugins[Python Plugins]
        Plugin1
        Plugin2
        Plugin3
    end
    
    MO2 --> PythonProxy
    PythonProxy --> PythonRunner
    PythonRunner --> PythonInterpreter
    PythonInterpreter --> PythonBindings
    PythonInterpreter --> PythonPlugins
    PythonPlugins --> PythonBindings
    PythonBindings --> MO2
```

## Component Relationships

The following diagram shows the relationships between the components of the Python plugin system:

```mermaid
classDiagram
    class IPluginProxy {
        +pluginList(pluginPath: QDir): QStringList
        +load(identifier: QString): QList<QObject*>
        +unload(identifier: QString): void
    }
    
    class ProxyPython {
        -m_MOInfo: IOrganizer*
        -m_RunnerLib: HMODULE
        -m_Runner: IPythonRunner*
        -m_LoadFailure: FailureType
        +init(moInfo: IOrganizer*): bool
        +pluginList(pluginPath: QDir): QStringList
        +load(identifier: QString): QList<QObject*>
        +unload(identifier: QString): void
    }
    
    class IPythonRunner {
        +load(identifier: QString): QList<QObject*>
        +unload(identifier: QString): void
        +initialize(pythonPaths: vector<path>): bool
        +addDllSearchPath(dllPath: path): void
        +isInitialized(): bool
    }
    
    class PythonRunner {
        -m_PythonObjects: unordered_map<QString, vector<py::handle>>
        -ensureFolderInPath(folder: QString): void
        +load(identifier: QString): QList<QObject*>
        +unload(identifier: QString): void
        +initialize(pythonPaths: vector<path>): bool
        +addDllSearchPath(dllPath: path): void
        +isInitialized(): bool
    }
    
    IPluginProxy <|-- ProxyPython
    IPythonRunner <|-- PythonRunner
    ProxyPython --> IPythonRunner
```

## Plugin Loading Sequence

The following sequence diagram shows the process of loading a Python plugin:

```mermaid
sequenceDiagram
    participant MO2 as Mod Organizer 2
    participant Proxy as Python Proxy Plugin
    participant Runner as Python Runner
    participant Interpreter as Python Interpreter
    participant Plugin as Python Plugin
    
    MO2->>Proxy: init(IOrganizer*)
    Proxy->>Runner: initialize(pythonPaths)
    Runner->>Interpreter: py::initialize_interpreter()
    Interpreter-->>Runner: Initialized
    Runner-->>Proxy: true
    
    MO2->>Proxy: pluginList(pluginPath)
    Proxy-->>MO2: [plugin1.py, plugin2]
    
    MO2->>Proxy: load(plugin1.py)
    Proxy->>Runner: load(plugin1.py)
    Runner->>Interpreter: py::gil_scoped_acquire
    Runner->>Interpreter: py::eval_file(plugin1.py)
    Interpreter->>Plugin: import
    Plugin-->>Interpreter: module
    Runner->>Plugin: createPlugin()
    Plugin-->>Runner: plugin object
    Runner->>Interpreter: extract_plugins(plugin object)
    Interpreter-->>Runner: QList<QObject*>
    Runner-->>Proxy: QList<QObject*>
    Proxy-->>MO2: QList<QObject*>
    
    MO2->>Proxy: unload(plugin1.py)
    Proxy->>Runner: unload(plugin1.py)
    Runner->>Interpreter: py::gil_scoped_acquire
    Runner->>Interpreter: clear plugin objects
    Runner-->>Proxy: void
    Proxy-->>MO2: void
```

## Python Plugin Structure

The following diagram shows the structure of a Python plugin:

```mermaid
classDiagram
    class IPlugin {
        +init(organizer: IOrganizer): bool
        +name(): QString
        +author(): QString
        +description(): QString
        +version(): VersionInfo
        +settings(): QList<PluginSetting>
    }
    
    class IPluginTool {
        +displayName(): QString
        +tooltip(): QString
        +icon(): QIcon
        +setParentWidget(widget: QWidget): void
        +display(): void
    }
    
    class MyTool {
        -_organizer: IOrganizer
        -_parentWidget: QWidget
        +init(organizer: IOrganizer): bool
        +name(): QString
        +author(): QString
        +description(): QString
        +version(): VersionInfo
        +settings(): QList<PluginSetting>
        +displayName(): QString
        +tooltip(): QString
        +icon(): QIcon
        +setParentWidget(widget: QWidget): void
        +display(): void
    }
    
    class createPlugin {
        +(): MyTool
    }
    
    IPlugin <|-- IPluginTool
    IPluginTool <|-- MyTool
    MyTool <-- createPlugin
```

## Plugin Interface Hierarchy

The following diagram shows the hierarchy of plugin interfaces:

```mermaid
classDiagram
    class IPlugin {
        +init(organizer: IOrganizer): bool
        +name(): QString
        +author(): QString
        +description(): QString
        +version(): VersionInfo
        +settings(): QList<PluginSetting>
    }
    
    class IPluginTool {
        +displayName(): QString
        +tooltip(): QString
        +icon(): QIcon
        +setParentWidget(widget: QWidget): void
        +display(): void
    }
    
    class IPluginGame {
        +detectGame(): void
        +gameName(): QString
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +executableForcedLoads(): QList<ExecutableForcedLoadSetting>
        +gameShortName(): QString
        +gameNexusName(): QString
        +nexusGameID(): int
        +...()
    }
    
    class IPluginInstaller {
        +isArchiveSupported(tree: IFileTree): bool
        +priority(): unsigned int
        +isManualInstaller(): bool
        +...()
    }
    
    class IPluginInstallerSimple {
        +install(modName: GuessedValue<QString>, tree: IFileTree, version: QString, nexusID: int): EInstallResult
    }
    
    class IPluginInstallerCustom {
        +isArchiveSupported(archiveName: QString): bool
        +supportedExtensions(): set<QString>
        +install(modName: GuessedValue<QString>, gameName: QString, archiveName: QString, version: QString, nexusID: int): EInstallResult
    }
    
    class IPluginModPage {
        +displayName(): QString
        +icon(): QIcon
        +pageURL(): QUrl
        +useIntegratedBrowser(): bool
        +handlesDownload(pageURL: QUrl, downloadURL: QUrl, fileInfo: ModRepositoryFileInfo): bool
        +setParentWidget(widget: QWidget): void
    }
    
    class IPluginPreview {
        +supportedExtensions(): set<QString>
        +supportsArchives(): bool
        +genFilePreview(fileName: QString, maxSize: QSize): QWidget*
        +genDataPreview(fileData: QByteArray, fileName: QString, maxSize: QSize): QWidget*
    }
    
    IPlugin <|-- IPluginTool
    IPlugin <|-- IPluginGame
    IPlugin <|-- IPluginInstaller
    IPluginInstaller <|-- IPluginInstallerSimple
    IPluginInstaller <|-- IPluginInstallerCustom
    IPlugin <|-- IPluginModPage
    IPlugin <|-- IPluginPreview
```

## Trampoline Class Hierarchy

The following diagram shows the hierarchy of trampoline classes:

```mermaid
classDiagram
    class PyPluginBaseNoFinal~PluginBase~ {
        +init(organizer: IOrganizer): bool
        +name(): QString
        +localizedName(): QString
        +master(): QString
        +author(): QString
        +description(): QString
        +version(): VersionInfo
        +settings(): QList<PluginSetting>
    }
    
    class PyPluginBase~PluginBase~ {
        +requirements(): vector<shared_ptr<const IPluginRequirement>>
        +enabledByDefault(): bool
    }
    
    class PyPlugin {
        // Inherits from PyPluginBase<IPyPlugin>
    }
    
    class PyPluginTool {
        +displayName(): QString
        +tooltip(): QString
        +icon(): QIcon
        +setParentWidget(widget: QWidget): void
        +display(): void
    }
    
    class PyPluginGame {
        +detectGame(): void
        +gameName(): QString
        +gameDirectory(): QDir
        +dataDirectory(): QDir
        +executableForcedLoads(): QList<ExecutableForcedLoadSetting>
        +gameShortName(): QString
        +gameNexusName(): QString
        +nexusGameID(): int
        +...()
    }
    
    PyPluginBaseNoFinal <|-- PyPluginBase
    PyPluginBase <|-- PyPlugin
    PyPluginBase <|-- PyPluginTool
    PyPluginBaseNoFinal <|-- PyPluginGame
```

## Memory Management

The following diagram shows the memory management of Python objects:

```mermaid
flowchart TD
    subgraph CPP[C++ Side]
        QObject
        IPlugin
    end
    
    subgraph Python[Python Side]
        PyObject
        PyPlugin
    end
    
    PyPlugin --> PyObject
    PyObject --> QObject
    PyPlugin --> IPlugin
    IPlugin --> QObject
    
    PyObject -- "py::qt::set_qt_owner()" --> QObject
```

These diagrams should help visualize the architecture and relationships of the Python plugin system for Mod Organizer 2.
