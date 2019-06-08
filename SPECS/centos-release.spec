%define debug_package %{nil}
%define product_family CentOS Linux
%define variant_titlecase Server
%define variant_lowercase server
%ifarch %{ix86}
%define targetdir x86_64
%else
%define targetdir %{_target_cpu}
%endif
%ifarch %{arm}
%define release_name AltArch
%else
%define release_name Core
%endif
%ifarch ppc64le
%define tuned_profile :server
%endif
%define base_release_version 8
%define full_release_version 8
%define dist_release_version 8
%define upstream_rel_long 8.0-0
%define upstream_rel 8.0
%define centos_rel 0.1905
#define beta Beta
%define dist .el%{dist_release_version}

Name:           centos-release
Version:        %{base_release_version}
Release:        %{centos_rel}.0.4%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Requires(post): coreutils, grep
%ifnarch %{arm}
%define pkg_name %{name}
%else
Requires:       extlinux-bootloader
%define pkg_name centos-userland-release
%package -n %{pkg_name}
Summary:        %{product_family} release file
%endif
Provides:       centos-release = %{version}-%{release}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}

Provides:       centos-release-eula
Provides:       redhat-release-eula

Source0:        centos-release-%{base_release_version}-%{centos_rel}.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset

Source99:       update-boot
Source100:      rootfs-expand

%ifarch %{arm}
%description -n %{pkg_name}
%{product_family} release files
%endif

%description
%{product_family} release files

%prep
%setup -q -n centos-release-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version}.%{centos_rel} (%{release_name}) " > %{buildroot}/etc/centos-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/centos-release-upstream
ln -s centos-release %{buildroot}/etc/system-release
ln -s centos-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:%{base_release_version}%{?tuned_profile}"
HOME_URL="https://www.centos.org/"
BUG_REPORT_URL="https://bugs.centos.org/"

CENTOS_MANTISBT_PROJECT="CentOS-%{base_release_version}"
CENTOS_MANTISBT_PROJECT_VERSION="%{base_release_version}"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="%{base_release_version}"

EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:centos:centos:%{base_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

pushd %{targetdir}
# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
for file in CentOS-*.repo; do 
    install -m 644 $file %{buildroot}/etc/yum.repos.d
done

mkdir -p -m 755 %{buildroot}/etc/yum/vars
install -m 0644 yum-vars-infra %{buildroot}/etc/yum/vars/infra
%ifarch %{arm}
echo %{base_release_version} > %{buildroot}/etc/yum/vars/releasever
%endif
popd

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/centos-release
ln -s centos-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 EULA %{buildroot}/%{_datadir}/centos-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/centos-release
ln -s centos-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/centos-release
install -m 644 Contributors %{buildroot}/%{_docdir}/centos-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/

%ifarch %{arm}
# Install armhfp specific tools
mkdir -p %{buildroot}/%{_bindir}/
install -m 0755 %{SOURCE99} %{buildroot}%{_bindir}/
install -m 0755 %{SOURCE100} %{buildroot}%{_bindir}/
%endif

%posttrans -n %{pkg_name}
%ifarch %{arm}
if [ -e /usr/local/bin/rootfs-expand ];then
rm -f /usr/local/bin/rootfs-expand
fi
echo 'altarch' >/etc/yum/vars/contentdir
%else
echo 'centos' > /etc/yum/vars/contentdir
%endif


%clean
rm -rf %{buildroot}

%files -n %{pkg_name}
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
/etc/centos-release-upstream
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) /etc/yum/vars/*
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/centos-release/*
%{_datadir}/redhat-release
%{_datadir}/centos-release/*
%{_prefix}/lib/systemd/system-preset/*
%ifarch %{arm}
%attr(0755,root,root) %{_bindir}/update-boot
%attr(0755,root,root) %{_bindir}/rootfs-expand
%endif

%changelog
* Wed May  8 2019 Pablo Greco <pablo@fliagreco.com.ar> 8-0.el7
- Initial setup for CentOS-8

