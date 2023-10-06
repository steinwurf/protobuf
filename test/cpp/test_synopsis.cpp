
// Copyright (c) Steinwurf ApS 2020.
// All Rights Reserved
//
// Distributed under the "BSD License". See the accompanying LICENSE.rst
// file.

#include <gtest/gtest.h>

#include "src.pb.h"
#include <google/protobuf/util/json_util.h>

TEST(test_synopsis, api)
{
    auto m = protobuf::Metrics();
    m.set_protocol_version(1);

    auto metric = m.add_metric();
    auto info = metric->mutable_info();
    info->set_kind(protobuf::Kind::COUNTER);
    info->set_name("metric0");
    info->set_description("An unsigned integer metric");
    info->set_unit("bytes");

    info->set_type(protobuf::Type::UINT64);
    metric->set_uint64_value(42);
    info->set_type(protobuf::Type::INT64);
    metric->set_int64_value(-42);
    info->set_type(protobuf::Type::FLOAT64);
    metric->set_float64_value(123.f);
    info->set_type(protobuf::Type::BOOL);
    metric->set_bool_value(true);

    std::string json;
    auto status = google::protobuf::util::MessageToJsonString(m, &json);
    EXPECT_TRUE(status.ok());

    google::protobuf::util::JsonParseOptions options;
    auto m2 = protobuf::Metrics();
    options.ignore_unknown_fields = false;
    status = google::protobuf::util::JsonStringToMessage(json, &m2, options);
    EXPECT_TRUE(status.ok());
}
