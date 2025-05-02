#include "hello_tool.h"
#include <QMessageBox>

// Constructor and Destructor
HelloTool::HelloTool() : m_Organizer(nullptr) {
}

HelloTool::~HelloTool() {
}

// IPlugin interface
bool HelloTool::init(IOrganizer* organizer) {
    m_Organizer = organizer;
    MOBase::log::info("Hello, Tool!");
    return true;
}

QString HelloTool::name() const {
    return "HelloTool";
}

QString HelloTool::author() const {
    return "Your Name";
}

QString HelloTool::description() const {
    return "A simple Tool plugin for Mod Organizer.";
}

VersionInfo HelloTool::version() const {
    return VersionInfo(1, 0, 0);
}

QList<PluginSetting> HelloTool::settings() const {
    return {};  // No settings for this example
}

// IPluginTool interface
QString HelloTool::displayName() const {
    return "Hello World Tool";
}

QString HelloTool::tooltip() const {
    return "This is a simple Hello World tool.";
}

QIcon HelloTool::icon() const {
    return QIcon(); 
}

void HelloTool::display() const {
    QMessageBox::information(parentWidget(), "Hello World", "Hello, World!");
}
