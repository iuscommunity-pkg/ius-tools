
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

#python major version
%{expand: %%global pyver %(%{__python} -c 'import sys;print(sys.version[0:3])')}

# disable by default many of the ius-tools subpackages due to requirements
%bcond_with admin
%bcond_with launchpad
%bcond_with ircbot
%bcond_with version_tracker

Name:		ius-tools	
Version:	0.1.6
Release:	1.ius%{?dist}
Summary:	Scripts and Utilities for The IUS Community Project 

Group:		Applicatons/System	
License:	GPLv2
URL:		https://github.com/rackspace/ius-tools
Source0:	http://dl.iuscommunity.org/pub/ius-tools/ius-tools-%{version}.tar.gz
Patch0:		remove_python_requires.diff

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

BuildRequires:	python, python-setuptools, python-genshi
Requires:	python, python-cement, python-genshi, python-configobj
Requires:	monkeyfarm-core, python-monkeyfarm-interface

%description	
The IUS Community Project is committed to providing up to date and regularly 
maintained RPM packages for the latest upstream versions of PHP, Python, MySQL 
and other common software specifically for Red Hat Enterprise Linux and 
clones.  The project is sponsored by Rackspace, and lead by a number of 
Linux Engineers from the companies 'RPM Development Team' that also 
contributes to other projects such as Fedora and EPEL.

The IUS Tools project is made up of scripts and utilities such as our irc bot,
and build system automation scripts.  It is Open Source and released under the
GNU General Public License v2.

This software is built on the Cement CLI Application Framework.

%if %{with admin}
%package admin
Group:          Applicatons/System
Summary:        Admin Plugin for IUS Community Project Tools

BuildRequires:  python, python-setuptools, python-genshi
Requires:       python, python-cement, python-genshi
Requires:       ius-tools

%description admin
Admin Plugin for IUS Community Project Tools
%endif

%if %{with launchpad}
%package launchpad
Group:          Applicatons/System
Summary:        LaunchPad Plugin for IUS Tools

BuildRequires:  python, python-setuptools, python-genshi
Requires:       python, python-cement, python-genshi
#Requires:	python-launchpad
Requires:       ius-tools

%description launchpad
LaunchPad Plugin for IUS Tools
%endif

%if %{with version_tracker}
%package version_tracker
Group:		Applicatons/System
Summary:	Plugin to get the latest version of Package from upstream

BuildRequires:	python, python-setuptools, python-genshi
Requires:	python, python-cement, python-genshi
Requires:	ius-tools

%description version_tracker
Plugin to get the latest version of Package from upstream
%endif

%if %{with ircbot}
%package ircbot
Group:		Applicatons/System
Summary:	Plugin to run the IUS IRC Bot

BuildRequires:	python, python-setuptools, python-genshi
Requires:	python, python-cement, python-genshi
Requires:	ius-tools

%description ircbot
Plugin to run the IUS IRC Bot
%endif

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
pushd src/iustools.core 
%{__python} setup.py build
popd

# if condition meet build with admin
%if %{with admin}
pushd src/iustools.admin
%{__python} setup.py build
popd
%endif

# if condition meet build with launchpad
%if %{with launchpad}
pushd src/iustools.launchpad
%{__python} setup.py build
popd
%endif

# if condition meet build with ircbot
%if %{with ircbot}
pushd src/iustools.ircbot
%{__python} setup.py build
popd
%endif

# if condition meet build with version_tracker
%if %{with version_tracker}
pushd src/iustools.version_tracker
%{__python} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_sysconfdir}/ius-tools/plugins.d/
mkdir -p %{buildroot}%{_datadir}/ius-tools/

pushd src/iustools.core 
%{__python} setup.py install -O1 \
		    --skip-build \
	     --root %{buildroot}
popd

# Install our configs
%__install src/iustools.core/config/ius-tools.conf \
	%{buildroot}%{_sysconfdir}/ius-tools/ius-tools.conf


# if condition meet build with admin
%if %{with admin}
pushd src/iustools.admin
%{__python} setup.py install -O1 \
                    --skip-build \
             --root %{buildroot}
popd

# Install config
%__install src/iustools.admin/config/plugins.d/admin.conf \
        %{buildroot}%{_sysconfdir}/ius-tools/plugins.d/admin.conf

%endif

# if condition meet build with launchpad
%if %{with launchpad}
pushd src/iustools.launchpad
%{__python} setup.py install -O1 \
                    --skip-build \
             --root %{buildroot}
popd

# Install config
%__install src/iustools.launchpad/config/plugins.d/launchpad.conf \
        %{buildroot}%{_sysconfdir}/ius-tools/plugins.d/launchpad.conf

%endif


# if condition meet build with ircbot
%if %{with ircbot}
pushd src/iustools.ircbot
%{__python} setup.py install -O1 \
		    --skip-build \
	     --root %{buildroot}
popd

# Install config
%__install src/iustools.ircbot/config/plugins.d/ircbot.conf \
	%{buildroot}%{_sysconfdir}/ius-tools/plugins.d/ircbot.conf

%endif

# if condition meet build with version_tracker
%if %{with version_tracker}
pushd src/iustools.version_tracker
%{__python} setup.py install -O1 \
		    --skip-build \
	     --root %{buildroot}
popd

# Install config
mkdir -p %{buildroot}%{_datadir}/ius-tools/version_tracker/pkgs/
%__install src/iustools.version_tracker/config/plugins.d/version_tracker.conf \
	%{buildroot}%{_sysconfdir}/ius-tools/plugins.d/version_tracker.conf

# version_tracker package configs
%__install src/iustools.version_tracker/pkgs/*.conf \
	%{buildroot}%{_datadir}/ius-tools/version_tracker/pkgs/

%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README
%dir %{_sysconfdir}/ius-tools/
%dir %{_sysconfdir}/ius-tools/plugins.d/
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/ius-tools/ius-tools.conf
%dir %{_datadir}/ius-tools/
%{_bindir}/ius
%{python_sitelib}/iustools.core-%{version}-py%{pyver}-nspkg.pth
%{python_sitelib}/iustools.core-%{version}-py%{pyver}.egg-info/
%dir %{python_sitelib}/iustools/bootstrap/
%dir %{python_sitelib}/iustools/controllers/
%dir %{python_sitelib}/iustools/helpers/
%dir %{python_sitelib}/iustools/lib/
%dir %{python_sitelib}/iustools/model/
%dir %{python_sitelib}/iustools/templates/
%dir %{python_sitelib}/iustools/templates/root/
%{python_sitelib}/iustools/bootstrap/root.py*
%{python_sitelib}/iustools/controllers/root.py*
%{python_sitelib}/iustools/core/
%{python_sitelib}/iustools/helpers/compare.py*
%{python_sitelib}/iustools/helpers/natsort.py*
%{python_sitelib}/iustools/lib/bitly.py*
%{python_sitelib}/iustools/lib/daemonize.py*
%{python_sitelib}/iustools/lib/testing_age.py*
%{python_sitelib}/iustools/model/root.py*
%{python_sitelib}/iustools/templates/root/__init__.py*
%{python_sitelib}/iustools/templates/root/error.txt
%{python_sitelib}/iustools/helpers/misc.py*
%{python_sitelib}/iustools/templates/root/api_error.txt

%if %{with admin}
%files admin
%defattr(-,root,root,-)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/ius-tools/plugins.d/admin.conf
%{python_sitelib}/iustools.admin-0.1.6-py2.4-nspkg.pth
%{python_sitelib}/iustools.admin-0.1.6-py2.4.egg-info/
%{python_sitelib}/iustools/bootstrap/admin.py*
%{python_sitelib}/iustools/controllers/admin.py*
%{python_sitelib}/iustools/helpers/smtp.py*
%{python_sitelib}/iustools/model/admin.py*
%{python_sitelib}/iustools/templates/admin/__init__.py*
%{python_sitelib}/iustools/templates/admin/admin_command.txt
%endif

%if %{with launchpad}
%files launchpad
%defattr(-,root,root,-)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/ius-tools/plugins.d/launchpad.conf
%{python_sitelib}/iustools.launchpad-0.1.6-py2.4-nspkg.pth
%{python_sitelib}/iustools.launchpad-0.1.6-py2.4.egg-info/
%{python_sitelib}/iustools/bootstrap/launchpad.py*
%{python_sitelib}/iustools/controllers/launchpad.py*
%{python_sitelib}/iustools/lib/launchpad.py*
%{python_sitelib}/iustools/model/launchpad.py*
%{python_sitelib}/iustools/templates/launchpad/__init__.py*
%endif

%if %{with version_tracker}
%files version_tracker
%defattr(-,root,root,-)
%dir %{_datadir}/ius-tools/version_tracker/
%config(noreplace) %attr(0640,root,root) %{_datadir}/ius-tools/version_tracker/pkgs/*.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/ius-tools/plugins.d/version_tracker.conf
%{python_sitelib}/iustools.version_tracker-%{version}-py%{pyver}-nspkg.pth
%{python_sitelib}/iustools.version_tracker-%{version}-py%{pyver}.egg-info/
%{python_sitelib}/iustools/bootstrap/version_tracker.py*
%{python_sitelib}/iustools/controllers/version_tracker.py*
%{python_sitelib}/iustools/lib/mf_identity.py*
%{python_sitelib}/iustools/lib/version_tracker.py*
%{python_sitelib}/iustools/model/version_tracker.py*
%{python_sitelib}/iustools/templates/version_tracker/
%endif

%if %{with ircbot}
%files ircbot
%defattr(-,root,root,-)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/ius-tools/plugins.d/ircbot.conf
%{python_sitelib}/iustools.ircbot-%{version}-py%{pyver}-nspkg.pth
%{python_sitelib}/iustools.ircbot-%{version}-py%{pyver}.egg-info
%{python_sitelib}/iustools/bootstrap/ircbot.py*
%{python_sitelib}/iustools/controllers/ircbot.py*
%{python_sitelib}/iustools/lib/ircbot.py*
%{python_sitelib}/iustools/model/ircbot.py*
%{python_sitelib}/iustools/templates/ircbot/
%endif

%changelog
* Wed Jun 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.6-1.ius
- Latest sources
- Adding admin and launchpad modules

* Tue Jun 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.4-4.ius
- Adding bconditions for subpackages

* Mon Jun 27 2011 BJ Dierkes <wdierkes@rackspace.com> - 0.1.4-3.ius
- Changed _datarootdir macro to _datadir

* Fri Jun 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.4-2.ius
- Installing configuration with each package
- Removing version_tracker for the time being
  this package requires Launchpad which many of the python requirements
  are not yet packaged

* Fri Jun 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.4-1.ius
- Latest sources

* Fri Jun 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.3-1.ius
- Latest sources

* Tue Jun 07 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.1.2-1.ius
- Initial spec

