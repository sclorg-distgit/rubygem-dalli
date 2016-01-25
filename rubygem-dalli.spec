%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name dalli

# Depends on Rails and its needed by Rails
%global enable_test 0

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.7.4
Release: 3%{?dist}
Summary: High performance memcached client for Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/mperham/dalli
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
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
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{enable_test} > 0
pushd .%{gem_instdir}
# connection_pool is not yet in Fedora
sed -i -e '3d' test/test_active_support.rb
sed -i -e '491,506d' test/test_active_support.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e "Dir.glob('./test/test_*.rb').sort.each{ |x| require x }"
%{?scl:EOF}
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
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 2.7.4-3
- Rebuild for sclo-ror42 SCL

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Josef Stribny <jstribny@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-2
- Fix the test the right way

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> - 2.7.2-1
- Update to dalli 2.7.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-2
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.6.4-1
- Initial package
