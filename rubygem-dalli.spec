%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from dalli-2.6.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name dalli

# Depends on Rails and its needed by Rails
%global enable_test 1

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.6.4
Release: 4%{?dist}
Summary: High performance memcached client for Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/mperham/dalli
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
%if 0%{enable_test} > 0
BuildRequires: memcached
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(rails)
%endif
BuildRequires: %{?scl_prefix_ruby}ruby
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
High performance memcached client for Ruby

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{enable_test} > 0
pushd .%{gem_instdir}
%{?scl:scl enable %{scl} "}
testrb -Ilib test/test_*.rb
%{?scl:"}
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Performance.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/test

%changelog
* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.4-4
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-3
- Rebuild for scl

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-2
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-1
- Initial package
