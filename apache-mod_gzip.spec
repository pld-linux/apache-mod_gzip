%define		mod_name	gzip
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: On-the-fly compression of HTML documents
Summary(pl.UTF-8):	Moduł do apache: kompresuje dokumenty HTML w locie
Name:		apache-mod_%{mod_name}
Version:	2.1.0
Release:	0.1
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	http://www.gknw.net/development/apache/httpd-2.0/unix/modules/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	9011aa2dc4701c0301e6c608269f8835
Source1:	%{name}.conf
URL:		http://www.gknw.net/development/apache/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: On-the-fly compression of HTML documents. Browser will
transparently decompress and display such documents.

%description -l pl.UTF-8
Moduł do apache: kompresuje dokumenty HTML w locie. Przeglądarki w
sposób przezroczysty dekompresują i wyświetlają takie dokumenty.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf
install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc *.txt logos/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
