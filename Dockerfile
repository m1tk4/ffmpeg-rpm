#
#   This Dockerfile is only used in the build process on Github
#

FROM rockylinux/rockylinux:8

ENV container=docker
ENV HOMEDIR=/home/build

RUN dnf -y install --nogpgcheck dnf-plugins-core https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    dnf -y config-manager --enable powertools; \
    dnf -y install https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm \
        https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm

COPY rpmlist.txt /tmp/rpmlist.txt
RUN dnf -y install `cat /tmp/rpmlist.txt`

RUN mkdir $HOMEDIR

# Ensure the termination happens on container stop, cgroup, starting init
WORKDIR $HOMEDIR
CMD ["/bin/bash"]
