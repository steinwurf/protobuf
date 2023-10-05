
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
    auto t = protobuf::Metrics();
    t.set_protocol_version(1);

    std::string json;
    auto msg = google::protobuf::util::MessageToJsonString(t, &json);
    EXPECT_TRUE(msg.ok());
}
