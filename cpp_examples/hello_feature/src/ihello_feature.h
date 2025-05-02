#pragma once

#include <QString>

#include "game_feature.h"

class IHelloFeature : public MOBase::details::GameFeatureCRTP<IHelloFeature> {
public:
    virtual ~IHelloFeature() = default;

    virtual QString exampleFunction() = 0;
};
