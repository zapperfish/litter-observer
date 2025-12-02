load("@rules_proto_grpc_python//:defs.bzl", "python_proto_compile", "python_proto_library")

proto_library(
    name = "litter_usage_metadata_proto",
    srcs = ["litter_usage_metadata.proto"],
)

python_proto_compile(
    name = "litter_usage_metadata_python_proto",
    protos = [":litter_usage_metadata_proto"],
)

proto_library(
    name = "observer_configs_proto",
    srcs = ["observer_configs.proto"],
)

python_proto_compile(
    name = "observer_configs_python_proto",
    protos = [":observer_configs_proto"],
)

python_proto_library(
    name = "litter_usage_metadata_py_pb2",
    protos = [":litter_usage_metadata_proto"],
    visibility = ["//visibility:public"],
)

python_proto_library(
    name = "observer_configs_py_pb2",
    protos = [":observer_configs_proto"],
    visibility = ["//visibility:public"],
)