# TODO: unvendor pydevd? (then debugpy would be noarch)
#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Implementation of the Debug Adapter Protocol for Python 2
Summary(pl.UTF-8):	Implementacja protokołu Debug Adapter Protocol dla Pythona 2
Name:		python-debugpy
Version:	1.3.0
Release:	2
License:	MIT with EPL v1.0, PSF v2, BSD parts
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/debugpy/
Source0:	https://files.pythonhosted.org/packages/source/d/debugpy/debugpy-%{version}.zip
# Source0-md5:	84900a0cbb80b172d75909b4edcbc736
URL:		https://pypi.org/project/debugpy/
BuildRequires:	libstdc++-devel
%if %{with python2}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
debugpy is an implementation of the Debug Adapter Protocol for Python.

%description -l pl.UTF-8
debugpy to implementacja protokołu Debug Adapter Protocol dla Pythona.

%package -n python3-debugpy
Summary:	Implementation of the Debug Adapter Protocol for Python 3
Summary(pl.UTF-8):	Implementacja protokołu Debug Adapter Protocol dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-debugpy
debugpy is an implementation of the Debug Adapter Protocol for Python.

%description -n python3-debugpy -l pl.UTF-8
debugpy to implementacja protokołu Debug Adapter Protocol dla Pythona.

%prep
%setup -q -n debugpy-%{version}

%{__rm} src/debugpy/_vendored/pydevd/pydevd_attach_to_process/*.{dll,dylib,exe,pdb,so}

%build
cd src/debugpy/_vendored/pydevd/pydevd_attach_to_process/linux_and_mac
%ifarch %{ix86}
%{__cxx} -shared %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -fPIC -o ../attach_linux_x86.so attach.cpp
%endif
%ifarch %{x8664}
%{__cxx} -shared %{rpmldflags} %{rpmcxxflags} %{rpmcppflags} -fPIC -o ../attach_linux_amd64.so attach.cpp
%endif
cd ../../../../../..

%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install \
	--install-lib=%{py_sitedir}

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/debugpy/ThirdPartyNotices.txt
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.{c,cpython-*.so}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/{.gitignore,pydevd_frame_evaluator.{c,cpython-*.so},release_mem.h}
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/{README.txt,common,linux_and_mac/{.gitignore,attach.cpp,compile_*},winappdbg,windows}
%endif

%if %{with python3}
%py3_install \
	--install-lib=%{py3_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/ThirdPartyNotices.txt
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.{c,so}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/{.gitignore,pydevd_frame_evaluator.c,release_mem.h}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/{README.txt,common,linux_and_mac/{.gitignore,attach.cpp,compile_*},winappdbg,windows}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc DESCRIPTION.md LICENSE README.md src/debugpy/ThirdPartyNotices.txt
%dir %{py_sitedir}/debugpy
%dir %{py_sitedir}/debugpy/_vendored
%dir %{py_sitedir}/debugpy/_vendored/pydevd
%{py_sitedir}/debugpy/_vendored/pydevd/_pydev_bundle
%{py_sitedir}/debugpy/_vendored/pydevd/_pydev_imps
%{py_sitedir}/debugpy/_vendored/pydevd/_pydev_runfiles
%dir %{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/_debug_adapter
%attr(755,root,root) %{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.so
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pxd
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pyx
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/*.py[co]
%dir %{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/vendored
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.pxd
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.py[co]
%{py_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.pyx
%{py_sitedir}/debugpy/_vendored/pydevd/pydev_ipython
%{py_sitedir}/debugpy/_vendored/pydevd/pydev_sitecustomize
%dir %{py_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{py_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/attach_linux_*.so
%endif
%{py_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/linux_and_mac
%{py_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/*.py[co]
%{py_sitedir}/debugpy/_vendored/pydevd/pydevd_concurrency_analyser
%{py_sitedir}/debugpy/_vendored/pydevd/pydevd_plugins
%{py_sitedir}/debugpy/_vendored/pydevd/*.py[co]
%{py_sitedir}/debugpy/_vendored/*.py[co]
%{py_sitedir}/debugpy/adapter
%{py_sitedir}/debugpy/common
%{py_sitedir}/debugpy/launcher
%{py_sitedir}/debugpy/server
%{py_sitedir}/debugpy/*.py[co]
%{py_sitedir}/debugpy-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-debugpy
%defattr(644,root,root,755)
%doc DESCRIPTION.md LICENSE README.md src/debugpy/ThirdPartyNotices.txt
%dir %{py3_sitedir}/debugpy
%dir %{py3_sitedir}/debugpy/_vendored
%dir %{py3_sitedir}/debugpy/_vendored/pydevd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydev_bundle
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydev_imps
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydev_runfiles
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/_debug_adapter
%attr(755,root,root) %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.cpython-*.so
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pxd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pyx
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_bundle/__pycache__
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/vendored
%attr(755,root,root) %{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.cpython-*.so
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.pxd
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/*.pyx
%{py3_sitedir}/debugpy/_vendored/pydevd/_pydevd_frame_eval/__pycache__
%{py3_sitedir}/debugpy/_vendored/pydevd/pydev_ipython
%{py3_sitedir}/debugpy/_vendored/pydevd/pydev_sitecustomize
%dir %{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/attach_linux_*.so
%endif
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/linux_and_mac
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/*.py
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_attach_to_process/__pycache__
%{py3_sitedir}/debugpy/_vendored/pydevd/pydevd_concurrency_analyser
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
%endif
