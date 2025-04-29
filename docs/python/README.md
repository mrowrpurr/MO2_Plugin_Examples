# Mod Organizer 2 Python Plugin System Documentation

This document provides a detailed overview of the Python plugin system for Mod Organizer 2, explaining how it works, its architecture, and how to develop plugins using it.

## Table of Contents

- [Mod Organizer 2 Python Plugin System Documentation](#mod-organizer-2-python-plugin-system-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Architecture Overview](#architecture-overview)
    - [Components](#components)
    - [Workflow](#workflow)
  - [Python Proxy Plugin](#python-proxy-plugin)
    - [ProxyPython Class](#proxypython-class)
    - [Plugin Loading Process](#plugin-loading-process)
  - [Python Runner](#python-runner)
    - [PythonRunner Class](#pythonrunner-class)
    - [Python Initialization](#python-initialization)
    - [Plugin Loading and Unloading](#plugin-loading-and-unloading)
  - [Python Bindings (mobase)](#python-bindings-mobase)
    - [Binding Structure](#binding-structure)
    - [Trampoline Classes](#trampoline-classes)
    - [Plugin Interfaces](#plugin-interfaces)
  - [Plugin Development](#plugin-development)
    - [Plugin Structure](#plugin-structure)
    - [Plugin Types](#plugin-types)
    - [Plugin Registration](#plugin-registration)
  - [Advanced Topics](#advanced-topics)
    - [Qt Integration](#qt-integration)
    - [Error Handling](#error-handling)
    - [Memory Management](#memory-management)
  - [Conclusion](#conclusion)

## Introduction

The Python plugin system for Mod Organizer 2 allows developers to create plugins in Python instead of C++. This provides several advantages:

1. **Ease of Development**: Python is generally easier to develop with than C++
2. **Rapid Iteration**: Python plugins can be modified without recompiling
3. **Access to Python Libraries**: Python plugins can use the extensive Python ecosystem

The system consists of three main components:

1. **Python Proxy Plugin**: A C++ plugin that interfaces with Mod Organizer 2
2. **Python Runner**: A library that manages the Python interpreter and loads/unloads Python plugins
3. **Python Bindings (mobase)**: A Python module that provides access to the Mod Organizer 2 API

## Architecture Overview

### Components

The Python plugin system consists of the following components:

1. **Python Proxy Plugin (`proxypython`)**: A C++ plugin that implements the `IPluginProxy` interface. It is responsible for discovering Python plugins and loading them through the Python runner.

2. **Python Runner (`runner`)**: A library that manages the Python interpreter and loads/unloads Python plugins. It provides the `IPythonRunner` interface for the proxy plugin to use.

3. **Python Bindings (`mobase`)**: A Python module that provides access to the Mod Organizer 2 API. It uses pybind11 to expose C++ classes and functions to Python.

4. **Qt Bindings (`pybind11-qt`)**: A library that provides integration between pybind11 and Qt, allowing Python plugins to use Qt classes and widgets.

5. **Utility Libraries (`pybind11-utils`)**: A collection of utility functions and classes for pybind11.

### Workflow

The workflow of the Python plugin system is as follows:

1. Mod Organizer 2 loads the Python proxy plugin (`proxypython.dll`)
2. The proxy plugin initializes the Python runner
3. The Python runner initializes the Python interpreter
4. The proxy plugin discovers Python plugins in the plugins directory
5. When a Python plugin is loaded, the proxy plugin calls the Python runner to load it
6. The Python runner imports the Python module and calls its `createPlugin()` or `createPlugins()` function
7. The Python plugin creates one or more plugin objects that implement the appropriate interfaces
8. The Python runner extracts the plugin objects and returns them to the proxy plugin
9. The proxy plugin returns the plugin objects to Mod Organizer 2
10. Mod Organizer 2 uses the plugin objects as if they were C++ plugins

## Python Proxy Plugin

The Python proxy plugin is a C++ plugin that implements the `IPluginProxy` interface. It is responsible for discovering Python plugins and loading them through the Python runner.

### ProxyPython Class

The `ProxyPython` class is the main class of the Python proxy plugin. It implements the `IPluginProxy` and `IPluginDiagnose` interfaces.

```cpp
class ProxyPython : public QObject,
                    public MOBase::IPluginProxy,
                    public MOBase::IPluginDiagnose {
    Q_OBJECT
    Q_INTERFACES(MOBase::IPlugin MOBase::IPluginProxy MOBase::IPluginDiagnose)
    Q_PLUGIN_METADATA(IID "org.mo2.ProxyPython")

public:
    ProxyPython();

    virtual bool init(MOBase::IOrganizer* moInfo);
    virtual QString name() const override;
    virtual QString localizedName() const override;
    virtual QString author() const override;
    virtual QString description() const override;
    virtual MOBase::VersionInfo version() const override;
    virtual QList<MOBase::PluginSetting> settings() const override;

    QStringList pluginList(const QDir& pluginPath) const override;
    QList<QObject*> load(const QString& identifier) override;
    void unload(const QString& identifier) override;

public:  // IPluginDiagnose
    virtual std::vector<unsigned int> activeProblems() const override;
    virtual QString shortDescription(unsigned int key) const override;
    virtual QString fullDescription(unsigned int key) const override;
    virtual bool hasGuidedFix(unsigned int key) const override;
    virtual void startGuidedFix(unsigned int key) const override;

private:
    MOBase::IOrganizer* m_MOInfo;
    HMODULE m_RunnerLib;
    std::unique_ptr<mo2::python::IPythonRunner> m_Runner;

    enum class FailureType : unsigned int {
        NONE           = 0,
        SEMICOLON      = 1,
        DLL_NOT_FOUND  = 2,
        INVALID_DLL    = 3,
        INITIALIZATION = 4
    };

    FailureType m_LoadFailure;
};
```

### Plugin Loading Process

The Python proxy plugin loads Python plugins through the following process:

1. The `init()` method initializes the Python runner and sets up the necessary paths
2. The `pluginList()` method discovers Python plugins in the plugins directory
3. The `load()` method loads a Python plugin through the Python runner
4. The `unload()` method unloads a Python plugin through the Python runner

The `pluginList()` method looks for two types of Python plugins:

1. **Single-file plugins**: Python files with a `.py` extension
2. **Module plugins**: Directories containing an `__init__.py` file

```cpp
QStringList ProxyPython::pluginList(const QDir& pluginPath) const
{
    QDir dir(pluginPath);
    dir.setFilter(dir.filter() | QDir::NoDotAndDotDot);
    QDirIterator iter(dir);

    // Note: We put python script (.py) and directory names, not the __init__.py
    // files in those since it is easier for the runner to import them.
    QStringList result;
    while (iter.hasNext()) {
        QString name   = iter.next();
        QFileInfo info = iter.fileInfo();

        if (info.isFile() && name.endsWith(".py")) {
            result.append(name);
        }
        else if (info.isDir() && QDir(info.absoluteFilePath()).exists("__init__.py")) {
            result.append(name);
        }
    }

    return result;
}
```

## Python Runner

The Python runner is a library that manages the Python interpreter and loads/unloads Python plugins. It provides the `IPythonRunner` interface for the proxy plugin to use.

### PythonRunner Class

The `PythonRunner` class is the main class of the Python runner. It implements the `IPythonRunner` interface.

```cpp
class PythonRunner : public IPythonRunner {

public:
    PythonRunner()  = default;
    ~PythonRunner() = default;

    QList<QObject*> load(const QString& identifier) override;
    void unload(const QString& identifier) override;

    bool initialize(std::vector<std::filesystem::path> const& pythonPaths) override;
    void addDllSearchPath(std::filesystem::path const& dllPath) override;
    bool isInitialized() const override;

private:
    /**
     * @brief Ensure that the given folder is in sys.path.
     */
    void ensureFolderInPath(QString folder);

private:
    // for each "identifier" (python file or python module folder), contains the
    // list of python objects - this does not keep the objects alive, it simply used
    // to unload plugins
    std::unordered_map<QString, std::vector<py::handle>> m_PythonObjects;
};
```

### Python Initialization

The Python runner initializes the Python interpreter through the `initialize()` method. This method sets up the Python interpreter with the necessary paths and configurations.

```cpp
bool PythonRunner::initialize(std::vector<std::filesystem::path> const& pythonPaths)
{
    // we only initialize Python once for the whole lifetime of the program, even if
    // MO2 is restarted and the proxy or PythonRunner objects are deleted and
    // recreated, Python is not re-initialized
    //
    // in an ideal world, we would initialize Python here (or in the constructor)
    // and then finalize it in the destructor
    //
    // unfortunately, many library, including PyQt6, do not handle properly
    // re-initializing the Python interpreter, so we cannot do that and we keep the
    // interpreter alive
    //

    if (Py_IsInitialized()) {
        return true;
    }

    try {
        static const char* argv0 = "ModOrganizer.exe";

        // set the module search paths
        //
        auto paths = pythonPaths;
        if (paths.empty()) {

            // while it is possible to use config.pythonpath_env, it requires
            // config.use_environment, which brings other stuffs in and might not be
            // what we want, so simply parsing the path ourselve
            //
            if (auto* pythonPath = std::getenv("PYTHONPATH")) {
                for (auto& path : QString::fromStdString(pythonPath).split(";")) {
                    paths.push_back(
                        std::filesystem::path{path.trimmed().toStdWString()});
                }
            }
        }

        PyConfig config;
        PyConfig_InitIsolatedConfig(&config);

        // from PyBind11
        config.parse_argv              = 0;
        config.install_signal_handlers = 0;

        // from MO2
        config.site_import        = 1;
        config.optimization_level = 2;

        // set paths to configuration
        if (!paths.empty()) {
            config.module_search_paths_set = 1;
            for (auto const& path : paths) {
                PyWideStringList_Append(&config.module_search_paths,
                                        absolute(path).native().c_str());
            }
        }

        py::initialize_interpreter(&config, 1, &argv0, true);

        if (!Py_IsInitialized()) {
            MOBase::log::error(
                "failed to init python: failed to initialize interpreter.");

            if (PyGILState_Check()) {
                PyEval_SaveThread();
            }

            return false;
        }

        {
            py::module_ mainModule   = py::module_::import("__main__");
            py::object mainNamespace = mainModule.attr("__dict__");
            mainNamespace["sys"]     = py::module_::import("sys");
            mainNamespace["mobase"]  = py::module_::import("mobase");

            mo2::python::configure_python_stream();
            mo2::python::configure_python_logging(mainNamespace["mobase"]);
        }

        // we need to release the GIL here - which is what this does
        //
        // when Python is initialized, the GIl is acquired, and if it is not
        // release, trying to acquire it on a different thread will deadlock
        PyEval_SaveThread();

        return true;
    }
    catch (const py::error_already_set& ex) {
        MOBase::log::error("failed to init python: {}", ex.what());
        return false;
    }
}
```

### Plugin Loading and Unloading

The Python runner loads and unloads Python plugins through the `load()` and `unload()` methods. These methods use pybind11 to interact with the Python interpreter.

The `load()` method loads a Python plugin and returns a list of plugin objects:

```cpp
QList<QObject*> PythonRunner::load(const QString& identifier)
{
    py::gil_scoped_acquire lock;

    // `pluginName` can either be a python file (single-file plugin or a folder
    // (whole module).
    //
    // For whole module, we simply add the parent folder to path, then we load
    // the module with a simple py::import, and we retrieve the associated
    // __dict__ from which we extract either createPlugin or createPlugins.
    //
    // For single file, we need to use py::eval_file, and we will use the
    // context (global variables) from __main__ (already contains mobase, and
    // other required module). Since the context is shared between called of
    // `instantiate`, we need to make sure to remove createPlugin(s) from
    // previous call.
    try {

        // dictionary that will contain createPlugin() or createPlugins().
        py::dict moduleDict;

        if (identifier.endsWith(".py")) {
            py::object mainModule = py::module_::import("__main__");

            // make a copy, otherwise we might end up calling the createPlugin() or
            // createPlugins() function multiple time
            py::dict moduleNamespace = mainModule.attr("__dict__").attr("copy")();

            std::string temp = ToString(identifier);
            py::eval_file(temp, moduleNamespace).is_none();
            moduleDict = moduleNamespace;
        }
        else {
            // Retrieve the module name:
            QStringList parts      = identifier.split("/");
            std::string moduleName = ToString(parts.takeLast());
            ensureFolderInPath(parts.join("/"));

            // check if the module is already loaded
            py::dict modules = py::module_::import("sys").attr("modules");
            if (modules.contains(moduleName)) {
                py::module_ prev = modules[py::str(moduleName)];
                py::module_(prev).reload();
                moduleDict = prev.attr("__dict__");
            }
            else {
                moduleDict =
                    py::module_::import(moduleName.c_str()).attr("__dict__");
            }
        }

        if (py::len(moduleDict) == 0) {
            MOBase::log::error("No plugins found in {}.", identifier);
            return {};
        }

        // Create the plugins:
        std::vector<py::object> plugins;

        if (moduleDict.contains("createPlugin")) {
            plugins.push_back(moduleDict["createPlugin"]());
        }
        else if (moduleDict.contains("createPlugins")) {
            py::object pyPlugins = moduleDict["createPlugins"]();
            if (!py::isinstance<py::sequence>(pyPlugins)) {
                MOBase::log::error(
                    "Plugin {}: createPlugins must return a sequence.", identifier);
            }
            else {
                py::sequence pyList(pyPlugins);
                size_t nPlugins = pyList.size();
                for (size_t i = 0; i < nPlugins; ++i) {
                    plugins.push_back(pyList[i]);
                }
            }
        }
        else {
            MOBase::log::error("Plugin {}: missing a createPlugin(s) function.",
                               identifier);
        }

        // If we have no plugins, there was an issue, and we already logged the
        // problem:
        if (plugins.empty()) {
            return QList<QObject*>();
        }

        QList<QObject*> allInterfaceList;

        for (py::object pluginObj : plugins) {

            // save to be able to unload it
            m_PythonObjects[identifier].push_back(pluginObj);

            QList<QObject*> interfaceList = py::module_::import("mobase.private")
                                                .attr("extract_plugins")(pluginObj)
                                                .cast<QList<QObject*>>();

            if (interfaceList.isEmpty()) {
                MOBase::log::error("Plugin {}: no plugin interface implemented.",
                                   identifier);
            }

            // Append the plugins to the main list:
            allInterfaceList.append(interfaceList);
        }

        return allInterfaceList;
    }
    catch (const py::error_already_set& ex) {
        MOBase::log::error("Failed to import plugin from {}.", identifier);
        throw pyexcept::PythonError(ex);
    }
}
```

The `unload()` method unloads a Python plugin:

```cpp
void PythonRunner::unload(const QString& identifier)
{
    auto it = m_PythonObjects.find(identifier);
    if (it != m_PythonObjects.end()) {

        py::gil_scoped_acquire lock;

        if (!identifier.endsWith(".py")) {

            // At this point, the identifier is the full path to the module.
            QDir folder(identifier);

            // We want to "unload" (remove from sys.modules) modules that come
            // from this plugin (whose __path__ points under this module,
            // including the module of the plugin itself).
            py::object sys   = py::module_::import("sys");
            py::dict modules = sys.attr("modules");
            py::list keys    = modules.attr("keys")();
            for (std::size_t i = 0; i < py::len(keys); ++i) {
                py::object mod = modules[keys[i]];
                if (PyObject_HasAttrString(mod.ptr(), "__path__")) {
                    QString mpath =
                        mod.attr("__path__")[py::int_(0)].cast<QString>();

                    if (!folder.relativeFilePath(mpath).startsWith("..")) {
                        // If the path is under identifier, we need to unload
                        // it.
                        log::debug("Unloading module {} from {} for {}.",
                                   keys[i].cast<std::string>(), mpath, identifier);

                        PyDict_DelItem(modules.ptr(), keys[i].ptr());
                    }
                }
            }
        }

        // Boost.Python does not handle cyclic garbace collection, so we need to
        // release everything hold by the objects before deleting the objects
        // themselves (done when erasing from m_PythonObjects).
        for (auto& obj : it->second) {
            obj.attr("__dict__").attr("clear")();
        }

        log::debug("Deleting {} python objects for {}.", it->second.size(),
                   identifier);
        m_PythonObjects.erase(it);
    }
}
```

## Python Bindings (mobase)

The Python bindings (`mobase`) provide access to the Mod Organizer 2 API from Python. They use pybind11 to expose C++ classes and functions to Python.

### Binding Structure

The `mobase` module is structured as follows:

1. `mobase.cpp`: The main module definition
2. `wrappers/`: Contains the bindings for various classes and interfaces
   - `basic_classes.cpp`: Bindings for basic classes like `IOrganizer`, `IModInterface`, etc.
   - `game_features.cpp`: Bindings for game features
   - `pyfiletree.cpp`: Bindings for the `IFileTree` interface
   - `pyplugins.cpp`: Bindings for plugin interfaces
   - `utils.cpp`: Bindings for utility functions
   - `widgets.cpp`: Bindings for widget classes
   - `wrappers.cpp`: Bindings for non-plugin classes that can be extended through Python

### Trampoline Classes

The Python bindings use "trampoline classes" to allow Python classes to override C++ virtual methods. These trampoline classes are defined in the `wrappers/` directory.

For example, the `PyPluginTool` trampoline class allows Python classes to implement the `IPluginTool` interface:

```cpp
class PyPluginTool : public PyPluginBase<IPluginTool> {
    Q_OBJECT
    Q_INTERFACES(MOBase::IPlugin MOBase::IPluginTool)
public:
    QString displayName() const override
    {
        PYBIND11_OVERRIDE_PURE(QString, IPluginTool, displayName, );
    }
    QString tooltip() const override
    {
        PYBIND11_OVERRIDE_PURE(QString, IPluginTool, tooltip, );
    }
    QIcon icon() const override
    {
        PYBIND11_OVERRIDE_PURE(QIcon, IPluginTool, icon, );
    }
    void setParentWidget(QWidget* widget) override
    {
        PYBIND11_OVERRIDE(void, IPluginTool, setParentWidget, widget);
    }
    void display() const override
    {
        PYBIND11_OVERRIDE_PURE(void, IPluginTool, display, );
    }

    // we need to bring this in public scope
    using IPluginTool::parentWidget;
};
```

### Plugin Interfaces

The Python bindings expose the following plugin interfaces:

1. `IPlugin`: The base interface for all plugins
2. `IPluginFileMapper`: Interface for plugins that map files
3. `IPluginDiagnose`: Interface for plugins that diagnose problems
4. `IPluginTool`: Interface for tool plugins
5. `IPluginPreview`: Interface for preview plugins
6. `IPluginModPage`: Interface for mod page plugins
7. `IPluginGame`: Interface for game plugins
8. `IPluginInstaller`: Interface for installer plugins
   - `IPluginInstallerSimple`: Interface for simple installer plugins
   - `IPluginInstallerCustom`: Interface for custom installer plugins

These interfaces are exposed through the `add_plugins_bindings()` function in `pyplugins.cpp`.

## Plugin Development

### Plugin Structure

Python plugins for Mod Organizer 2 can be structured in two ways:

1. **Single-file plugins**: A single Python file with a `.py` extension
2. **Module plugins**: A directory containing an `__init__.py` file

Both types of plugins must define either a `createPlugin()` or `createPlugins()` function that returns one or more plugin objects.

### Plugin Types

Python plugins can implement any of the plugin interfaces exposed by the `mobase` module:

1. `IPlugin`: The base interface for all plugins
2. `IPluginFileMapper`: Interface for plugins that map files
3. `IPluginDiagnose`: Interface for plugins that diagnose problems
4. `IPluginTool`: Interface for tool plugins
5. `IPluginPreview`: Interface for preview plugins
6. `IPluginModPage`: Interface for mod page plugins
7. `IPluginGame`: Interface for game plugins
8. `IPluginInstaller`: Interface for installer plugins
   - `IPluginInstallerSimple`: Interface for simple installer plugins
   - `IPluginInstallerCustom`: Interface for custom installer plugins

### Plugin Registration

Python plugins are registered with Mod Organizer 2 through the `createPlugin()` or `createPlugins()` function. These functions must return one or more plugin objects that implement the appropriate interfaces.

For example, a simple tool plugin might look like this:

```python
import mobase

class MyTool(mobase.IPluginTool):
    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parentWidget = None

    def init(self, organizer):
        self._organizer = organizer
        return True

    def name(self):
        return "My Tool"

    def author(self):
        return "Me"

    def description(self):
        return "A simple tool plugin"

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.final)

    def settings(self):
        return []

    def displayName(self):
        return "My Tool"

    def tooltip(self):
        return "A simple tool plugin"

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self._parentWidget = widget

    def display(self):
        QMessageBox.information(self._parentWidget, "My Tool", "Hello, world!")

def createPlugin():
    return MyTool()
```

## Advanced Topics

### Qt Integration

The Python bindings include integration with Qt through the `pybind11-qt` library. This allows Python plugins to use Qt classes and widgets.

The `pybind11-qt` library provides the following features:

1. Conversion between Python and Qt types
2. Support for Qt signals and slots
3. Support for Qt containers like `QList`, `QMap`, etc.
4. Support for Qt enums and flags

### Error Handling

The Python bindings include error handling to convert Python exceptions to C++ exceptions and vice versa. This allows Python plugins to raise exceptions that are properly handled by Mod Organizer 2.

The `pyexcept::PythonError` class is used to wrap Python exceptions in C++:

```cpp
catch (const py::error_already_set& ex) {
    MOBase::log::error("Failed to import plugin from {}.", identifier);
    throw pyexcept::PythonError(ex);
}
```

### Memory Management

The Python bindings include memory management to ensure that Python objects are properly garbage collected. This is done through the `py::qt::set_qt_owner()` function, which ties the lifetime of a Python object to the lifetime of a Qt object:

```cpp
// tie the lifetime of the Python object to the lifetime of the QObject
for (auto* object : helper.objects) {
    py::qt::set_qt_owner(object, plugin_obj);
}
```

## Conclusion

The Python plugin system for Mod Organizer 2 provides a powerful way to extend Mod Organizer 2 with Python plugins. It allows developers to create plugins in Python instead of C++, which can be easier to develop and iterate on.

The system consists of three main components:

1. **Python Proxy Plugin**: A C++ plugin that interfaces with Mod Organizer 2
2. **Python Runner**: A library that manages the Python interpreter and loads/unloads Python plugins
3. **Python Bindings (mobase)**: A Python module that provides access to the Mod Organizer 2 API

These components work together to allow Python plugins to be loaded and used by Mod Organizer 2 as if they were C++ plugins.
