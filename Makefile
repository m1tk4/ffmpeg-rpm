
RPM_DOCK_IMG=ffbuilder-rpm
RPM_DOCK_CTR=$(RPM_DOCK_IMG)c

# Entry point
build :: build-image patch
	-@docker rm $(RPM_DOCK_CTR)
	docker run -v $(PWD):/home/build --user="`id -u`:`id -g`" --name $(RPM_DOCK_CTR) $(RPM_DOCK_IMG) make ctr-build

# Run within docker to actually build the RPM
ctr-build::
	cd FFmpeg && rpmbuild --define "_topdir `mktemp -d`" --build-in-place -bb ../ffmpeg.spec

# Re-build the list of RPMs needed for building
rpmlist :: build-image
	-@docker rm $(RPM_DOCK_CTR)
	docker run -v $(PWD):/home/build --name $(RPM_DOCK_CTR) $(RPM_DOCK_IMG) make ctr-rpmlist

# Run in docker and rebuild the list of RPMs needed for building
ctr-rpmlist ::
	dnf -y builddep ffmpeg.spec
	dnf repoquery --userinstalled --qf "%{name}" > rpmlist.txt
	chown --reference=ffmpeg.spec rpmlist.txt

# Builds the docker image
build-image ::
	docker build --pull --rm --tag $(RPM_DOCK_IMG) --file Dockerfile .

patch ::
	cd FFmpeg && patch -p 1 -N  < ../alternative_input.patch || true

clean ::
	-@docker container rm --force $(RPM_DOCK_CTR)
	-@rm -f dist/*.{rpm,tgz}
	$(MAKE) -C FFmpeg clean

distclean :: clean
	-@docker image rm --force $(RPM_DOCK_IMG)
	-@docker image prune --force
	-@docker container prune --force
	-rm -rf FFmpeg/_doc
	$(MAKE) -C FFmpeg distclean
