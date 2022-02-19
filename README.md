# ffmpeg-rpm

RPM Spec and build env Docker container to build ffmpeg5 RPM on Rocky, significantly 
influenced by the work done by the folks at https://rpmfusion.org/.

Includes several ffmpeg tools and few non-official patches, namely:

- `alternative_input` by Béla Bödecs

## Installation

```bash
dnf -y install --nogpgcheck \
    dnf-plugins-core \
    https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
dnf -y config-manager --enable powertools; \
dnf -y install https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm \
    https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm;
dnf install -y \
    https://github.com/m1tk4/ffmpeg-rpm/releases/download/latest/ffmpeg-5.0.0.x86_64.rpm \
    https://github.com/m1tk4/ffmpeg-rpm/releases/download/latest/ffmpeg-libs-5.0.0.x86_64.rpm \ 
    https://github.com/m1tk4/ffmpeg-rpm/releases/download/latest/libavdevice-5.0.0.x86_64.rpm 
```

Optional tools / dev packages:
```bash
dnf install -y \
    https://github.com/m1tk4/ffmpeg-rpm/releases/download/latest/ffmpeg-tools-5.0.0.x86_64.rpm \
    https://github.com/m1tk4/ffmpeg-rpm/releases/download/latest/ffmpeg-devel-5.0.0.x86_64.rpm 
```