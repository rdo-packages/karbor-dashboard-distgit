%global pypi_name karbor-dashboard
%global openstack_name karbor-ui

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?rhel} || 0%{?fedora}
%global rdo 1
%global http_dashboard_dir %{_datarootdir}/openstack-dashboard
%else
%global http_dashboard_dir /srv/www/openstack-dashboard
%endif

Name:           openstack-%{openstack_name}
Version:        XXX
Release:        XXX
Summary:        The Karbor Dashboard

License:        ASL 2.0
Url:            https://wiki.openstack.org/wiki/Karbor
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  fdupes
BuildRequires:  openstack-dashboard
BuildRequires:  openstack-macros
BuildRequires:  python-karborclient
BuildRequires:  python-pbr

Requires:       python-horizon-plugin-karbor-ui = %{version}

%description
The Karbor UI Horizon plugin adds Karbor panel to the OpenStack dashboard.

%package -n    python-horizon-plugin-karbor-ui
Summary:       The Karbor Dashboard - Python module
Requires:      python-babel
Requires:      python-django
Requires:      PyYAML
Requires:      python-django-babel
Requires:      python-django-compressor
Requires:      python-django-openstack-auth
Requires:      python-django-pyscss
Requires:      python-karborclient
Requires:      python-pbr

%description -n python-horizon-plugin-karbor-ui
The Karbor UI Horizon plugin adds Karbor panel to the OpenStack dashboard.

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
%py_req_cleanup

%build
%py2_build

%install
%py2_install

install -m 0755 -d %{buildroot}%{http_dashboard_dir}/openstack_dashboard/enabled/
cp -a karbor_dashboard/enabled/_60*.py %{buildroot}%{http_dashboard_dir}/openstack_dashboard/enabled/

%fdupes %{buildroot}%{python2_sitelib}
%fdupes %{buildroot}%{http_dashboard_dir}

%post
su %{apache_user} -s /bin/sh -c "python %{http_dashboard_dir}/manage.py collectstatic --noinput --clear > /dev/null"

%postun
su %{apache_user} -s /bin/sh -c "python %{http_dashboard_dir}/manage.py collectstatic --noinput --clear > /dev/null"

%files
%doc ChangeLog CONTRIBUTING.rst README.rst
%license LICENSE
%{http_dashboard_dir}/openstack_dashboard/enabled/*.py

%files -n python-horizon-plugin-karbor-ui
%doc README.rst
%license LICENSE
%{python2_sitelib}/karbor_dashboard
%{python2_sitelib}/karbor_dashboard-*.egg-info
%exclude %{http_dashboard_dir}/openstack_dashboard/enabled/*.pyc
%exclude %{http_dashboard_dir}/openstack_dashboard/enabled/*.pyo

%changelog
