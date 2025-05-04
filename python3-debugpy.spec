# TODO: unvendor pydevd? (then debugpy would be noarch)
#
Summary:	Implementation of the Debug Adapter Protocol for Python
Summary(pl.UTF-8):	Implementacja protokołu Debug Adapter Protocol dla Pythona
Name:		python3-debugpy
Version:	1.8.14
Release:	1
License:	MIT with EPL v1.0, PSF v2, BSD parts
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/debugpy/
Source0:	https://files.pythonhosted.org/packages/source/d/debugpy/debugpy-%{version}.tar.gz
# Source0-md5:	4155c8004de85f5f9b39c98fc940aba7
URL:		https://pypi.org/project/debugpy/
BuildRequires:	libstdc++-devel
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
debugpy is an implementation of the Debug Adapter Protocol for Python.

%description -l pl.UTF-8
debugpy to implementacja protokołu Debug Adapter Protocol dla Pythona.

%prep
%setup -q -n debugpy-%{version}

%build
cd src/debugpy/_vendored/pydevd/pydevd_attach_to_process/linux_and_mac
%ifarch %{ix86}
%{__cxx} -shared %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -fPIC -o ../attach_linux_x86.so attach.cpp
%endif
%ifarch %{x8664}
%{__cxx} -shared %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -fPIC -o ../attach_linux_amd64.so attach.cpp
%endif
cd ../../../../../..

%py3_build

%install
rm -rf $RPM_BUILD_ROOT

%py3_install \
	--install-lib=%{py3_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython*.{c,so}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/{.gitignore,pydevd_frame_evaluator.c,release_mem.h}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/{README.txt,common,linux_and_mac/{.gitignore,attach.cpp,compile_*},winappdbg,windows}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DESCRIPTION.md LICENSE README.md src/debugpy/ThirdPartyNotices.txt
%dir %{py3_sitedir}/debugpy
%dir %{py3_sitedir}/debugpy/_vendored
%dir %{py3_sitedir}/debugpy/_vendored/pydevd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydev_bundle
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydev_runfiles
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/_debug_adapter
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pxd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pyx
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/__pycache__
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_concurrency_analyser
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/vendored
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.pxd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.pyx
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/__pycache__
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_sys_monitoring
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_sys_monitoring/*.py
%attr(755,root,root) %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_sys_monitoring/*.so
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_sys_monitoring/__pycache__/*pydevd*
%{py3_sitedir}/debugpy/_vendored/pydevd/pydev_ipython
%{py3_sitedir}/debugpy/_vendored/pydevd/pydev_sitecustomize
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/attach_linux_*.so
%endif
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/linux_and_mac
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/__pycache__
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_plugins
%{py3_sitedir}/debugpy/_vendored/pydevd/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/__pycache__
%{py3_sitedir}/debugpy/_vendored/*.py
%{py3_sitedir}/debugpy/_vendored/__pycache__
%{py3_sitedir}/debugpy/adapter
%{py3_sitedir}/debugpy/common
%{py3_sitedir}/debugpy/launcher
%{py3_sitedir}/debugpy/server
%{py3_sitedir}/debugpy/*.py
%{py3_sitedir}/debugpy/__pycache__
%{py3_sitedir}/debugpy-%{version}-py*.egg-info
