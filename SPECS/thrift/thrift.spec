%define without_java 1
%define without_python 1
%define without_tests 1
%define without_ruby 1
%define without_php 1
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
Name:           thrift
License:        Apache License v2.0
Group:          Development
Summary:        RPC and serialization framework
Version:        0.19.0
Release:        0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

URL:            http://thrift.apache.org
Packager:       Thrift Developers <dev@thrift.apache.org>
Source0:        https://dlcdn.apache.org/thrift/%{version}/thrift-%{version}.tar.gz


BuildRequires:  gcc >= 3.4.6
BuildRequires:  gcc-c++
%if 0%{!?without_java:1}
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
%endif
%if 0%{!?without_python:1}
BuildRequires:  python-devel
%endif
%if 0%{!?without_ruby:1}
%define gem_name %{name}
BuildRequires:  ruby-devel
BuildRequires:  rubygems-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Smalltalk, Erlang, OCaml, Haskell, and
other languages.
%files
%defattr(-,root,root)
%{_bindir}/thrift
%package lib-cpp
Summary: Thrift C++ library
Group:   Libraries
%description lib-cpp
C++ libraries for Thrift.
%files lib-cpp
%defattr(-,root,root)
%{_libdir}/libthrift*.so.*
%{_libdir}/libthrift*.so
%package lib-cpp-devel
Summary:   Thrift C++ library development files
Group:     Libraries
Requires:  %{name} = %{version}-%{release}
Requires:  boost-devel
%if 0%{!?without_libevent:1}
Requires:  libevent-devel >= 1.2
%endif
%if 0%{!?without_zlib:1}
Requires:  zlib-devel
%endif
%description lib-cpp-devel
C++ static libraries and headers for Thrift.
%files lib-cpp-devel
%defattr(-,root,root)
%{_includedir}/thrift/
%{_libdir}/libthrift*.*a
%{_libdir}/pkgconfig/thrift*.pc
%if 0%{!?without_java:1}
%package lib-java
Summary:   Thrift Java library
Group:     Libraries
Requires:  java >= 0:1.5.0
%description lib-java
Java libraries for Thrift.
%files lib-java
%defattr(-,root,root)
%{_javadir}/*
%endif
%if 0%{!?without_python:1}
%package lib-python
Summary: Thrift Python library
Group:   Libraries
%description lib-python
Python libraries for Thrift.
%files lib-python
%defattr(-,root,root)
%{python_sitearch}/*
%endif
%if 0%{!?without_ruby:1}
%package -n rubygem-%{gem_name}
Summary: Thrift Ruby library
Group:   Libraries
%description -n rubygem-%{gem_name}
Ruby libraries for Thrift.
%files -n rubygem-%{gem_name}
%defattr(-,root,root)
%{gem_dir}/*
%endif
%if 0%{!?without_php:1}
%package lib-php
Summary: Thrift PHP library
Group:   Libraries
%description lib-php
PHP libraries for Thrift.
%files lib-php
%defattr(-,root,root)
/usr/lib/php/*
%endif
%prep
%setup -q
%build
[[ -e Makefile.in ]] || ./bootstrap.sh
export GEM_HOME=${PWD}/.gem-home
export RUBYLIB=${PWD}/lib/rb/lib
%configure \
  %{?without_libevent: --without-libevent } \
  %{?without_zlib:     --without-zlib     } \
  %{?without_tests:    --without-tests    } \
  %{?without_java:     --without-java     } \
  %{?without_python:   --without-python   } \
  %{?without_ruby:     --without-ruby     } \
  %{?without_php:      --without-php      } \
  %{!?without_php:     PHP_PREFIX=${RPM_BUILD_ROOT}/usr/lib/php } \
  --without-erlang 

%if 0%{!?without_ruby:1}
eval $(grep "^WITH_RUBY_TRUE" config.log)
if [[ "${WITH_RUBY_TRUE}" != "" ]]; then
  set +x
  echo ""
  echo "configure determined that ruby requirements are missing (bundler gem?), either install missing components" >&2
  echo "or disable the ruby sub-packages as follows:"                                                              >&2
  echo "     rpmbuild -D'%without_ruby 1' ..."                                                                     >&2
  echo ""
  exit 1
fi
%endif

make %{?_smp_mflags}
%if 0%{!?without_java:1}
cd lib/java
%ant
cd ../..
%endif

%if 0%{!?without_python:1}
cd lib/py
CFLAGS="%{optflags}" %{__python} setup.py build
cd ../..
%endif

%if 0%{!?without_ruby:1}
%gem_install -n lib/rb/thrift*.gem
%endif

%install
export GEM_HOME=${PWD}/.gem-home
export RUBYLIB=${PWD}/lib/rb/lib



%makeinstall
%if 0%{!?without_java:1}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/java/build/*.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%if 0%{!?without_python:1}
cd lib/py
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cd ../..
%endif

%if 0%{!?without_ruby:1}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
%endif



%clean
rm -rf ${RPM_BUILD_ROOT}

%post
umask 007
/sbin/ldconfig > /dev/null 2>&1

%postun
umask 007
/sbin/ldconfig > /dev/null 2>&1


%changelog
* Wed Aug 21 2013 Thrift Dev <dev@thrift.apache.org>
- Thrift 0.9.1 release.
* Wed Oct 10 2012 Thrift Dev <dev@thrift.apache.org> 
- Thrift 0.9.0 release.