#pragma once

#include <iplugintool.h>
#include <log.h>

using namespace MOBase;

class HelloTool : public IPluginTool {
    Q_OBJECT
    Q_INTERFACES(MOBase::IPlugin MOBase::IPluginTool)  // the MOBase:: prefix is required
    Q_PLUGIN_METADATA(IID "org.example.HelloTool" FILE "hellotool.json")

public:
    HelloTool();
    virtual ~HelloTool();

    // IPlugin interface
    bool                         init(MOBase::IOrganizer* moInfo) override;
    QString                      name() const override;
    QString                      author() const override;
    QString                      description() const override;
    MOBase::VersionInfo          version() const override;
    QList<MOBase::PluginSetting> settings() const override;

    // IPluginTool interface
    QString displayName() const override;
    QString tooltip() const override;
    QIcon   icon() const override;

public Q_SLOTS:
    void display() const override;

private:
    IOrganizer* m_Organizer;
};
