#pragma once

#include <iplugin.h>
#include <log.h>

using namespace MOBase;

class HelloPlugin : public QObject, public IPlugin {
    Q_OBJECT
    Q_INTERFACES(MOBase::IPlugin) // the MOBase:: prefix is required
    Q_PLUGIN_METADATA(IID "org.example.HelloPlugin" FILE "helloplugin.json")
    
public:
    HelloPlugin();
    virtual ~HelloPlugin();

    // IPlugin interface
    bool init(MOBase::IOrganizer* moInfo) override;
    QString name() const override;
    QString author() const override;
    QString description() const override;
    MOBase::VersionInfo version() const override;
    QList<MOBase::PluginSetting> settings() const override;

private:
    IOrganizer* m_Organizer;
};
