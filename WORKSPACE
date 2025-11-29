workspace(name = "litter_observer")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Protobuf - using version 25.1 (latest stable for Bazel 7.x)
http_archive(
    name = "com_google_protobuf",
    sha256 = "9bd87b8280ef720d3240514f884e56a712f2218f0d693b48050c836028940a42",
    strip_prefix = "protobuf-25.1",
    urls = ["https://github.com/protocolbuffers/protobuf/releases/download/v25.1/protobuf-25.1.tar.gz"],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
protobuf_deps()

# Python rules
http_archive(
    name = "rules_python",
    sha256 = "9d04041ac92a0985e344235f5d946f71ac543f1b1565f2cdbc9a2aaee8adf55b",
    strip_prefix = "rules_python-0.26.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.26.0/rules_python-0.26.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")
py_repositories()

python_register_toolchains(
    name = "python3_10",
    python_version = "3.10",
)

# Ruby rules - simplified custom rules
# We'll define custom Ruby rules in //tools/ruby
