%define debug_package %{nil}
%define product_family CentOs Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Final
%define base_release_version 7rc1
%define full_release_version 7.0
%define dist_release_version 7
#define beta Beta
%define dist .el%{dist_release_version}

Name:           centos-release
Version:        %{base_release_version}
Release:        0%{?dist}.0
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       centos-release = %{version}-%{release}
Provides:       redhat-release = %{version}-%{release}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{base_release_version}%{?variant_titlecase}
Source0:        centos-release-%{base_release_version}.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset


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
echo "%{product_family}%{?variant_titlecase: %{variant_titlecase}} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > %{buildroot}/etc/centos-release
ln -s centos-release %{buildroot}/etc/system-release
ln -s centos-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}}"
VERSION="%{full_release_version} (%{release_name})"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family}%{?variant_titlecase: %{variant_titlecase}} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}"
HOME_URL="https://www.redhat.com/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="%{product_family} %{base_release_version}"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{full_release_version}
REDHAT_SUPPORT_PRODUCT="%{product_family}"
REDHAT_SUPPORT_PRODUCT_VERSION=%{full_release_version}
EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:redhat:enterprise_linux:%{full_release_version}:%{?beta:beta}%{!?beta:GA}%{?variant_lowercase::%{variant_lowercase}}" | tr [A-Z] [a-z] > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%centos_ver %{base_release_version}
%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/redhat-release
install -m 644 EULA %{buildroot}/%{_datadir}/redhat-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/redhat-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
/etc/rpm/macros.dist
%{_docdir}/redhat-release/*
%{_datadir}/redhat-release/*
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Fri Jun 13 2014 Karanbir Singh <kbsingh@centos.org> 7-0.el7
- initial setup for centos-rc
