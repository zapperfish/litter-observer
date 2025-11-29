load("//tools/ruby:defs.bzl", "ruby_library")

ruby_library(
    name = "litter_usage_backend",
    srcs = ["litter_usage_backend.rb"],
    visibility = ["//visibility:public"],
    deps = [
        ":litter_usage_metadata_db",
    ],
)

ruby_library(
    name = "litter_usage_metadata_db",
    srcs = ["litter_usage_metadata_db.rb"],
    visibility = ["//visibility:public"],
)

