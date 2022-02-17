
# Get the BUILD_VERSION from command line or set to 0.0.0
BUILD_VERSION?=v5.0.0
B_VERSION:=$(subst v,,$(BUILD_VERSION))

# Entry point
build_all: build

# Note: the order of these is meaningful as .deb builds rely on RPM builds
# to collecti all the right files for them
# build recipes actually will be there
include pkg/rpm/Makefile
#include pkg/deb/Makefile

clean ::
	

