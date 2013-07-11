%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Name:           mod_authnz_crowd
Version:        2.0.2
Release:        2%{?dist}
Summary:        Modules for integrating Apache httpd and Subversion with Atlassian Crowd

License:        Apache License, Version 2.0
URL:            http://www.atlassian.com/software/crowd/
Source0:        %{name}-%{version}.tar.gz
Source1:        10-%{name}.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf automake curl-devel httpd-devel libtool libxml2-devel subversion-devel
#Requires:       curl httpd-devel libtool libxml2 mod_dav_svn
Requires:       libcurl libxml2 mod_dav_svn
Requires:       httpd-mmn = %{_httpd_mmn}

Group:          Networking/WWW

%description
Modules for Apache httpd that allow Atlassian Crowd to be used for the authentication and authorisation of HTTP and Subversion requests

%prep
%setup

%build
aclocal
autoreconf --install
%configure
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_httpd_confdir}
mkdir -p %{buildroot}%{_httpd_moddir}

install -d -m 0755 %{buildroot}%{_httpd_confdir}
install -Dp -m644 %{SOURCE1} %{buildroot}%{_httpd_confdir}/10-%{name}.conf

install -m 755 src/.libs/%{name}.so %{buildroot}%{_httpd_moddir}
install -m 755 src/svn/.libs/mod_authz_svn_crowd.so %{buildroot}%{_httpd_moddir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_libdir}/httpd/modules/mod_authnz_crowd.so
%{_libdir}/httpd/modules/mod_authz_svn_crowd.so
%config(noreplace) %{_httpd_confdir}/*.conf
%doc LICENSE


%changelog
* Thu Jul 11 2013 julien.tognazzi@swissinfo.ch 2.0.2-1
- Spec clean up
