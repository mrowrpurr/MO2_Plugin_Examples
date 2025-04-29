# MO2 File Tree System Diagrams

This document provides visual representations of the file tree system in Mod Organizer 2, complementing the detailed explanations in [FILE_TREE_DETAILS.md](FILE_TREE_DETAILS.md).

## Table of Contents

- [MO2 File Tree System Diagrams](#mo2-file-tree-system-diagrams)
  - [Table of Contents](#table-of-contents)
  - [Class Hierarchy](#class-hierarchy)
  - [File Tree Implementations](#file-tree-implementations)
  - [Virtual File System Architecture](#virtual-file-system-architecture)
  - [File Tree Operations](#file-tree-operations)
  - [Plugin Integration](#plugin-integration)
  - [File Tree Traversal Example](#file-tree-traversal-example)
  - [Combining Physical and Virtual Trees](#combining-physical-and-virtual-trees)

## Class Hierarchy

```mermaid
classDiagram
    class FileTreeEntry {
        <<abstract>>
        +bool isFile()
        +bool isDir()
        +QString name()
        +QString path()
        +astree()
        +detach()
        +moveTo()
    }
    
    class IFileTree {
        <<interface>>
        +begin()
        +end()
        +find(path, type)
        +exists(path, type)
        +addFile(path)
        +addDirectory(path)
        +insert(entry)
        +merge(source)
        +walk(callback)
    }
    
    class QDirFileTree {
        <<concrete>>
        +static makeTree(QDir)
    }
    
    class ArchiveFileTree {
        <<concrete>>
        +static makeTree(Archive)
        +mapToArchive(Archive)
    }
    
    class VirtualFileTree {
        <<concrete>>
        +static makeTree(DirectoryEntry)
    }
    
    FileTreeEntry <|-- IFileTree
    IFileTree <|-- QDirFileTree
    IFileTree <|-- ArchiveFileTree
    IFileTree <|-- VirtualFileTree
```

## File Tree Implementations

```mermaid
graph TD
    subgraph "IFileTree Interface"
        IFT[IFileTree]
    end
    
    subgraph "Concrete Implementations"
        QDT[QDirFileTree]
        AFT[ArchiveFileTree]
        VFT[VirtualFileTree]
    end
    
    subgraph "Data Sources"
        FS[File System]
        AR[Archive Files]
        VFS[Virtual File System]
    end
    
    IFT --> QDT
    IFT --> AFT
    IFT --> VFT
    
    QDT --> FS
    AFT --> AR
    VFT --> VFS
    
    subgraph "Usage in MO2"
        MOD[Mod Files]
        INST[Installer]
        PLUG[Plugins]
    end
    
    FS --> MOD
    AR --> INST
    VFS --> PLUG
```

## Virtual File System Architecture

```mermaid
graph TD
    subgraph "MO2 Core"
        OC[OrganizerCore]
        DS[DirectoryStructure]
        VFT[VirtualFileTree]
        DR[DirectoryRefresher]
    end
    
    subgraph "Mod Management"
        ML[ModList]
        PROF[Profile]
        MODS[Mods]
    end
    
    subgraph "Plugin API"
        OP[OrganizerProxy]
        PLUG[Plugins]
    end
    
    OC --> DS
    OC --> VFT
    OC --> DR
    
    DR --> DS
    DS --> VFT
    
    ML --> PROF
    PROF --> MODS
    MODS --> DS
    
    OC --> OP
    OP --> PLUG
    VFT --> OP
    OP --> PLUG
```

## File Tree Operations

```mermaid
sequenceDiagram
    participant Plugin
    participant Organizer as IOrganizer
    participant VFT as VirtualFileTree
    participant DS as DirectoryStructure
    
    Plugin->>Organizer: virtualFileTree()
    Organizer->>VFT: value()
    VFT->>DS: getDirectoryEntry()
    DS-->>VFT: DirectoryEntry
    VFT-->>Organizer: IFileTree
    Organizer-->>Plugin: IFileTree
    
    Plugin->>VFT: find("meshes/actors/character.nif")
    VFT->>DS: searchFile("meshes/actors/character.nif")
    DS-->>VFT: FileEntry
    VFT-->>Plugin: FileTreeEntry
    
    Plugin->>Organizer: getFileOrigins("meshes/actors/character.nif")
    Organizer->>DS: getOriginByID(fileEntry->getOrigin())
    DS-->>Organizer: FilesOrigin
    Organizer-->>Plugin: QStringList origins
```

## Plugin Integration

```mermaid
graph TD
    subgraph "Plugin Development"
        PT[IPluginTool]
        UI[Custom UI]
        FTV[File Tree Viewer]
    end
    
    subgraph "MO2 API"
        ORG[IOrganizer]
        VFT[VirtualFileTree]
    end
    
    PT --> FTV
    FTV --> UI
    ORG --> VFT
    VFT --> FTV
    
    subgraph "User Interaction"
        BROWSE[Browse Files]
        SEARCH[Search Files]
        FILTER[Filter Content]
        ORIGIN[View Origins]
    end
    
    UI --> BROWSE
    UI --> SEARCH
    UI --> FILTER
    UI --> ORIGIN
```

## File Tree Traversal Example

```mermaid
graph TD
    subgraph "Virtual File Tree"
        ROOT[Data]
        MESH[meshes]
        TEX[textures]
        SCRIPT[scripts]
        
        ACT[actors]
        CHAR[character]
        ARMOR[armor]
        
        LAND[landscape]
        ARCH[architecture]
        
        DRAGON[dragon.nif]
        PLAYER[character.nif]
        IRON[iron.nif]
        
        DIRT[dirt.dds]
        STONE[stone.dds]
        
        QUEST[quest.pex]
    end
    
    ROOT --> MESH
    ROOT --> TEX
    ROOT --> SCRIPT
    
    MESH --> ACT
    MESH --> LAND
    
    ACT --> CHAR
    ACT --> ARMOR
    
    CHAR --> PLAYER
    CHAR --> DRAGON
    
    ARMOR --> IRON
    
    TEX --> ARCH
    
    ARCH --> DIRT
    ARCH --> STONE
    
    SCRIPT --> QUEST
    
    subgraph "Walk Operation"
        W1[Start at Root]
        W2[Process Each Entry]
        W3[Recurse into Directories]
        W4[Apply Filter]
    end
    
    W1 --> W2
    W2 --> W3
    W3 --> W4
    
    ROOT -.-> W1
    W2 -.-> MESH
    W2 -.-> TEX
    W2 -.-> SCRIPT
    W3 -.-> ACT
    W4 -.-> PLAYER
```

## Combining Physical and Virtual Trees

```mermaid
graph TD
    subgraph "Physical File System"
        PFS[Physical Files]
        PDATA[Data Directory]
        PBASE[Base Game Files]
        PDLC[DLC Files]
    end
    
    subgraph "Virtual File System"
        VFS[Virtual Files]
        VMODS[Mod Files]
        VOVER[Overwrite Files]
    end
    
    subgraph "Combined View"
        CV[Combined View]
        MERGED[Merged Files]
        CONFLICTS[Conflict Resolution]
    end
    
    PFS --> PDATA
    PDATA --> PBASE
    PDATA --> PDLC
    
    VFS --> VMODS
    VFS --> VOVER
    
    PDATA --> CV
    VFS --> CV
    
    CV --> MERGED
    CV --> CONFLICTS
    
    subgraph "User Interface"
        TREE[Tree View]
        LIST[List View]
        DETAILS[Details View]
    end
    
    CV --> TREE
    CV --> LIST
    CV --> DETAILS
