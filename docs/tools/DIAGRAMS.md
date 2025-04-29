# Mod Organizer 2 Tool Plugins Diagrams

This document provides visual diagrams of the classes and their relationships in the Mod Organizer 2 tool plugins, specifically the INI Editor and FNIS tool plugins.

## Table of Contents

- [Mod Organizer 2 Tool Plugins Diagrams](#mod-organizer-2-tool-plugins-diagrams)
  - [Table of Contents](#table-of-contents)
  - [Plugin Interface Hierarchy](#plugin-interface-hierarchy)
  - [INI Editor Plugin Structure](#ini-editor-plugin-structure)
  - [FNIS Tool Plugin Structure](#fnis-tool-plugin-structure)
  - [Tool Plugin Integration with Mod Organizer 2](#tool-plugin-integration-with-mod-organizer-2)
  - [Tool Plugin Workflow](#tool-plugin-workflow)

## Plugin Interface Hierarchy

The following diagram shows the inheritance hierarchy of the plugin interfaces in Mod Organizer 2:

```mermaid
classDiagram
    IPlugin <|-- IPluginTool
    
    class IPlugin {
        +init(IOrganizer* moInfo)
        +name() const
        +author() const
        +description() const
        +version() const
        +settings() const
    }
    
    class IPluginTool {
        +displayName() const
        +localizedName() const
        +tooltip() const
        +icon() const
        +setParentWidget(QWidget* widget)
        +display() const
        #parentWidget() const
        -m_ParentWidget: QWidget*
    }
```

## INI Editor Plugin Structure

The following diagram shows the structure of the INI Editor plugin:

```mermaid
classDiagram
    IPluginTool <|-- IniEditor
    IniEditor --> TextViewer: uses
    
    class IniEditor {
        +init(IOrganizer* moInfo)
        +name() const
        +localizedName() const
        +author() const
        +description() const
        +version() const
        +settings() const
        +displayName() const
        +tooltip() const
        +icon() const
        +display() const
        -m_MOInfo: IOrganizer*
    }
    
    class TextViewer {
        +TextViewer(const QString& title, QWidget* parent)
        +setDescription(const QString& description)
        +addFile(const QString& fileName, bool writable)
        -m_EditorTabs: QTabWidget*
        -m_Modified: std::set<QTextEdit*>
        -m_FindDialog: FindDialog*
        -m_FindPattern: QString
    }
```

## FNIS Tool Plugin Structure

The following diagram shows the structure of the FNIS tool plugin:

```mermaid
classDiagram
    IPluginTool <|-- FNISTool
    IPluginTool <|-- FNISToolReset
    IPluginTool <|-- FNISPatches
    FNISToolReset --> FNISTool: references
    FNISPatches --> FNISTool: references
    
    class FNISTool {
        +init(IOrganizer* organizer)
        +name()
        +localizedName()
        +author()
        +description()
        +version()
        +requirements()
        +settings()
        +displayName()
        +tooltip()
        +icon()
        +setParentWidget(widget)
        +display()
        -__organizer: IOrganizer
        -__parentWidget: QWidget
        -__getRedirectOutput()
        -__getRedirectLogs()
        -__getOutputPath()
        -__getLogOutputPath()
        -__getFNISPath()
        -__getModDirectory()
        -__withinDirectory(innerPath, outerDir)
    }
    
    class FNISToolReset {
        +init(IOrganizer* organizer)
        +name()
        +localizedName()
        +author()
        +description()
        +version()
        +master()
        +settings()
        +displayName()
        +tooltip()
        +icon()
        +setParentWidget(widget)
        +display()
        -__organizer: IOrganizer
        -__parentWidget: QWidget
        -__mainToolName()
    }
    
    class FNISPatches {
        +init(IOrganizer* organizer)
        +name()
        +localizedName()
        +author()
        +description()
        +version()
        +master()
        +settings()
        +displayName()
        +tooltip()
        +icon()
        +setParentWidget(widget)
        +display()
        -__organizer: IOrganizer
        -__parentWidget: QWidget
        -__mainToolName()
        -__getFNISPath()
        -__getModDirectory()
        -__withinDirectory(innerPath, outerDir)
        -__loadEnabledPatches()
        -__saveEnabledPatches(enabledPatches)
        -__loadAvailablePatches()
    }
```

## Tool Plugin Integration with Mod Organizer 2

The following diagram shows how tool plugins integrate with Mod Organizer 2:

```mermaid
flowchart TD
    subgraph ModOrganizer2[Mod Organizer 2]
        IOrganizer
        PluginSystem
        ToolsMenu
    end
    
    subgraph INIEditorPlugin[INI Editor Plugin]
        IniEditor
        TextViewer
    end
    
    subgraph FNISToolPlugin[FNIS Tool Plugin]
        FNISTool
        FNISToolReset
        FNISPatches
    end
    
    PluginSystem --- IniEditor
    PluginSystem --- FNISTool
    PluginSystem --- FNISToolReset
    PluginSystem --- FNISPatches
    
    IOrganizer --- IniEditor
    IOrganizer --- FNISTool
    IOrganizer --- FNISToolReset
    IOrganizer --- FNISPatches
    
    ToolsMenu --- IniEditor
    ToolsMenu --- FNISTool
    FNISTool --- FNISToolReset
    FNISTool --- FNISPatches
```

## Tool Plugin Workflow

The following sequence diagram shows the typical workflow of a tool plugin:

```mermaid
sequenceDiagram
    participant User
    participant MO2 as Mod Organizer 2
    participant Tool as Tool Plugin
    participant UI as UI Components
    
    User->>MO2: Start Mod Organizer 2
    MO2->>Tool: Load plugin
    Tool->>MO2: Register with plugin system
    
    User->>MO2: Click on tool in menu
    MO2->>Tool: Call display() method
    
    alt INI Editor
        Tool->>UI: Create TextViewer
        UI->>Tool: Return TextViewer instance
        Tool->>UI: Add INI files to TextViewer
        UI->>User: Show TextViewer dialog
        User->>UI: Edit INI files
        UI->>Tool: Save changes
        Tool->>MO2: Update INI files
    else FNIS Tool
        Tool->>MO2: Get FNIS path
        MO2->>Tool: Return FNIS path
        Tool->>MO2: Get output settings
        MO2->>Tool: Return output settings
        Tool->>MO2: Run FNIS
        MO2->>Tool: Return FNIS result
        Tool->>User: Show result message
    end
```

These diagrams should help visualize the structure and relationships of the tool plugins in Mod Organizer 2.
