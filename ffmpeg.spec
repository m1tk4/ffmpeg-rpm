%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress
%define _builddir ./
%define _sourcedir ./
%define _rpmdir ./
%define _build_name_fmt ../dist/%%{NAME}-%%{VERSION}.%%{ARCH}.rpm

# m1tk4 fixes
%define _without_bluray 1
%define _with_zmq 1

# TODO: add make test to %%check section

#global branch  oldabi-
#global date    20180419
#global rel     rc1

# Cuda and others are only available on some arches
%global cuda_arches x86_64

%if 0%{?el7}
%global _without_aom      1
%global _without_dav1d    1
%global _without_frei0r   1
%global _without_opus     1
%global _without_srt      1
%global _without_vpx      1
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
%if 0%{?rhel} > 7
%ifarch x86_64 i686
%global _with_vapoursynth 1
%endif
%endif
%ifarch x86_64
%global _with_mfx         1
%endif
%endif

# flavor nonfree
%if 0%{?_with_cuda:1}
%global debug_package %{nil}
%global flavor           -cuda
%global progs_suffix     -cuda
#global build_suffix     -lgpl
%ifarch %{cuda_arches}
%global _with_cuvid      1
%global _with_libnpp     1
%endif
%global _with_fdk_aac    1
%global _without_cdio    1
%global _without_frei0r  1
%global _without_gpl     1
%global _without_vidstab 1
%global _without_x264    1
%global _without_x265    1
%global _without_xvid    1
%endif

# Disable nvenc when not relevant
%ifnarch %{cuda_arches}
%global _without_nvenc    1
%endif

# extras flags
%if 0%{!?_cuda_version:1}
%global _cuda_version 10.2
%endif
%global _cuda_version_rpm %(echo %{_cuda_version} | sed -e 's/\\./-/')
%global _cuda_bindir %{_cuda_prefix}/bin
%if 0%{?_with_cuda:1}
%global cuda_cflags $(pkg-config --cflags cuda-%{_cuda_version})
%global cuda_ldflags $(pkg-config --libs cuda-%{_cuda_version})
%endif

%if 0%{?_with_libnpp:1}
%global libnpp_cflags $(pkg-config --cflags nppi-%{_cuda_version} nppc-%{_cuda_version})
%global libnpp_ldlags $(pkg-config --libs-only-L nppi-%{_cuda_version} nppc-%{_cuda_version})
%endif

%if 0%{?_with_rpi:1}
%global _with_omx        1
%global _with_omx_rpi    1
%global _with_mmal       1
ExclusiveArch: armv7hnl
%endif

%if 0%{?_without_gpl}
%global lesser L
%endif

%if 0%{!?_without_amr} || 0%{?_with_gmp} || 0%{?_with_smb}
%global ffmpeg_license %{?lesser}GPLv3+
%else
%global ffmpeg_license %{?lesser}GPLv2+
%endif

Summary:        Digital VCR and streaming server
Name:           ffmpeg%{?flavor}
Version:        5.0.0
Release:        1
License:        %{ffmpeg_license}
URL:            http://ffmpeg.org/

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%{?_with_cuda:BuildRequires: cuda-minimal-build-%{_cuda_version_rpm} cuda-drivers-devel}
%{?_with_libnpp:BuildRequires: pkgconfig(nppc-%{_cuda_version})}
BuildRequires:  alsa-lib-devel
BuildRequires:  bzip2-devel
%{?_with_faac:BuildRequires: faac-devel}
%{?_with_fdk_aac:BuildRequires: fdk-aac-devel}
%{?_with_flite:BuildRequires: flite-devel}
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
%{!?_without_frei0r:BuildRequires: frei0r-devel}
%{?_with_gme:BuildRequires: game-music-emu-devel}
BuildRequires:  gnutls-devel
BuildRequires:  gsm-devel
%{?_with_ilbc:BuildRequires: ilbc-devel}
BuildRequires:  lame-devel >= 3.98.3
%{!?_without_jack:BuildRequires: jack-audio-connection-kit-devel}
%{!?_without_ladspa:BuildRequires: ladspa-devel}
%{!?_without_aom:BuildRequires:  libaom-devel}
%{!?_without_dav1d:BuildRequires:  libdav1d-devel >= 0.2.1}
%{!?_without_ass:BuildRequires:  libass-devel}
%{!?_without_bluray:BuildRequires:  libbluray-devel}
%{?_with_bs2b:BuildRequires: libbs2b-devel}
%{?_with_caca:BuildRequires: libcaca-devel}
%{!?_without_cdio:BuildRequires: libcdio-paranoia-devel}
%{?_with_chromaprint:BuildRequires: libchromaprint-devel}
%{?_with_crystalhd:BuildRequires: libcrystalhd-devel}
%if 0%{?_with_ieee1394}
BuildRequires:  libavc1394-devel
BuildRequires:  libdc1394-devel
BuildRequires:  libiec61883-devel
%endif
BuildRequires:  libdrm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libGL-devel
BuildRequires:  libmodplug-devel
BuildRequires:  librsvg2-devel
%{?_with_rtmp:BuildRequires: librtmp-devel}
%{?_with_smb:BuildRequires: libsmbclient-devel}
%{!?_without_srt:BuildRequires: srt-devel > 1.3.0}
BuildRequires:  libssh-devel
BuildRequires:  libtheora-devel
BuildRequires:  libv4l-devel
%{?!_without_vaapi:BuildRequires: libva-devel >= 0.31.0}
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
%{?_with_vapoursynth:BuildRequires: vapoursynth-devel}
%{?!_without_vpx:BuildRequires: libvpx-devel >= 1.4.0}
%{?_with_mfx:BuildRequires: pkgconfig(libmfx) >= 1.23-1}
%ifarch %{ix86} x86_64
BuildRequires:  nasm
%endif
%{?_with_webp:BuildRequires: libwebp-devel}
%{?_with_netcdf:BuildRequires: netcdf-devel}
%{?_with_rpi:BuildRequires: raspberrypi-vc-devel}
%{!?_without_nvenc:BuildRequires: nv-codec-headers}
%{!?_without_amr:BuildRequires: opencore-amr-devel vo-amrwbenc-devel}
%{?_with_omx:BuildRequires: libomxil-bellagio-devel}
BuildRequires:  libxcb-devel
%{!?_without_openal:BuildRequires: openal-soft-devel}
%if 0%{!?_without_opencl:1}
BuildRequires:  opencl-headers ocl-icd-devel
%{?fedora:Recommends: opencl-icd}
%endif
%{?_with_opencv:BuildRequires: opencv-devel}
BuildRequires:  openjpeg2-devel
%{!?_without_opus:BuildRequires: opus-devel >= 1.1.3}
%{!?_without_pulse:BuildRequires: pulseaudio-libs-devel}
BuildRequires:  perl(Pod::Man)
%{?_with_rubberband:BuildRequires: rubberband-devel}
%{!?_without_tools:BuildRequires: SDL2-devel}
%{?_with_snappy:BuildRequires: snappy-devel}
BuildRequires:  soxr-devel
BuildRequires:  speex-devel
%{?_with_tesseract:BuildRequires: tesseract-devel}
#BuildRequires:  texi2html
BuildRequires:  texinfo
%{?_with_twolame:BuildRequires: twolame-devel}
%{?_with_wavpack:BuildRequires: wavpack-devel}
%{!?_without_vidstab:BuildRequires:  vid.stab-devel}
%{!?_without_x264:BuildRequires: x264-devel >= 0.0.0-0.31}
%{!?_without_x265:BuildRequires: x265-devel}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
BuildRequires:  zimg-devel >= 2.7.0
BuildRequires:  zlib-devel
%{?_with_zmq:BuildRequires: zeromq-devel}
%{!?_without_zvbi:BuildRequires: zvbi-devel}

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}

%description    libs
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package     -n libavdevice%{?flavor}
Summary:        Special devices muxing/demuxing library
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description -n libavdevice%{?flavor}
Libavdevice is a complementary library to libavf "libavformat". It provides
various "special" platform-specific muxers and demuxers, e.g. for grabbing
devices, audio capture and playback etc.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?flavor}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

# Don't use the %%configure macro as this is not an autotool script
%global ff_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/%{name} \\\
    --docdir=%{_docdir}/%{name} \\\
    --incdir=%{_includedir}/%{name} \\\
    --libdir=%{_libdir} \\\
    --mandir=%{_mandir} \\\
    --arch=%{_target_cpu} \\\
    --optflags="%{optflags}" \\\
    --extra-ldflags="%{?__global_ldflags} %{?cuda_ldflags} %{?libnpp_ldlags}" \\\
    --extra-cflags="%{?cuda_cflags} %{?libnpp_cflags}" \\\
    %{?flavor:--disable-manpages} \\\
    %{?progs_suffix:--progs-suffix=%{progs_suffix}} \\\
    %{?build_suffix:--build-suffix=%{build_suffix}} \\\
    %{!?_without_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3} \\\
    --enable-bzlib \\\
    %{?_with_chromaprint:--enable-chromaprint} \\\
    %{!?_with_crystalhd:--disable-crystalhd} \\\
    --enable-fontconfig \\\
    %{!?_without_frei0r:--enable-frei0r} \\\
    --enable-gcrypt \\\
    %{?_with_gmp:--enable-gmp --enable-version3} \\\
    --enable-gnutls \\\
    %{!?_without_ladspa:--enable-ladspa} \\\
    %{!?_without_aom:--enable-libaom} \\\
    %{!?_without_dav1d:--enable-libdav1d} \\\
    %{!?_without_ass:--enable-libass} \\\
    %{!?_without_bluray:--enable-libbluray} \\\
    %{?_with_bs2b:--enable-libbs2b} \\\
    %{?_with_caca:--enable-libcaca} \\\
    %{?_with_cuda:--enable-cuda-sdk --enable-nonfree} \\\
    %{?_with_cuvid:--enable-cuvid --enable-nonfree} \\\
    %{!?_without_cdio:--enable-libcdio} \\\
    %{?_with_ieee1394:--enable-libdc1394 --enable-libiec61883} \\\
    --enable-libdrm \\\
    %{?_with_faac:--enable-libfaac --enable-nonfree} \\\
    %{?_with_fdk_aac:--enable-libfdk-aac --enable-nonfree} \\\
    %{?_with_flite:--enable-libflite} \\\
    %{!?_without_jack:--enable-libjack} \\\
    --enable-libfreetype \\\
    %{!?_without_fribidi:--enable-libfribidi} \\\
    %{?_with_gme:--enable-libgme} \\\
    --enable-libgsm \\\
    %{?_with_ilbc:--enable-libilbc} \\\
    %{?_with_libnpp:--enable-libnpp --enable-nonfree} \\\
    --enable-libmp3lame \\\
    %{?_with_netcdf:--enable-netcdf} \\\
    %{?_with_mmal:--enable-mmal} \\\
    %{!?_without_nvenc:--enable-nvenc} \\\
    %{?_with_omx:--enable-omx} \\\
    %{?_with_omx_rpi:--enable-omx-rpi} \\\
    %{!?_without_openal:--enable-openal} \\\
    %{!?_without_opencl:--enable-opencl} \\\
    %{?_with_opencv:--enable-libopencv} \\\
    %{!?_without_opengl:--enable-opengl} \\\
    --enable-libopenjpeg \\\
    %{!?_without_opus:--enable-libopus} \\\
    %{!?_without_pulse:--enable-libpulse} \\\
    --enable-librsvg \\\
    %{?_with_rtmp:--enable-librtmp} \\\
    %{?_with_rubberband:--enable-librubberband} \\\
    %{?_with_smb:--enable-libsmbclient} \\\
    %{?_with_snappy:--enable-libsnappy} \\\
    %{!?_without_srt:--enable-libsrt} \\\
    --enable-libsoxr \\\
    --enable-libspeex \\\
    --enable-libssh \\\
    %{?_with_tesseract:--enable-libtesseract} \\\
    --enable-libtheora \\\
    %{?_with_twolame:--enable-libtwolame} \\\
    --enable-libvorbis \\\
    --enable-libv4l2 \\\
    %{!?_without_vidstab:--enable-libvidstab} \\\
    %{?_with_vapoursynth:--enable-vapoursynth} \\\
    %{!?_without_vpx:--enable-libvpx} \\\
    %{?_with_webp:--enable-libwebp} \\\
    %{!?_without_x264:--enable-libx264} \\\
    %{!?_without_x265:--enable-libx265} \\\
    %{!?_without_xvid:--enable-libxvid} \\\
    --enable-libzimg \\\
    %{?_with_zmq:--enable-libzmq} \\\
    %{!?_without_zvbi:--enable-libzvbi} \\\
    --enable-avfilter \\\
    --enable-libmodplug \\\
    --enable-postproc \\\
    --enable-pthreads \\\
    --disable-static \\\
    --enable-shared \\\
    %{!?_without_gpl:--enable-gpl} \\\
    --disable-debug \\\
    --disable-stripping


%prep
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
mkdir -p _doc/examples
cp -pr doc/examples/{*.c,Makefile,README} _doc/examples/

%build
%{?_with_cuda:export PATH=${PATH}:%{_cuda_bindir}}
%{ff_configure}\
    --shlibdir=%{_libdir} \
%if 0%{?_without_tools:1}
    --disable-doc \
    --disable-ffmpeg --disable-ffplay --disable-ffprobe \
%endif
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
    %{?_with_mfx:--enable-libmfx} \
%ifarch %{ix86} x86_64 %{power64}
    --enable-runtime-cpudetect \
%endif
%ifarch %{power64}
%ifarch ppc64
    --cpu=g5 \
%endif
%ifarch ppc64p7
    --cpu=power7 \
%endif
%ifarch ppc64le
    --cpu=power8 \
%endif
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%endif
%ifarch armv7hl armv7hnl
    --cpu=armv7-a \
    --enable-vfpv3 \
    --enable-thumb \
%endif
%ifarch armv7hl
    --disable-neon \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif
    || cat ffbuild/config.log

%make_build -j6
make documentation V=1
make alltools V=1

%install
%make_install V=1
%if 0%{!?flavor:1}
rm -r %{buildroot}%{_datadir}/%{name}/examples
%endif
%if 0%{!?progs_suffix:1}
install -pm755 tools/qt-faststart %{buildroot}%{_bindir}
%endif

%ldconfig_scriptlets  libs
%ldconfig_scriptlets -n libavdevice%{?flavor}



%if 0%{!?_without_tools:1}
%files
%{_bindir}/ffmpeg%{?progs_suffix}
%{_bindir}/ffplay%{?progs_suffix}
%{_bindir}/ffprobe%{?progs_suffix}
%{!?progs_suffix:%{_bindir}/qt-faststart}
%{!?flavor:
%{_mandir}/man1/ffmpeg*.1*
%{_mandir}/man1/ffplay*.1*
%{_mandir}/man1/ffprobe*.1*
}
%{_datadir}/%{name}
%endif

%files libs
%doc  CREDITS README.md
%license %(find COPYING.* -printf ' %%p')
%{_libdir}/lib*.so.*
%exclude %{_libdir}/libavdevice%{?build_suffix}.so.*
%{!?flavor:%{_mandir}/man3/lib*.3*
%exclude %{_mandir}/man3/libavdevice.3*
}

%files -n libavdevice%{?flavor}
%{_libdir}/libavdevice%{?build_suffix}.so.*
%{!?flavor:%{_mandir}/man3/libavdevice.3*}

%files devel
%doc MAINTAINERS doc/APIchanges %(find doc/*.txt -printf ' %%p')
%doc _doc/examples
%doc %{_docdir}/%{name}/*.html
%{_includedir}/%{name}
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/lib*.so


%changelog
* Wed Dec 01 2021 Leigh Scott <leigh123linux@gmail.com> - 4.2.5-2
- rebuilt
