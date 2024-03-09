%global debug_package %{nil}

# Run tests in check section
%bcond_without check

# https://github.com/rs/zerolog
%global goipath		github.com/rs/zerolog
%global forgeurl	https://github.com/rs/zerolog
Version:		1.32.0

%gometa

Summary:	Zero Allocation JSON Logger for GO
Name:		golang-github-rs-zerolog

Release:	1
Source0:	https://github.com/rs/zerolog/archive/v%{version}/zerolog-%{version}.tar.gz
URL:		https://github.com/rs/zerolog
License:	MIT
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(github.com/coreos/go-systemd/v22/journal)
BuildRequires:	golang(github.com/mattn/go-colorable)
BuildRequires:	golang(github.com/pkg/errors)
BuildRequires:	golang(github.com/rs/xid)
BuildRequires:	golang(golang.org/x/tools/go/loader)

%description
The zerolog package provides a fast and simple logger
dedicated to JSON output.

Zerolog's API is designed to provide both a great developer
experience and stunning performance.  Its unique chaining API
allows zerolog to write JSON (or CBOR) log events by avoiding
allocations and reflection.

Uber's zap library pioneered this approach.  Zerolog is taking
this concept to the next level with a simpler to use API and
even better performance.

%files
%license LICENSE
%doc README.md
%{_bindir}/lint
%{_bindir}/prettylog

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n zerolog-%{version}

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
# journald test requires journald running
%gochecks -d journald
%endif

