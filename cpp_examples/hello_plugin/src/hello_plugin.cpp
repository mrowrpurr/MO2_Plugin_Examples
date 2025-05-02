#include "hello_plugin.h"

// Constructor and Destructor
HelloPlugin::HelloPlugin() : m_Organizer(nullptr) {}

HelloPlugin::~HelloPlugin() {}

// IPlugin interface
bool HelloPlugin::init(IOrganizer* organizer) {
    m_Organizer = organizer;
    MOBase::log::info("Hello, Plugin!");
    return true;
}

QString HelloPlugin::name() const { return "HelloPlugin"; }

QString HelloPlugin::author() const { return "Your Name"; }

QString HelloPlugin::description() const { return "A simple plugin for Mod Organizer."; }

VersionInfo HelloPlugin::version() const { return VersionInfo(1, 0, 0); }

QList<PluginSetting> HelloPlugin::settings() const {
    return {};  // No settings for this example
}
