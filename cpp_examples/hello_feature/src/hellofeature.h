#pragma once

#include "ihello_feature.h"

class HelloFeature : public IHelloFeature {
public:
    HelloFeature()           = default;
    ~HelloFeature() override = default;

    QString exampleFunction() override;
};