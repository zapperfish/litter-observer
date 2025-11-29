load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "litter_box_observer",
    srcs = ["litter_box_observer.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":video_buffer",
    ],
)

py_library(
    name = "video_buffer",
    srcs = ["video_buffer.py"],
    visibility = ["//visibility:public"],
)

