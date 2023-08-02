%if 0%{?fedora}
%global buildforkernels akmod
%endif
%if 0%{?el9}
# kmod fails on rhel9 kernel with aarch64 - just build an akmod there
%ifarch aarch64
%global buildforkernels akmod
%endif
%endif
%global debug_package %{nil}

%global commit 2c9b67072b15d903fecde67c7f269abeafee4c25
%global commitdate 20230503
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global prjname v4l2loopback

Name:           %{prjname}-kmod
Summary:        Kernel module (kmod) for %{prjname}
Version:        0.12.7^%{commitdate}g%{shortcommit}
Release:        2%{?dist}
License:        GPLv2+

URL:            https://github.com/umlaeute/v4l2loopback
Source0:        %{url}/archive/%{commit}/%{prjname}-%{shortcommit}.tar.gz

Patch0:         0001-v4l2loopback-Fixup-bytesused-field-when-writer-sends.patch

BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This module allows you to create "virtual video devices". Normal (v4l2)
applications will read these devices as if they were ordinary video
devices, but the video will not be read from e.g. a capture card but
instead it is generated by another application.

This package contains the kmod module for %{prjname}.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c
(cd v4l2loopback-%{commit}
%patch0 -p1
)

for kernel_version  in %{?kernel_versions} ; do
  cp -a v4l2loopback-%{commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/v4l2loopback.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}


%changelog
* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.12.7^20230503g2c9b670-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Kate Hsuan <hpa@redhat.com> - 0.12.7-20230503g2c9b670-1
- Updated to commit 2c9b67072b15d903fecde67c7f269abeafee4c25 
- The patch is used to prevent the value of byteused field becomes too large

* Thu Mar 02 2023 Kate Hsuan <hpa@redhat.com> - 0.12.7-20230220ga669686-1
- Updated to commit a66968647843f57448b59cf98d0318f1e98e072c

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.12.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Fri Aug 05 2022 Leigh Scott <leigh123linux@gmail.com> - 0.12.7-1
- Update to 0.12.7

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.12.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.12.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.12.5-4
- rebuilt

* Tue Feb 23 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.12.5-3
- Bump spec

* Mon Feb 15 2021 Nicolas Chauvet <kwizart@gmail.com> - 0.12.5-2
- Rework spec file

* Sat Dec 26 2020 Neal Gompa <ngompa13@gmail.com> - 0.12.5-1
- Initial packaging
