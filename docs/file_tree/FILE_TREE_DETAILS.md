# MO2 File Tree System

This document provides a detailed explanation of the file tree system in Mod Organizer 2, focusing on the `IFileTree` interface and its implementations, particularly the virtual file tree.

## Table of Contents

- [MO2 File Tree System](#mo2-file-tree-system)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [IFileTree Interface](#ifiletree-interface)
    - [Key Features](#key-features)
    - [Important Methods](#important-methods)
    - [FileTreeEntry](#filetreeentry)
  - [Concrete Implementations](#concrete-implementations)
    - [QDirFileTree](#qdirfiletree)
      - [Key Features](#key-features-1)
      - [Usage](#usage)
    - [ArchiveFileTree](#archivefiletree)
      - [Key Features](#key-features-2)
      - [Usage](#usage-1)
    - [VirtualFileTree](#virtualfiletree)
      - [Key Features](#key-features-3)
      - [Implementation Details](#implementation-details)
      - [Creation and Usage](#creation-and-usage)
  - [Usage in MO2](#usage-in-mo2)
    - [In OrganizerCore](#in-organizercore)
    - [In Plugins](#in-plugins)
  - [Creating Your Own Tab with IFileTree](#creating-your-own-tab-with-ifiletree)
    - [Example Plugin](#example-plugin)
    - [Example Dialog](#example-dialog)
  - [Advanced Usage](#advanced-usage)
    - [Combining Multiple Trees](#combining-multiple-trees)
    - [Filtering Files](#filtering-files)
    - [Walking the Tree](#walking-the-tree)
    - [Getting File Origins](#getting-file-origins)

## Overview

The file tree system in MO2 is built around the `IFileTree` interface, which provides a unified way to work with hierarchical file structures from various sources. This abstraction allows MO2 to handle files from different sources (disk, archives, virtual file system) in a consistent manner.

The key components of this system are:

1. **IFileTree Interface**: The base interface that defines operations for navigating and manipulating file trees.
2. **FileTreeEntry**: A class representing an entry in a file tree (either a file or a directory).
3. **Concrete Implementations**: Various implementations of IFileTree for different sources:
   - `QDirFileTree`: Represents a directory on disk
   - `ArchiveFileTree`: Represents files in an archive (BSA, BA2, ZIP, etc.)
   - `VirtualFileTree`: Represents MO2's virtual file system

## IFileTree Interface

The `IFileTree` interface (defined in `ifiletree.h`) provides a rich set of operations for working with file trees:

### Key Features

- **Navigation**: Methods to traverse the tree structure
- **Search**: Find files and directories by path or pattern
- **Modification**: Add, remove, or move files and directories
- **Merging**: Combine multiple trees with priority-based overrides
- **Lazy Loading**: Trees are populated on-demand to improve performance

### Important Methods

- `find(path, type)`: Find a file or directory by path
- `exists(path, type)`: Check if a file or directory exists
- `walk(callback)`: Traverse the entire tree, calling a function for each entry
- `addFile(path)`: Add a file to the tree
- `addDirectory(path)`: Add a directory to the tree
- `merge(source)`: Merge another tree into this one

### FileTreeEntry

The `FileTreeEntry` class represents an entry in a file tree, which can be either a file or a directory. Key methods include:

- `isFile()` / `isDir()`: Check if the entry is a file or directory
- `name()`: Get the name of the entry
- `path()`: Get the full path to the entry
- `astree()`: Convert the entry to a tree (if it's a directory)

## Concrete Implementations

### QDirFileTree

`QDirFileTree` represents a directory on the physical disk. It's defined in `qdirfiletree.h`.

#### Key Features

- Lazily populated: Only reads from disk when needed
- Read-only: Doesn't support mutable operations
- Can ignore specific files (like meta.ini in the root)

#### Usage

```cpp
// Create a tree representing a directory
auto tree = QDirFileTree::makeTree(QDir("C:/Games/Skyrim/Data"));

// Find a file
auto file = tree->find("meshes/actors/character/character.nif");

// Check if a directory exists
bool hasMeshes = tree->exists("meshes", IFileTree::DIRECTORY);
```

### ArchiveFileTree

`ArchiveFileTree` represents the contents of an archive file (BSA, BA2, ZIP, etc.). It's defined in `archivefiletree.h`.

#### Key Features

- Maps to an `Archive` object
- Can update the archive to reflect changes in the tree
- Can mark specific entries for extraction

#### Usage

```cpp
// Create a tree from an archive
auto tree = ArchiveFileTree::makeTree(archive);

// Mark files for extraction
ArchiveFileTree::mapToArchive(archive, selectedEntries);
```

### VirtualFileTree

`VirtualFileTree` represents MO2's virtual file system, which combines files from multiple mods according to their priority. It's defined in `virtualfiletree.h` and implemented in `virtualfiletree.cpp`.

#### Key Features

- Maps to MO2's internal `DirectoryEntry` structure
- Read-only: Doesn't support mutable operations
- Reflects the current state of the virtual file system

#### Implementation Details

The `VirtualFileTree` is implemented by the `VirtualFileTreeImpl` class, which:

1. Wraps a `DirectoryEntry` from MO2's internal directory structure
2. Populates the tree by converting `DirectoryEntry` and `FileEntry` objects to `FileTreeEntry` objects
3. Disables all mutable operations (beforeReplace, beforeInsert, beforeRemove)

#### Creation and Usage

The `VirtualFileTree` is created in `OrganizerCore` using a memoized lazy initialization:

```cpp
m_VirtualFileTree([this]() {
  return VirtualFileTree::makeTree(m_DirectoryStructure);
})
```

This means the tree is only created when needed and is cached until the directory structure changes.

The tree is exposed through the `virtualFileTree()` method in `OrganizerProxy`:

```cpp
std::shared_ptr<const MOBase::IFileTree> OrganizerProxy::virtualFileTree() const
{
  return m_Proxied->m_VirtualFileTree.value();
}
```

## Usage in MO2

### In OrganizerCore

The `OrganizerCore` class maintains the virtual file tree and makes it available to plugins:

```cpp
// Declaration in organizercore.h
MOBase::MemoizedLocked<std::shared_ptr<const MOBase::IFileTree>> m_VirtualFileTree;

// Initialization in organizercore.cpp constructor
m_VirtualFileTree([this]() {
  return VirtualFileTree::makeTree(m_DirectoryStructure);
})
```

The tree is invalidated when the directory structure changes:

```cpp
void OrganizerCore::onDirectoryRefreshed()
{
  // ...
  std::swap(m_DirectoryStructure, newStructure);
  m_VirtualFileTree.invalidate();
  // ...
}
```

### In Plugins

Plugins can access the virtual file tree through the `IOrganizer` interface:

```cpp
std::shared_ptr<const MOBase::IFileTree> virtualFileTree = organizer->virtualFileTree();
```

This allows plugins to navigate and search the virtual file system without having to understand the details of how it's implemented.

## Creating Your Own Tab with IFileTree

To create a custom tab in MO2 that uses the `IFileTree` interface, you would typically:

1. Create a plugin that implements the `IPluginTool` interface
2. Access the virtual file tree through the `IOrganizer` interface
3. Create a UI that displays and interacts with the file tree

### Example Plugin

```cpp
class FileTreeViewer : public MOBase::IPluginTool
{
public:
  // IPlugin interface
  QString name() const override { return "FileTreeViewer"; }
  QString author() const override { return "Your Name"; }
  QString description() const override { return "A tool to view the virtual file tree"; }
  MOBase::VersionInfo version() const override { return {1, 0, 0}; }
  
  // IPluginTool interface
  QString displayName() const override { return "File Tree Viewer"; }
  QString tooltip() const override { return "View the virtual file tree"; }
  QIcon icon() const override { return QIcon(); }
  
  bool init(MOBase::IOrganizer* organizer) override
  {
    m_Organizer = organizer;
    return true;
  }
  
  void display() const override
  {
    // Get the virtual file tree
    auto fileTree = m_Organizer->virtualFileTree();
    
    // Create and show a dialog to display the tree
    FileTreeDialog dialog(parentWidget(), fileTree);
    dialog.exec();
  }
  
private:
  MOBase::IOrganizer* m_Organizer;
};
```

### Example Dialog

```cpp
class FileTreeDialog : public QDialog
{
  Q_OBJECT
  
public:
  FileTreeDialog(QWidget* parent, std::shared_ptr<const MOBase::IFileTree> fileTree)
    : QDialog(parent), m_FileTree(fileTree)
  {
    setWindowTitle("File Tree Viewer");
    resize(800, 600);
    
    // Create UI
    QVBoxLayout* layout = new QVBoxLayout(this);
    m_TreeWidget = new QTreeWidget(this);
    m_TreeWidget->setHeaderLabels({"Name", "Type"});
    layout->addWidget(m_TreeWidget);
    
    // Populate the tree widget
    populateTreeWidget();
  }
  
private:
  void populateTreeWidget()
  {
    m_TreeWidget->clear();
    
    // Add root item
    QTreeWidgetItem* rootItem = new QTreeWidgetItem(m_TreeWidget, {"Data"});
    
    // Recursively populate the tree
    populateTreeWidgetItem(rootItem, m_FileTree);
    
    // Expand the root item
    rootItem->setExpanded(true);
  }
  
  void populateTreeWidgetItem(QTreeWidgetItem* item, std::shared_ptr<const MOBase::IFileTree> tree)
  {
    // Add all entries in the tree
    for (auto it = tree->begin(); it != tree->end(); ++it)
    {
      auto entry = *it;
      
      // Create a new item
      QTreeWidgetItem* childItem = new QTreeWidgetItem(item);
      childItem->setText(0, entry->name());
      childItem->setText(1, entry->isDir() ? "Directory" : "File");
      
      // If it's a directory, recursively populate it
      if (entry->isDir())
      {
        populateTreeWidgetItem(childItem, entry->astree());
      }
    }
  }
  
private:
  std::shared_ptr<const MOBase::IFileTree> m_FileTree;
  QTreeWidget* m_TreeWidget;
};
```

## Advanced Usage

### Combining Multiple Trees

You can create a custom view that combines files from both the filesystem and the virtual file system:

```cpp
// Create a tree for a physical directory
auto physicalTree = QDirFileTree::makeTree(QDir("C:/Games/Skyrim/Data"));

// Get the virtual file tree
auto virtualTree = organizer->virtualFileTree();

// Create a custom tree that combines both
auto combinedTree = createCombinedTree(physicalTree, virtualTree);

// Display the combined tree
displayTree(combinedTree);
```

### Filtering Files

You can filter files based on various criteria:

```cpp
// Find all texture files
auto textureFiles = fileTree->findFiles("textures", [](const QString& filename) {
  return filename.endsWith(".dds", Qt::CaseInsensitive);
});

// Display the texture files
displayFiles(textureFiles);
```

### Walking the Tree

You can traverse the entire tree and perform operations on each entry:

```cpp
fileTree->walk([](const QString& path, std::shared_ptr<const FileTreeEntry> entry) {
  if (entry->isFile() && entry->name().endsWith(".esp", Qt::CaseInsensitive)) {
    qDebug() << "Found plugin:" << path + entry->name();
  }
  return IFileTree::WalkReturn::CONTINUE;
});
```

### Getting File Origins

You can find out which mod a file comes from:

```cpp
QString fileName = "meshes/actors/character/character.nif";
QStringList origins = organizer->getFileOrigins(fileName);

qDebug() << "File" << fileName << "comes from:";
for (const QString& origin : origins) {
  qDebug() << "  " << origin;
}
