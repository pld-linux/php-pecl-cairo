%define		modname	cairo
%define		status		alpha
Summary:	Cairo Graphics Library Extension
Summary(pl.UTF-8):	Rozszerzenie biblioteki Cairo
Name:		php-pecl-%{modname}
Version:	0.2.0
Release:	4
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/Cairo-%{version}.tgz
# Source0-md5:	e35ac0eda37e5cd4370858aebe08f0f8
URL:		http://pecl.php.net/package/Cairo/
BuildRequires:	cairo-devel
BuildRequires:	php-devel >= 3:5.0.4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	which
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cairo is a 2D graphics library with support for multiple output
devices. Currently supported output targets include the X Window
System, Quartz, Win32, image buffers, PostScript, PDF, and SVG file
output.

In PECL status of this extension is: %{status}.

%package devel
Summary:	Header files for Cairo PECL extension
Group:		Development/Libraries
# does not require base
Requires:	php-devel >= 3:5.0.4

%description devel
Header files for Cairo PECL extension.

%prep
%setup -qc
mv Cairo-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README SYMBOLS TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files devel
%defattr(644,root,root,755)
%dir %{php_includedir}/ext/cairo
%{php_includedir}/ext/cairo/php_cairo_api.h
