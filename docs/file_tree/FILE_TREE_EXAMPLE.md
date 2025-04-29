# MO2 File Tree Example Plugin

This document provides a complete example of a plugin that uses the IFileTree interface to show files from both the filesystem and virtual folders in Mod Organizer 2.

## Table of Contents

- [MO2 File Tree Example Plugin](#mo2-file-tree-example-plugin)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Plugin Structure](#plugin-structure)
  - [Implementation](#implementation)
    - [Plugin Class](#plugin-class)
    - [File Tree Dialog](#file-tree-dialog)
    - [Combined Tree Model](#combined-tree-model)
    - [File Origin Widget](#file-origin-widget)
  - [Building and Installation](#building-and-installation)
    - [CMakeLists.txt](#cmakeliststxt)
    - [filetreeviewer.json](#filetreeviewerjson)
  - [Usage](#usage)
  - [Advanced Features](#advanced-features)

## Overview

This example demonstrates how to create a plugin for Mod Organizer 2 that:

1. Shows files from both the physical filesystem and MO2's virtual file system
2. Allows browsing and searching the combined file tree
3. Displays information about file origins (which mod provides each file)
4. Highlights conflicts between files from different sources

## Plugin Structure

The plugin consists of the following components:

1. **FileTreeViewer**: The main plugin class that implements IPluginTool
2. **FileTreeDialog**: The main dialog that displays the combined file tree
3. **CombinedTreeModel**: A model that combines physical and virtual file trees
4. **FileOriginWidget**: A widget that displays information about file origins

## Implementation

### Plugin Class

```cpp
#include <iplugin.h>
#include <iplugintool.h>
#include <imoinfo.h>
#include <ifiletree.h>
#include <QDir>

class FileTreeViewer : public MOBase::IPluginTool
{
  Q_OBJECT
  Q_INTERFACES(MOBase::IPlugin MOBase::IPluginTool)
  Q_PLUGIN_METADATA(IID "org.example.FileTreeViewer" FILE "filetreeviewer.json")

public:
  FileTreeViewer();
  virtual ~FileTreeViewer();

  // IPlugin interface
  virtual bool init(MOBase::IOrganizer* organizer) override;
  virtual QString name() const override;
  virtual QString author() const override;
  virtual QString description() const override;
  virtual MOBase::VersionInfo version() const override;
  virtual QList<MOBase::PluginSetting> settings() const override;

  // IPluginTool interface
  virtual QString displayName() const override;
  virtual QString tooltip() const override;
  virtual QIcon icon() const override;
  virtual void display() const override;

private:
  MOBase::IOrganizer* m_Organizer;
};

FileTreeViewer::FileTreeViewer() : m_Organizer(nullptr)
{
}

FileTreeViewer::~FileTreeViewer()
{
}

bool FileTreeViewer::init(MOBase::IOrganizer* organizer)
{
  m_Organizer = organizer;
  return true;
}

QString FileTreeViewer::name() const
{
  return "FileTreeViewer";
}

QString FileTreeViewer::author() const
{
  return "Your Name";
}

QString FileTreeViewer::description() const
{
  return "A tool to view files from both the filesystem and virtual folders";
}

MOBase::VersionInfo FileTreeViewer::version() const
{
  return MOBase::VersionInfo(1, 0, 0);
}

QList<MOBase::PluginSetting> FileTreeViewer::settings() const
{
  return QList<MOBase::PluginSetting>();
}

QString FileTreeViewer::displayName() const
{
  return "File Tree Viewer";
}

QString FileTreeViewer::tooltip() const
{
  return "View files from both the filesystem and virtual folders";
}

QIcon FileTreeViewer::icon() const
{
  return QIcon();
}

void FileTreeViewer::display() const
{
  // Get the virtual file tree
  auto virtualTree = m_Organizer->virtualFileTree();
  
  // Create a tree for the physical data directory
  auto gamePlugin = m_Organizer->managedGame();
  auto physicalTree = QDirFileTree::makeTree(gamePlugin->dataDirectory());
  
  // Create and show the dialog
  FileTreeDialog dialog(parentWidget(), m_Organizer, physicalTree, virtualTree);
  dialog.exec();
}
```

### File Tree Dialog

```cpp
#include <QDialog>
#include <QTreeView>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSplitter>
#include <QLabel>
#include <QComboBox>
#include <QCheckBox>
#include <QTabWidget>
#include <QFileInfo>
#include <QMessageBox>

class FileTreeDialog : public QDialog
{
  Q_OBJECT

public:
  FileTreeDialog(QWidget* parent, MOBase::IOrganizer* organizer,
                 std::shared_ptr<const MOBase::IFileTree> physicalTree,
                 std::shared_ptr<const MOBase::IFileTree> virtualTree);
  
private slots:
  void onItemSelected(const QModelIndex& index);
  void onSearch();
  void onFilterChanged(int index);
  void onShowConflictsToggled(bool checked);
  
private:
  void setupUI();
  void populateFilterComboBox();
  
  MOBase::IOrganizer* m_Organizer;
  std::shared_ptr<const MOBase::IFileTree> m_PhysicalTree;
  std::shared_ptr<const MOBase::IFileTree> m_VirtualTree;
  
  QTreeView* m_TreeView;
  QLineEdit* m_SearchEdit;
  QPushButton* m_SearchButton;
  QComboBox* m_FilterComboBox;
  QCheckBox* m_ShowConflictsCheckBox;
  QTabWidget* m_InfoTabWidget;
  FileOriginWidget* m_OriginWidget;
  CombinedTreeModel* m_TreeModel;
};

FileTreeDialog::FileTreeDialog(QWidget* parent, MOBase::IOrganizer* organizer,
                               std::shared_ptr<const MOBase::IFileTree> physicalTree,
                               std::shared_ptr<const MOBase::IFileTree> virtualTree)
  : QDialog(parent),
    m_Organizer(organizer),
    m_PhysicalTree(physicalTree),
    m_VirtualTree(virtualTree)
{
  setupUI();
  
  // Create the model
  m_TreeModel = new CombinedTreeModel(m_PhysicalTree, m_VirtualTree, this);
  m_TreeView->setModel(m_TreeModel);
  
  // Connect signals
  connect(m_TreeView->selectionModel(), &QItemSelectionModel::currentChanged,
          this, &FileTreeDialog::onItemSelected);
  connect(m_SearchButton, &QPushButton::clicked, this, &FileTreeDialog::onSearch);
  connect(m_FilterComboBox, QOverload<int>::of(&QComboBox::currentIndexChanged),
          this, &FileTreeDialog::onFilterChanged);
  connect(m_ShowConflictsCheckBox, &QCheckBox::toggled,
          this, &FileTreeDialog::onShowConflictsToggled);
  
  // Populate the filter combo box
  populateFilterComboBox();
}

void FileTreeDialog::setupUI()
{
  setWindowTitle("File Tree Viewer");
  resize(1000, 700);
  
  QVBoxLayout* mainLayout = new QVBoxLayout(this);
  
  // Search and filter controls
  QHBoxLayout* controlsLayout = new QHBoxLayout();
  
  QLabel* searchLabel = new QLabel("Search:", this);
  controlsLayout->addWidget(searchLabel);
  
  m_SearchEdit = new QLineEdit(this);
  controlsLayout->addWidget(m_SearchEdit);
  
  m_SearchButton = new QPushButton("Search", this);
  controlsLayout->addWidget(m_SearchButton);
  
  controlsLayout->addSpacing(20);
  
  QLabel* filterLabel = new QLabel("Filter:", this);
  controlsLayout->addWidget(filterLabel);
  
  m_FilterComboBox = new QComboBox(this);
  controlsLayout->addWidget(m_FilterComboBox);
  
  controlsLayout->addSpacing(20);
  
  m_ShowConflictsCheckBox = new QCheckBox("Show Conflicts Only", this);
  controlsLayout->addWidget(m_ShowConflictsCheckBox);
  
  controlsLayout->addStretch();
  
  mainLayout->addLayout(controlsLayout);
  
  // Splitter for tree view and info panel
  QSplitter* splitter = new QSplitter(Qt::Horizontal, this);
  
  // Tree view
  m_TreeView = new QTreeView(this);
  m_TreeView->setHeaderHidden(false);
  m_TreeView->setAlternatingRowColors(true);
  m_TreeView->setSortingEnabled(true);
  splitter->addWidget(m_TreeView);
  
  // Info panel
  m_InfoTabWidget = new QTabWidget(this);
  
  // Origin tab
  m_OriginWidget = new FileOriginWidget(m_Organizer, this);
  m_InfoTabWidget->addTab(m_OriginWidget, "Origins");
  
  // Add more tabs as needed
  
  splitter->addWidget(m_InfoTabWidget);
  splitter->setStretchFactor(0, 3);
  splitter->setStretchFactor(1, 1);
  
  mainLayout->addWidget(splitter);
  
  // Button box
  QDialogButtonBox* buttonBox = new QDialogButtonBox(QDialogButtonBox::Close, this);
  connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::reject);
  mainLayout->addWidget(buttonBox);
}

void FileTreeDialog::populateFilterComboBox()
{
  m_FilterComboBox->addItem("All Files", "");
  m_FilterComboBox->addItem("Meshes", "nif");
  m_FilterComboBox->addItem("Textures", "dds");
  m_FilterComboBox->addItem("Scripts", "pex");
  m_FilterComboBox->addItem("Plugins", "esp,esm,esl");
  m_FilterComboBox->addItem("Archives", "bsa,ba2");
}

void FileTreeDialog::onItemSelected(const QModelIndex& index)
{
  if (!index.isValid())
    return;
  
  // Get the file path from the model
  QString path = m_TreeModel->getFilePath(index);
  
  // Update the origin widget
  m_OriginWidget->setFile(path);
}

void FileTreeDialog::onSearch()
{
  QString searchText = m_SearchEdit->text();
  if (searchText.isEmpty())
    return;
  
  // Apply the search filter to the model
  m_TreeModel->setSearchFilter(searchText);
}

void FileTreeDialog::onFilterChanged(int index)
{
  QString filter = m_FilterComboBox->itemData(index).toString();
  
  // Apply the file extension filter to the model
  m_TreeModel->setExtensionFilter(filter.split(","));
}

void FileTreeDialog::onShowConflictsToggled(bool checked)
{
  // Show only conflicting files
  m_TreeModel->setShowOnlyConflicts(checked);
}
```

### Combined Tree Model

```cpp
#include <QAbstractItemModel>
#include <QFileIconProvider>
#include <QFont>
#include <QColor>
#include <QIcon>
#include <QSet>
#include <QMap>

class TreeItem
{
public:
  TreeItem(const QString& name, bool isDir, TreeItem* parent = nullptr);
  ~TreeItem();
  
  void appendChild(TreeItem* child);
  TreeItem* child(int row);
  int childCount() const;
  int columnCount() const;
  QVariant data(int column) const;
  int row() const;
  TreeItem* parent();
  
  QString name() const { return m_Name; }
  bool isDir() const { return m_IsDir; }
  
  void setVirtualEntry(std::shared_ptr<const MOBase::FileTreeEntry> entry) { m_VirtualEntry = entry; }
  void setPhysicalEntry(std::shared_ptr<const MOBase::FileTreeEntry> entry) { m_PhysicalEntry = entry; }
  
  std::shared_ptr<const MOBase::FileTreeEntry> virtualEntry() const { return m_VirtualEntry; }
  std::shared_ptr<const MOBase::FileTreeEntry> physicalEntry() const { return m_PhysicalEntry; }
  
  bool hasConflict() const { return m_VirtualEntry && m_PhysicalEntry; }
  
private:
  QString m_Name;
  bool m_IsDir;
  TreeItem* m_Parent;
  QList<TreeItem*> m_Children;
  std::shared_ptr<const MOBase::FileTreeEntry> m_VirtualEntry;
  std::shared_ptr<const MOBase::FileTreeEntry> m_PhysicalEntry;
};

class CombinedTreeModel : public QAbstractItemModel
{
  Q_OBJECT
  
public:
  CombinedTreeModel(std::shared_ptr<const MOBase::IFileTree> physicalTree,
                    std::shared_ptr<const MOBase::IFileTree> virtualTree,
                    QObject* parent = nullptr);
  ~CombinedTreeModel();
  
  // QAbstractItemModel interface
  QModelIndex index(int row, int column, const QModelIndex& parent = QModelIndex()) const override;
  QModelIndex parent(const QModelIndex& index) const override;
  int rowCount(const QModelIndex& parent = QModelIndex()) const override;
  int columnCount(const QModelIndex& parent = QModelIndex()) const override;
  QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
  QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;
  
  // Custom methods
  QString getFilePath(const QModelIndex& index) const;
  void setSearchFilter(const QString& filter);
  void setExtensionFilter(const QStringList& extensions);
  void setShowOnlyConflicts(bool showOnlyConflicts);
  
private:
  void buildTree();
  void addToTree(TreeItem* parent, std::shared_ptr<const MOBase::IFileTree> tree, bool isVirtual);
  bool matchesFilter(TreeItem* item) const;
  
  TreeItem* m_RootItem;
  std::shared_ptr<const MOBase::IFileTree> m_PhysicalTree;
  std::shared_ptr<const MOBase::IFileTree> m_VirtualTree;
  QFileIconProvider m_IconProvider;
  
  QString m_SearchFilter;
  QStringList m_ExtensionFilter;
  bool m_ShowOnlyConflicts;
};

CombinedTreeModel::CombinedTreeModel(std::shared_ptr<const MOBase::IFileTree> physicalTree,
                                     std::shared_ptr<const MOBase::IFileTree> virtualTree,
                                     QObject* parent)
  : QAbstractItemModel(parent),
    m_PhysicalTree(physicalTree),
    m_VirtualTree(virtualTree),
    m_ShowOnlyConflicts(false)
{
  m_RootItem = new TreeItem("Data", true);
  buildTree();
}

CombinedTreeModel::~CombinedTreeModel()
{
  delete m_RootItem;
}

void CombinedTreeModel::buildTree()
{
  // Add physical tree entries
  addToTree(m_RootItem, m_PhysicalTree, false);
  
  // Add virtual tree entries
  addToTree(m_RootItem, m_VirtualTree, true);
}

void CombinedTreeModel::addToTree(TreeItem* parent, std::shared_ptr<const MOBase::IFileTree> tree, bool isVirtual)
{
  for (auto it = tree->begin(); it != tree->end(); ++it)
  {
    auto entry = *it;
    QString name = entry->name();
    
    // Find or create the item
    TreeItem* item = nullptr;
    for (int i = 0; i < parent->childCount(); ++i)
    {
      if (parent->child(i)->name().compare(name, Qt::CaseInsensitive) == 0)
      {
        item = parent->child(i);
        break;
      }
    }
    
    if (!item)
    {
      item = new TreeItem(name, entry->isDir(), parent);
      parent->appendChild(item);
    }
    
    // Set the entry
    if (isVirtual)
      item->setVirtualEntry(entry);
    else
      item->setPhysicalEntry(entry);
    
    // Recurse into directories
    if (entry->isDir())
    {
      addToTree(item, entry->astree(), isVirtual);
    }
  }
}

QModelIndex CombinedTreeModel::index(int row, int column, const QModelIndex& parent) const
{
  if (!hasIndex(row, column, parent))
    return QModelIndex();
  
  TreeItem* parentItem;
  
  if (!parent.isValid())
    parentItem = m_RootItem;
  else
    parentItem = static_cast<TreeItem*>(parent.internalPointer());
  
  TreeItem* childItem = parentItem->child(row);
  if (childItem)
    return createIndex(row, column, childItem);
  else
    return QModelIndex();
}

QModelIndex CombinedTreeModel::parent(const QModelIndex& index) const
{
  if (!index.isValid())
    return QModelIndex();
  
  TreeItem* childItem = static_cast<TreeItem*>(index.internalPointer());
  TreeItem* parentItem = childItem->parent();
  
  if (parentItem == m_RootItem)
    return QModelIndex();
  
  return createIndex(parentItem->row(), 0, parentItem);
}

int CombinedTreeModel::rowCount(const QModelIndex& parent) const
{
  TreeItem* parentItem;
  if (parent.column() > 0)
    return 0;
  
  if (!parent.isValid())
    parentItem = m_RootItem;
  else
    parentItem = static_cast<TreeItem*>(parent.internalPointer());
  
  return parentItem->childCount();
}

int CombinedTreeModel::columnCount(const QModelIndex& parent) const
{
  return 3; // Name, Type, Source
}

QVariant CombinedTreeModel::data(const QModelIndex& index, int role) const
{
  if (!index.isValid())
    return QVariant();
  
  TreeItem* item = static_cast<TreeItem*>(index.internalPointer());
  
  if (role == Qt::DisplayRole)
  {
    switch (index.column())
    {
    case 0: // Name
      return item->name();
    case 1: // Type
      return item->isDir() ? "Directory" : "File";
    case 2: // Source
      if (item->virtualEntry() && item->physicalEntry())
        return "Both (Conflict)";
      else if (item->virtualEntry())
        return "Virtual";
      else if (item->physicalEntry())
        return "Physical";
      else
        return "Unknown";
    }
  }
  else if (role == Qt::DecorationRole && index.column() == 0)
  {
    if (item->isDir())
      return m_IconProvider.icon(QFileIconProvider::Folder);
    else
      return m_IconProvider.icon(QFileIconProvider::File);
  }
  else if (role == Qt::FontRole)
  {
    if (item->hasConflict())
    {
      QFont font;
      font.setBold(true);
      return font;
    }
  }
  else if (role == Qt::BackgroundRole)
  {
    if (item->hasConflict())
      return QColor(255, 200, 200); // Light red for conflicts
  }
  
  return QVariant();
}

QVariant CombinedTreeModel::headerData(int section, Qt::Orientation orientation, int role) const
{
  if (orientation == Qt::Horizontal && role == Qt::DisplayRole)
  {
    switch (section)
    {
    case 0:
      return "Name";
    case 1:
      return "Type";
    case 2:
      return "Source";
    }
  }
  
  return QVariant();
}

QString CombinedTreeModel::getFilePath(const QModelIndex& index) const
{
  if (!index.isValid())
    return QString();
  
  TreeItem* item = static_cast<TreeItem*>(index.internalPointer());
  
  // Build the path by walking up the tree
  QString path;
  TreeItem* current = item;
  while (current && current != m_RootItem)
  {
    path = current->name() + (path.isEmpty() ? "" : "/" + path);
    current = current->parent();
  }
  
  return path;
}

void CombinedTreeModel::setSearchFilter(const QString& filter)
{
  beginResetModel();
  m_SearchFilter = filter;
  endResetModel();
}

void CombinedTreeModel::setExtensionFilter(const QStringList& extensions)
{
  beginResetModel();
  m_ExtensionFilter = extensions;
  endResetModel();
}

void CombinedTreeModel::setShowOnlyConflicts(bool showOnlyConflicts)
{
  beginResetModel();
  m_ShowOnlyConflicts = showOnlyConflicts;
  endResetModel();
}

bool CombinedTreeModel::matchesFilter(TreeItem* item) const
{
  // If showing only conflicts, check for conflict
  if (m_ShowOnlyConflicts && !item->hasConflict())
    return false;
  
  // If search filter is active, check name
  if (!m_SearchFilter.isEmpty() && !item->name().contains(m_SearchFilter, Qt::CaseInsensitive))
    return false;
  
  // If extension filter is active, check extension
  if (!m_ExtensionFilter.isEmpty() && !item->isDir())
  {
    QFileInfo fileInfo(item->name());
    QString suffix = fileInfo.suffix().toLower();
    if (!m_ExtensionFilter.contains(suffix))
      return false;
  }
  
  return true;
}
```

### File Origin Widget

```cpp
#include <QWidget>
#include <QVBoxLayout>
#include <QTableWidget>
#include <QLabel>
#include <QHeaderView>

class FileOriginWidget : public QWidget
{
  Q_OBJECT
  
public:
  FileOriginWidget(MOBase::IOrganizer* organizer, QWidget* parent = nullptr);
  
  void setFile(const QString& filePath);
  
private:
  void setupUI();
  void updateOrigins(const QString& filePath);
  
  MOBase::IOrganizer* m_Organizer;
  QLabel* m_FilePathLabel;
  QTableWidget* m_OriginsTable;
};

FileOriginWidget::FileOriginWidget(MOBase::IOrganizer* organizer, QWidget* parent)
  : QWidget(parent),
    m_Organizer(organizer)
{
  setupUI();
}

void FileOriginWidget::setupUI()
{
  QVBoxLayout* layout = new QVBoxLayout(this);
  
  m_FilePathLabel = new QLabel(this);
  m_FilePathLabel->setWordWrap(true);
  layout->addWidget(m_FilePathLabel);
  
  m_OriginsTable = new QTableWidget(this);
  m_OriginsTable->setColumnCount(2);
  m_OriginsTable->setHorizontalHeaderLabels({"Origin", "Priority"});
  m_OriginsTable->horizontalHeader()->setStretchLastSection(true);
  m_OriginsTable->verticalHeader()->setVisible(false);
  m_OriginsTable->setAlternatingRowColors(true);
  m_OriginsTable->setSelectionBehavior(QAbstractItemView::SelectRows);
  layout->addWidget(m_OriginsTable);
}

void FileOriginWidget::setFile(const QString& filePath)
{
  m_FilePathLabel->setText("File: " + filePath);
  updateOrigins(filePath);
}

void FileOriginWidget::updateOrigins(const QString& filePath)
{
  m_OriginsTable->clearContents();
  
  QStringList origins = m_Organizer->getFileOrigins(filePath);
  
  m_OriginsTable->setRowCount(origins.size());
  
  for (int i = 0; i < origins.size(); ++i)
  {
    QString origin = origins[i];
    
    // Origin name
    QTableWidgetItem* nameItem = new QTableWidgetItem(origin);
    m_OriginsTable->setItem(i, 0, nameItem);
    
    // Priority
    int priority = -1;
    if (origin != "base")
    {
      for (int j = 0; j < m_Organizer->modList()->size(); ++j)
      {
        if (m_Organizer->modList()->name(j) == origin)
        {
          priority = m_Organizer->modList()->priority(j);
          break;
        }
      }
    }
    
    QTableWidgetItem* priorityItem = new QTableWidgetItem(priority >= 0 ? QString::number(priority) : "N/A");
    m_OriginsTable->setItem(i, 1, priorityItem);
  }
  
  m_OriginsTable->resizeColumnsToContents();
}
```

## Building and Installation

To build the plugin, you'll need:

1. Qt 5.x development libraries
2. Mod Organizer 2 development files
3. CMake 3.x or later

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)
project(FileTreeViewer)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

# Set the path to MO2 development files
set(MO2_ROOT "C:/Path/To/MO2/Development/Files")

include_directories(
    ${MO2_ROOT}/uibase/include
)

add_library(FileTreeViewer SHARED
    src/filetreeviewer.cpp
    src/filetreedialog.cpp
    src/combinedtreemodel.cpp
    src/fileoriginwidget.cpp
    src/filetreeviewer.json
)

target_link_libraries(FileTreeViewer
    Qt5::Widgets
    ${MO2_ROOT}/uibase/lib/uibase.lib
)

install(TARGETS FileTreeViewer
    RUNTIME DESTINATION bin/plugins
)
```

### filetreeviewer.json

```json
{
  "name": "File Tree Viewer",
  "author": "Your Name",
  "version": "1.0.0",
  "description": "A tool to view files from both the filesystem and virtual folders"
}
```

## Usage

After building and installing the plugin:

1. Start Mod Organizer 2
2. The plugin will appear in the toolbar as "File Tree Viewer"
3. Click the button to open the file tree dialog
4. Browse the combined file tree
5. Use the search and filter controls to find specific files
6. Select a file to view its origins
7. Check "Show Conflicts Only" to focus on files that exist in both the physical and virtual file systems

## Advanced Features

Here are some additional features you could add to the plugin:

1. **File Preview**: Add a preview tab that shows the content of selected files
2. **Conflict Resolution**: Add buttons to resolve conflicts by copying files between sources
3. **File Comparison**: Add a diff viewer to compare conflicting files
4. **Export**: Add the ability to export the file tree or search results
5. **Bookmarks**: Allow users to bookmark frequently accessed files or directories
6. **Custom Filters**: Allow users to create and save custom file filters
7. **Context Menu**: Add a context menu with actions like "Open in Explorer", "Copy Path", etc.
8. **Drag and Drop**: Allow dragging files from the tree to other applications
