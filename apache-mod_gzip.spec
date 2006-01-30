%define		mod_name	gzip
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: On-the-fly compression of HTML documents
Summary(pl):	Modu³ do apache: kompresuje dokumenty HTML w locie
Name:		apache-mod_%{mod_name}
Version:	2.0.40
Release:	0.1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.gknw.com/development/apache/httpd-2.0/unix/modules/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	30c17d999edb5d83368369cde1c921bb
Source1:	%{name}.conf
Source2:	%{name}.logrotate
#URL:		http://www.schroepl.net/projekte/mod_gzip/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_pkglogdir	%(%{apxs} -q PREFIX 2>/dev/null)/logs

%description
Apache module: On-the-fly compression of HTML documents. Browser will
transparently decompress and display such documents.

%description -l pl
Modu³ do apache: kompresuje dokumenty HTML w locie. Przegl±darki w
sposób przezroczysty dekompresuj± i wy¶wietlaj± takie dokumenty.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -Wc,-Wall,-pipe -c mod_%{mod_name}.c mod_%{mod_name}_debug.c mod_%{mod_name}_compress.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf,/etc/logrotate.d,%{_pkglogdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

> $RPM_BUILD_ROOT%{_pkglogdir}/mod_gzip.log

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(640,root,root) %ghost %{_pkglogdir}/*
