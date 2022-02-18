
# Get the BUILD_VERSION from command line or set to 0.0.0
BUILD_VERSION?=v5.0.0
B_VERSION:=$(subst v,,$(BUILD_VERSION))

RPM_DOCK_IMG=ffbuilder-rpm
RPM_DOCK_CTR=$(RPM_DOCK_IMG)c

RPM_BUILD_CMD=make build-rpm
#RPM_BUILD_CMD=cd FFmpeg; rpmbuild --define "_topdir `mktemp -d`" -bc ../pkg/rpm/ffmpeg.spec
#RPM_BUILD_CMD=/bin/bash
#RPM_BUILD_CMD=dnf builddep pkg/rpm/ffmpeg.spec

# Entry point
build ::
	docker build --pull --rm --tag $(RPM_DOCK_IMG) --file pkg/rpm/Dockerfile .
	-@docker rm $(RPM_DOCK_CTR)
	docker run -it -v $(PWD):/home/build --user="`id -u`:`id -g`" --name $(RPM_DOCK_CTR) $(RPM_DOCK_IMG) $(RPM_BUILD_CMD)
#	docker run -v $(PWD):/home/build --user="`id -u`:`id -g`" --name $(RPM_DOCK_CTR) $(RPM_DOCK_IMG) $(RPM_BUILD_CMD)
build-rpm:
	cd FFmpeg && rpmbuild --define "_topdir `mktemp -d`" --build-in-place -bb ../pkg/rpm/ffmpeg.spec
	bash

clean ::
	-@docker container rm --force $(RPM_DOCK_CTR)
	-@rm -f dist/*.{rpm,tgz}

distclean ::
	-@rm -f dist/*.{rpm,tgz}
	-@docker image rm --force $(RPM_DOCK_IMG)
	-@docker image prune --force
	-@docker container prune --force
	-@docker container rm --force $(RPM_DOCK_CTR)
