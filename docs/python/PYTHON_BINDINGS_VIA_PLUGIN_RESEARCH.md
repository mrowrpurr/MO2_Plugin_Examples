# Extending Python API via C++ Plugins in Mod Organizer 2

## Table of Contents

- [Extending Python API via C++ Plugins in Mod Organizer 2](#extending-python-api-via-c-plugins-in-mod-organizer-2)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Architecture Overview](#architecture-overview)
    - [Python Proxy Plugin](#python-proxy-plugin)
    - [Python Runner](#python-runner)
    - [Python Bindings (mobase)](#python-bindings-mobase)
  - [Can C++ Plugins Extend the Python API?](#can-c-plugins-extend-the-python-api)
    - [Official Approach](#official-approach)
    - [Technical Challenges](#technical-challenges)
    - [Potential Solutions](#potential-solutions)
  - [Alternative Approaches](#alternative-approaches)
    - [Inter-Plugin Communication](#inter-plugin-communication)
      - [Understanding Q\_INVOKABLE and Its Limitations](#understanding-q_invokable-and-its-limitations)
      - [Conclusion on Inter-Plugin Communication](#conclusion-on-inter-plugin-communication)
      - [Potential Use Cases (If Possible)](#potential-use-cases-if-possible)
      - [Advantages and Disadvantages](#advantages-and-disadvantages)
      - [More Reliable Alternative: Shared Data Approach](#more-reliable-alternative-shared-data-approach)
    - [Python Wrapper for C++ Plugin](#python-wrapper-for-c-plugin)
    - [Embedding Lua or JavaScript](#embedding-lua-or-javascript)
  - [Conclusion](#conclusion)

## Introduction

This document explores the possibility of extending the Python API for Mod Organizer 2 (MO2) through C++ plugins. The goal is to determine whether it's possible for a C++ plugin to expose additional functionality to Python plugins, and if so, how this might be accomplished.

## Architecture Overview

Before diving into the specifics, it's important to understand the architecture of the Python integration in MO2.

### Python Proxy Plugin

The Python proxy plugin (`ProxyPython`) is a C++ plugin that interfaces with MO2. It's responsible for:

1. Loading the Python runner library
2. Initializing the Python interpreter
3. Discovering Python plugins
4. Loading and unloading Python plugins

The proxy plugin is implemented in `proxypython.cpp` and `proxypython.h`. It implements the `IPluginProxy` interface, which allows it to load plugins from non-C++ sources.

Key points from the code:
- The proxy plugin loads the Python runner library dynamically
- It initializes the Python interpreter with specific paths
- It discovers Python plugins by looking for `.py` files or directories with `__init__.py` files
- It loads Python plugins by calling `createPlugin()` or `createPlugins()` functions

### Python Runner

The Python runner (`PythonRunner`) is responsible for:

1. Managing the Python interpreter
2. Loading and unloading Python plugins
3. Extracting plugin interfaces from Python objects

The runner is implemented in `pythonrunner.cpp` and `pythonrunner.h`. It uses pybind11 to interface with the Python interpreter.

Key points from the code:
- The runner initializes the Python interpreter only once for the lifetime of the program
- It loads Python plugins by evaluating Python files or importing Python modules
- It extracts plugin interfaces from Python objects using the `extract_plugins` function
- It manages the lifetime of Python objects to ensure they're not garbage collected while in use

### Python Bindings (mobase)

The Python bindings (`mobase`) provide access to the MO2 API from Python. They're implemented using pybind11 and are organized into several files under the `mobase` directory.

Key points from the code:
- The bindings are organized into several files based on functionality
- They use pybind11 to expose C++ classes and functions to Python
- They include trampoline classes to allow Python classes to override C++ virtual methods
- They handle conversion between C++ and Python types

## Can C++ Plugins Extend the Python API?

Based on the analysis of the code, there is no official or straightforward way for a C++ plugin to extend the Python API. However, there are some potential approaches that could be explored.

### Official Approach

There is no official mechanism for C++ plugins to extend the Python API. The Python proxy plugin and runner are designed to load Python plugins, not to allow C++ plugins to extend the Python API.

The `mobase` module is built as part of the Python proxy plugin, and its contents are defined at compile time. There's no mechanism for dynamically adding new bindings at runtime.

### Technical Challenges

Several technical challenges make it difficult to extend the Python API from a C++ plugin:

1. **Access to the Python Interpreter**: The Python interpreter is managed by the Python runner, which is loaded by the Python proxy plugin. A C++ plugin would need to somehow get access to this interpreter.

2. **Timing of Initialization**: The Python interpreter is initialized when the Python proxy plugin is loaded. A C++ plugin would need to register its bindings before any Python plugins are loaded, which might be difficult to guarantee.

3. **Extending the `mobase` Module**: The `mobase` module is created during the initialization of the Python interpreter. A C++ plugin would need to modify this module to add new bindings, which is not straightforward.

4. **Build System Integration**: The Python bindings are built using pybind11, which requires compile-time knowledge of the C++ types being exposed. A C++ plugin would need to use the same build system and pybind11 version to ensure compatibility.

### Potential Solutions

Despite these challenges, there are some potential approaches that could be explored:

1. **Accessing the Python Interpreter**: The Python interpreter is a global resource, so it might be possible to access it using the Python C API. However, this would require careful coordination with the Python proxy plugin to ensure that the interpreter is initialized before attempting to access it.

2. **Creating a New Module**: Instead of extending the `mobase` module, a C++ plugin could create a new Python module that exposes its functionality. This would avoid the need to modify the existing `mobase` module.

3. **Using the Python C API**: A C++ plugin could use the Python C API to create new Python objects and functions at runtime. This would allow it to extend the Python API without needing to modify the `mobase` module.

4. **Monkey Patching**: A C++ plugin could provide a Python module that monkey patches the `mobase` module to add new functionality. This would require the Python plugin to import this module explicitly.

## Alternative Approaches

Given the challenges of extending the Python API directly from a C++ plugin, there are several alternative approaches that might be more practical.

### Inter-Plugin Communication

Instead of trying to extend the Python API, a C++ plugin could expose its functionality through MO2's plugin system, and Python plugins could interact with it through that interface.

This approach would involve:

1. The C++ plugin implementing one of the MO2 plugin interfaces (e.g., `IPluginTool`)
2. The C++ plugin exposing its functionality through methods on that interface
3. Python plugins accessing the C++ plugin through the MO2 organizer interface

#### Understanding Q_INVOKABLE and Its Limitations

After examining the MO2 codebase, I've found that there isn't a direct `plugin()` method exposed in the C++ IOrganizer interface, and I couldn't find clear examples of Python plugins accessing C++ plugins directly. 

It's important to understand the role of `Q_INVOKABLE` in this context:

**What Q_INVOKABLE Does**:
- `Q_INVOKABLE` is a Qt macro that marks a method in a QObject-derived class as invokable through Qt's meta-object system
- It allows methods to be called dynamically at runtime using Qt's meta-object system
- It's primarily used for Qt's signals and slots mechanism, QML integration, and Qt's property system

**Q_INVOKABLE and Python**:
- In PyQt or PySide (Qt bindings for Python), methods marked with `Q_INVOKABLE` are automatically exposed to Python
- However, MO2 uses pybind11 for its Python bindings, not PyQt/PySide
- pybind11 doesn't use Qt's meta-object system for binding C++ to Python
- Instead, pybind11 generates Python bindings at compile time using template metaprogramming
- Methods need to be explicitly exposed in the pybind11 bindings to be callable from Python

This means that simply marking a method with `Q_INVOKABLE` in a C++ plugin doesn't automatically make it callable from Python in MO2. The method would need to be explicitly exposed in the pybind11 bindings, which would require modifying the MO2 core.

The approach described below is theoretical and would not work as described:

1. **Create a C++ Plugin with Extended Interface**:
   ```cpp
   // MyPluginTool.h
   class MyPluginTool : public QObject, public MOBase::IPluginTool {
       Q_OBJECT
       Q_INTERFACES(MOBase::IPlugin MOBase::IPluginTool)
       
   public:
       // Standard IPluginTool interface methods
       bool init(MOBase::IOrganizer* organizer) override;
       QString name() const override;
       QString displayName() const override;
       // ... other required methods ...
       
       // These methods would NOT be automatically accessible from Python
       // despite being marked with Q_INVOKABLE
       Q_INVOKABLE QString processText(const QString& input);
       Q_INVOKABLE QStringList getAvailableOptions();
       Q_INVOKABLE bool executeSpecialFunction(const QString& functionName, const QVariantMap& params);
   };
   ```

2. **Register Your Plugin with MO2**:
   ```cpp
   // plugin.cpp
   extern "C" DLLEXPORT QList<MOBase::IPlugin*> createPlugins() {
       return QList<MOBase::IPlugin*>() << new MyPluginTool();
   }
   ```

3. **Why This Approach Doesn't Work**:

   Even if you could somehow get a reference to your C++ plugin from Python:

   a. The methods marked with `Q_INVOKABLE` would not be accessible from Python because:
   - MO2's Python bindings use pybind11, not PyQt/PySide
   - pybind11 doesn't use Qt's meta-object system for binding
   - The methods would need to be explicitly exposed in the pybind11 bindings

   b. There doesn't appear to be a direct way for Python plugins to access other plugin instances:
   - The hypothetical `organizer.plugin("MyPluginTool")` method doesn't exist in the C++ API
   - The `pluginList()` method returns an `IPluginList` interface that doesn't provide access to plugin objects, only information about them

#### Conclusion on Inter-Plugin Communication

Based on my examination of the MO2 codebase and understanding of how pybind11 works, direct inter-plugin communication between Python and C++ plugins is not possible with the current MO2 architecture without modifying the MO2 core.

The `Q_INVOKABLE` macro is not relevant for making C++ methods callable from Python in MO2, as MO2 uses pybind11 for its Python bindings, not PyQt/PySide.

To make a C++ method callable from Python in MO2, it would need to be explicitly exposed in the pybind11 bindings, which would require modifying the MO2 core.

#### Potential Use Cases (If Possible)

If direct inter-plugin communication were possible, it could be useful for scenarios like:

1. **Extended File Operations**: A C++ plugin that provides advanced file operations that Python plugins could use
   ```python
   # Python plugin using C++ file operations (theoretical)
   def processArchive(self, archive_path):
       result = self._cpp_plugin.extractSpecialArchive(archive_path)
       return result
   ```

2. **Performance-Critical Operations**: Offloading intensive operations to C++
   ```python
   # Python plugin delegating heavy work to C++ (theoretical)
   def analyzeModConflicts(self):
       conflicts = self._cpp_plugin.findConflicts(self._organizer.modList().allMods())
       return self._formatConflictReport(conflicts)
   ```

3. **Access to External Libraries**: Using C++ to interface with libraries that don't have Python bindings
   ```python
   # Python plugin using C++ plugin to access external library (theoretical)
   def renderPreview(self, model_path):
       preview_image = self._cpp_plugin.renderModel(model_path)
       return preview_image
   ```

#### Advantages and Disadvantages

**Advantages (if possible):**
- Would work within the existing MO2 plugin system
- No need to modify MO2 core
- Clear separation between C++ and Python code

**Disadvantages:**
- May not be possible with the current MO2 architecture
- Limited to types that can be marshalled through Qt's meta-object system
- Cannot expose C++ classes for Python plugins to subclass
- Method calls go through Qt's meta-object system, which adds some overhead
- Cannot add new Python types or extend existing ones
- Requires experimentation to determine if it's even possible

Given the uncertainty about whether this approach is viable, it's recommended to focus on the more reliable alternatives described below.

#### More Reliable Alternative: Shared Data Approach

A more reliable approach is to use the persistent storage mechanism provided by MO2 for indirect communication:

```cpp
// C++ plugin storing data
organizer->setPersistent("MyPluginTool", "sharedData", someQVariant);

// Python plugin retrieving data
data = self._organizer.persistent("MyPluginTool", "sharedData")
```

This approach is more limited in terms of interaction (one-way, not real-time) but provides a reliable way to share data between plugins. It's well-documented in the MO2 API and is guaranteed to work.

### Python Wrapper for C++ Plugin

Another approach would be to create a Python wrapper for the C++ plugin. This would involve:

1. The C++ plugin implementing its core functionality
2. A separate Python plugin that wraps the C++ plugin and exposes its functionality to other Python plugins

The Python wrapper could use ctypes or cffi to call into the C++ plugin, or it could use a more sophisticated approach like pybind11 or SWIG.

This approach has the advantage of allowing more flexibility in terms of the types of functionality that can be exposed, but it requires maintaining both a C++ plugin and a Python wrapper.

### Embedding Lua or JavaScript

If the goal is to provide a scripting interface for a C++ plugin, another option would be to embed a different scripting language like Lua or JavaScript. This would involve:

1. The C++ plugin embedding a Lua or JavaScript interpreter
2. The C++ plugin exposing its functionality to the scripting language
3. Users writing scripts in Lua or JavaScript to extend the plugin

This approach has the advantage of giving the C++ plugin complete control over the scripting environment, but it requires users to learn a different scripting language.

## Conclusion

Based on the analysis of the MO2 codebase, there is no official or straightforward way for a C++ plugin to extend the Python API. The architecture of the Python integration in MO2 is not designed to support this use case.

However, there are several alternative approaches that could be explored, including:

1. Using inter-plugin communication through the MO2 plugin system
2. Creating a Python wrapper for the C++ plugin
3. Embedding a different scripting language like Lua or JavaScript

Each of these approaches has its own advantages and disadvantages, and the best choice would depend on the specific requirements of the plugin.

If extending the Python API is a critical requirement, it might be worth considering contributing to the MO2 core to add official support for this use case. This would involve modifying the Python proxy plugin and runner to allow C++ plugins to register additional bindings.
