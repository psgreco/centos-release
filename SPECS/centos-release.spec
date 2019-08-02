%define debug_package %{nil}
%define product_family CentOS Linux
%define variant_titlecase Server
%define variant_lowercase server
%ifarch %{arm}
%define release_name AltArch
%define contentdir   altarch
%else
%define release_name Core
%define contentdir   centos
%endif
%ifarch ppc64le
%define tuned_profile :server
%endif
%define infra_var stock
%define base_release_version 8
%define full_release_version 8
%define dist_release_version 8
%define upstream_rel_long 8.0-0
%define upstream_rel 8.0
%define centos_rel 0.1905
#define beta Beta
%define dist .el%{dist_release_version}

# The anaconda scripts in %{_libexecdir} can create false requirements
%global __requires_exclude_from %{_libexecdir}

Name:           centos-release
Version:        %{upstream_rel}
Release:        %{centos_rel}.0.6%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
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

Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
Source10:       RPM-GPG-KEY-centosofficial
Source11:       RPM-GPG-KEY-centostesting

Source99:       update-boot
Source100:      rootfs-expand

Source200:      EULA
Source201:      GPL
Source202:      Contributors

Source300:      CentOS-Base.repo
Source301:      CentOS-CR.repo
Source302:      CentOS-Debuginfo.repo
Source303:      CentOS-Extras.repo
Source304:      CentOS-fasttrack.repo
Source305:      CentOS-Media.repo
Source306:      CentOS-Sources.repo
Source307:      CentOS-Vault.repo
Source308:      CentOS-AppStream.repo
Source309:      CentOS-Devel.repo
Source310:      CentOS-centosplus.repo

%ifarch %{arm}
%description -n %{pkg_name}
%{product_family} release files
%endif

%description
%{product_family} release files

%prep
echo OK

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
PLATFORM_ID="platform:el%{full_release_version}"
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

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE10} %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE11} %{buildroot}/etc/pki/rpm-gpg

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE300} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE301} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE302} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE303} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE304} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE305} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE306} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE307} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE308} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE309} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE310} %{buildroot}/etc/yum.repos.d

mkdir -p -m 755 %{buildroot}/etc/dnf/vars
echo "%{infra_var}" > %{buildroot}/etc/dnf/vars/infra
echo "%{contentdir}" >%{buildroot}/etc/dnf/vars/contentdir
%ifarch %{arm}
echo %{base_release_version} > %{buildroot}/etc/dnf/vars/releasever
%endif

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
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/centos-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/centos-release
ln -s centos-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 %{SOURCE201} %{buildroot}/%{_docdir}/centos-release
install -m 644 %{SOURCE202} %{buildroot}/%{_docdir}/centos-release

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
%config(noreplace) /etc/dnf/vars/*
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

