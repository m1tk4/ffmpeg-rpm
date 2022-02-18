
RPM_DOCK_IMG=ffbuilder-rpm
RPM_DOCK_CTR=$(RPM_DOCK_IMG)c

# Entry point
build ::
	docker build --pull --rm --tag $(RPM_DOCK_IMG) --file Dockerfile .
	-@docker rm $(RPM_DOCK_CTR)
	docker run -v $(PWD):/home/build --user="`id -u`:`id -g`" --name $(RPM_DOCK_CTR) $(RPM_DOCK_IMG) make build-rpm

# Run within docker to actually build the RPM
build-rpm ::
	cd FFmpeg && rpmbuild --define "_topdir `mktemp -d`" --build-in-place -bb ../ffmpeg.spec

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
