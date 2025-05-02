#include "hello_world_plugin.h"
#include <QMessageBox>

// Constructor and Destructor
HelloWorldPlugin::HelloWorldPlugin() : m_Organizer(nullptr) {
}

HelloWorldPlugin::~HelloWorldPlugin() {
}

// IPlugin interface
bool HelloWorldPlugin::init(IOrganizer* organizer) {
    m_Organizer = organizer;
    MOBase::log::info("Hello, World!");  // Log a message to the console
    return true;
}

QString HelloWorldPlugin::name() const {
    return "HelloWorldPlugin";
}

QString HelloWorldPlugin::author() const {
    return "Your Name";
}

QString HelloWorldPlugin::description() const {
    return "A simple Hello World plugin for Mod Organizer.";
}

VersionInfo HelloWorldPlugin::version() const {
    return VersionInfo(1, 0, 0);
}

QList<PluginSetting> HelloWorldPlugin::settings() const {
    return {};  // No settings for this example
}

// IPluginTool interface
QString HelloWorldPlugin::displayName() const {
    return "Hello World Tool";
}

QString HelloWorldPlugin::tooltip() const {
    return "This is a simple Hello World tool.";
}

QIcon HelloWorldPlugin::icon() const {
    return QIcon(); 
}

void HelloWorldPlugin::display() const {
    QMessageBox::information(parentWidget(), "Hello World", "Hello, World!");
}
