%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Summary: A graphical interface for configuring kernel crash dumping
Name: system-config-kdump
Version: 2.0.13
Release: 15%{?dist}
URL: http://fedorahosted.org/system-config-kdump/
License: GPLv2+
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source0: http://fedorahosted.org/released/system-config-kdump/%{name}-%{version}.tar.bz2
BuildRequires: desktop-file-utils
BuildRequires: intltool, gettext, gnome-doc-utils, docbook-dtds, rarian-compat, scrollkeeper
Requires: pygtk2 >= 2.8.6
Requires: pygtk2-libglade
Requires: usermode >= 1.36
Requires: kexec-tools
Requires: yelp
Requires: python-slip-dbus
Requires(pre): gtk2 >= 2.8.20
Requires(pre): hicolor-icon-theme
Requires(post): rarian-compat
Requires(postun): rarian-compat

# RHEL 7 is able to use auto option
# rhbz#859020
Patch1: system-config-kdump-2.0.13-enable_auto.patch

# Remove defunct GUI element
# rhbz#1011659
Patch2: system-config-kdump-2.0.13-remove_dump_format.patch

# Translation updates
# rhbz#1030379
Patch3: system-config-kdump-2.0.13-translation_updates.patch

# Broken Reload button
# rhbz#1052042
Patch4: system-config-kdump-2.0.13-fix_reload_button.patch

# Update default core_collector to use LZO compression
# rhbz#1047816
Patch5: system-config-kdump-2.0.13-core_collector_lzo.patch

# Translation updates 2
# rhbz#1011659
Patch6: system-config-kdump-2.0.13-translation_updates-2.patch

# Change misleading label in FS selection combobox
# rhbz#1061770
Patch7: system-config-kdump-2.0.13-partition_combobox.patch

# Fix broken FADump
# rhbz#1070305
Patch8: system-config-kdump-2.0.13-fadump.patch

# Set $PATH in backend so that zipl knows where to find dmsetup.
# rhbz#1077113
Patch9: system-config-kdump-2.0.13-backend_set_path.patch

# Move the application to System category in the desktop file
# rhbz#1078743
Patch10: system-config-kdump-2.0.13-desktop_category_system.patch

# Clarify NFS server input box
# rhbz#1208191
Patch11: system-config-kdump-2.0.13-nfs_server_label.patch

# Warn when NFS export target is not mounted
# rhbz#1121590
Patch12: system-config-kdump-2.0.13-nfs_warn_not_mounted.patch

# Translation updates 3
# rhbz#1294036
# rhbz#1303014
Patch13: system-config-kdump-2.0.13-translation_updates-3.patch

# Allow setting path even if no partition chosen
# rhbz#1131820
Patch14: system-config-kdump-2.0.13-root_partition_allow_path.patch

# Add check for nfs4 filesystem
# rhbz#1121590
Patch15: system-config-kdump-2.0.13-check_nfs4.patch

%description
system-config-kdump is a graphical tool for configuring kernel crash
dumping via kdump and kexec.

%prep
%setup -q
%patch1 -p1 -b .enable_auto
%patch2 -p1 -b .remove_dump_format
%patch3 -p2 -b .translation_updates
%patch4 -p1 -b .fix_reload_button
%patch5 -p1 -b .core_collector_lzo
%patch6 -p2 -b .translation_updates-2
%patch7 -p1 -b .partition_combobox
%patch8 -p1 -b .fadump
%patch9 -p1 -b .backend_set_path
%patch10 -p1 -b .desktop_category_system
%patch11 -p1 -b .nfs_server_label
%patch12 -p1 -b .nfs_warn_not_mounted
%patch13 -p1 -b .translation_updates-3
%patch14 -p1 -b .root_partition_path
%patch15 -p1 -b .check_nfs4

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor system --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/system-config-kdump.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi
%{_bindir}/scrollkeeper-update -q || :



%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/system-config-kdump
%{_datadir}/system-config-kdump
%{_datadir}/applications/*
%{python_sitelib}/*egg*
%{python_sitelib}/sckdump/

%config %{_sysconfdir}/security/console.apps/system-config-kdump
%config %{_sysconfdir}/pam.d/system-config-kdump
%config %{_sysconfdir}/dbus-1/system.d/org.fedoraproject.systemconfig.kdump.mechanism.conf

%{_datadir}/dbus-1/system-services/org.fedoraproject.systemconfig.kdump.mechanism.service
%{_datadir}/polkit-1/actions/org.fedoraproject.systemconfig.kdump.policy
%{_datadir}/icons/hicolor/48x48/apps/system-config-kdump.png

%doc ChangeLog COPYING
%doc %{_datadir}/gnome/help/system-config-kdump
%doc %{_datadir}/omf/system-config-kdump

%changelog
* Tue Sep 13 2016 Than Ngo <than@redhat.com> - 2.0.13-15
- Warn when NFS export target is not mounted, check nfs4 file system
- Resolves: #1121590

* Wed Jun 29 2016 Martin Milata <mmilata@redhat.com> - 2.0.13-14
- Allow setting path even if no partition chosen
- Resolves: #1131820

* Wed Jun 29 2016 Martin Milata <mmilata@redhat.com> - 2.0.13-13
- Translation updates
- Resolves: #1294036, #1303014

* Wed Jun 29 2016 Martin Milata <mmilata@redhat.com> - 2.0.13-12
- Warn when NFS export target is not mounted
- Resolves: #1121590

* Wed Jun 29 2016 Martin Milata <mmilata@redhat.com> - 2.0.13-11
- Clarify the meaning of the NFS server input box
- Resolves: #1208191

* Thu Mar 20 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-10
- Move the application to System category in the desktop file
- Resolves: #1078743

* Wed Mar 19 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-9
- Set PATH in backend so that zipl knows where to find dmsetup (affects only s390x)
- Resolves: #1077113

* Fri Feb 28 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-8
- Fix broken FADump handling
- Resolves: #1070305

* Wed Feb 12 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-7
- Change misleading label in FS selection combobox
- Resolves: #1061770

* Tue Jan 28 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-6
- Translation updates
- Resolves: #1011659

* Wed Jan 22 2014 Martin Milata <mmilata@redhat.com> - 2.0.13-5
- Fix broken Reload button
- Resolves: #1052042
- Update default core_collector to use LZO compression
- Resolves: #1047816

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.13-4
- Mass rebuild 2013-12-27

* Mon Dec 09 2013 Martin Milata <mmilata@redhat.com> - 2.0.13-3
- Translation updates
- Resolves: #1030379

* Wed Oct 16 2013 Martin Milata <mmilata@redhat.com> - 2.0.13-2
- Remove defunct file format radio buttons
- Resolves: #1011659

* Tue Jul 23 2013 Martin Milata <mmilata@redhat.com> - 2.0.13-1
- Update to 2.0.13
- New version incorporates several bugfixes and adds support for x86 EFI
  systems

* Thu Dec 13 2012 Roman Rakus <rrakus@redhat.com> - 2.0.10-3
- Use kdumpctl and systemctl instead of service command
- Default action changed so accordingly change also our message
- Configuration for nfs and ssh changed
  Resolves: #886321,#883769,#883638

* Wed Nov 28 2012 Roman Rakus <rrakus@redhat.com> - 2.0.10-2
- Rebuild with correct release tarball

* Wed Nov 28 2012 Roman Rakus <rrakus@redhat.com> - 2.0.10-1
- always enable auto option
- always use memory info from /proc/meminfo
- Resolves: #859096, #859020

* Tue Sep 11 2012 Roman Rakus <rrakus@redhat.com> - 2.0.9-1
- Update to 2.0.9

* Wed Aug 22 2012 Roman Rakus <rrakus@redhat.com> - 2.0.8-1
- Update to 2.0.8

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Roman Rakus <rrakus@redhat.com> - 2.0.7-1
- Update to 2.0.7

* Wed Feb 22 2012 Dan Horák <dan[at]danny.cz> - 2.0.5-8
- enable on s390x

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Roman Rakus <rrakus@redhat.com> - 2.0.5-6
- Another typo fixed

* Thu Sep 15 2011 Roman Rakus <rrakus@redhat.com> - 2.0.5-5
- Fix a bug in creating dialog

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Roman Rakus <rrakus@redhat.com> - 2.0.5-3
- Fix some typos (#649385)

* Fri Oct 01 2010 Roman Rakus <rrakus@redhat.com> - 2.0.5-2
- New icon (#540288)

* Thu Sep 30 2010 Roman Rakus <rrakus@redhat.com> - 2.0.5-1
- Release 2.0.5

* Sat Jul 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.4-7
- Rebuild for python-2.7

* Fri Jul 23 2010 Roman Rakus <rrakus@redhat.com> - 2.0.4-6
- Added missing patch

* Fri Jul 23 2010 Roman Rakus <rrakus@redhat.com> - 2.0.4-5
- Fix the nonassigned variable (#615001)
  Bumped release

* Wed Apr 21 2010 Roman Rakus <rrakus@redhat.com> - 2.0.4-3
- Do not require any fonts

* Fri Mar 26 2010 Roman Rakus <rrakus@redhat.com> - 2.0.4-2
- Use python_sitelib macro

* Fri Mar 26 2010 Roman Rakus <rrakus@redhat.com> - 2.0.4-1
- Release 2.0.4

* Fri Feb 26 2010 Roman Rakus <rrakus@redhat.com> 2.0.3-2
- bitmap-fonts is no more. Just try bitmap-fixed-fonts

* Tue Feb 02 2010 Roman Rakus <rrakus@redhat.com> 2.0.3-1
- update to 2.0.3. see changelog for more

* Mon Dec 07 2009 Roman Rakus <rrakus@redhat.com> - 2.0.2-1
- Don't be interested in non linux entries in bootloaders conf
  Resolves: #538850

* Wed Sep 30 2009 Roman Rakus <rrakus@redhat.com> - 2.0.1-1
- Update to version 2.0.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-2
- Added missing requires python-slip-dbus

* Tue May 05 2009 Roman Rakus <rrakus@redhat.com> - 2.0.0-1
- Changed to satisfy system config tools clenaup

* Mon Apr 13 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0.14-6
- Improve error handling when applying settings

* Mon Mar 23 2009 Roman Rakus <rrakus@redhat.com> - 1.0.14-5
- Fix off by one error in kernel command line parsing
  Resolves #334269

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.14-3
- Rebuild for Python 2.6

* Thu Sep 11 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-2
- Don't specify any offset in cmdline argument
  Resolves: #461602

* Tue Sep 09 2008 Roman Rakus <rrakus@redhat.com> 1.0.14-1
- Bump to version 1.0.14

* Fri Feb 01 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-2%{?dist}
- replace desktop file category "SystemSetup" with "Settings"

* Fri Jan 18 2008 Dave Lehman <dlehman@redhat.com> 1.0.13-1%{?dist}
- handle kdump service start/stop
  Resolves: rhbz#239324
- only suggest reboot if memory reservation altered
  Related: rhbz#239324
- preserve unknown config options
  Resolves: rhbz#253603
- add 'halt' default action
  Related: rhbz#253603

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-5%{?dist}
- fix license tag again

* Tue Oct 23 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-4%{?dist}
- fix desktop file in spec to avoid patching

* Mon Oct 22 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-3%{?dist}
- fix desktop file categories
- remove redhat-artwork requires

* Fri Oct 19 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-2%{?dist}
- change License to GPL2+

* Tue Sep 11 2007 Dave Lehman <dlehman@redhat.com> 1.0.12-1%{?dist}
- prompt user for a PAE kernel for 32-bit xen with >4G memory (Jarod Wilson)
  Resolves: rhbz#284851

* Wed Aug 29 2007 Dave Lehman <dlehman@redhat.com> 1.0.11-1%{?dist}
- add support for xen (patch from Jarod Wilson)
  Resolves: #243191

* Tue Jan 16 2007 Dave Lehman <dlehman@redhat.com> 1.0.10-1%{?dist}
- handle ia64 bootloader correctly
  Resolves: #220231
- align memory requirements with documented system limits
  Resolves: #228711

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-3%{?dist}
- only present ext2 and ext3 as filesystem type choices (#220223)

* Wed Dec 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-2%{?dist}
- make "Edit Location" button translatable (#216596, again)

* Mon Dec 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.9-1%{?dist}
- more translations
- use file: URIs instead of local: (#218878)

* Tue Dec  5 2006 Dave Lehman <dlehman@redhat.com> 1.0.8-1%{?dist}
- more translations (#216596)

* Wed Nov 29 2006 Dave Lehman <dlehman@redhat.com> 1.0.7-1%{?dist}
- rework memory constraints for increased flexibility (#215990)
- improve consistency WRT freezing/thawing of widgets (#215991)
- update translations (#216596)

* Fri Oct 27 2006 Dave Lehman <dlehman@redhat.com> 1.0.6-1%{?dist}
- add ChangeLog and COPYING as docs

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-3%{?dist}
- use %%{_sysconfdir} instead of /etc in specfile

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-2%{?dist}
- remove #!/usr/bin/python from system-config-kdump.py (for rpmlint)

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.5-1%{?dist}
- fix install make target to specify modes where needed
- remove unnecessary %%preun
- various specfile fixes to appease rpmlint

* Thu Oct 26 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-2
- fix path to icon in glade file

* Tue Oct 24 2006 Dave Lehman <dlehman@redhat.com> 1.0.4-1
- all location types now in combo box (no text entry for type)
- preserve comment lines from kdump.conf instead of writing config header
- add hicolor icon from Diana Fong

* Thu Oct 19 2006 Dave Lehman <dlehman@redhat.com> 1.0.3-1
- rework UI to only allow one location
- minor spec file cleanup

* Wed Oct 18 2006 Dave Lehman <dlehman@redhat.com> 1.0.2-1
- add support for "core_collector" and "path" handlers
- give choices of "ssh" and "nfs" instead of "net"
- validate results of edit location dialog
- add choice of "none" to default actions
- remove "ifc" support since it's gone from kexec-tools
- update kdump config file header
- fix a couple of strings that weren't getting translated

* Mon Oct 16 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-3
- Fix parsing of "crashkernel=..." string from /proc/cmdline

* Fri Oct 13 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-2
- convert crashkernel values to ints when parsing

* Tue Oct 10 2006 Dave Lehman <dlehman@redhat.com> 1.0.1-1
- Fix bugs in writeDumpConfig and writeBootloaderConfig
- Fix handling of pre-existing "ifc" and "default" directives
- Always leave network interface checkbutton sensitive
- Various minor fixes

* Fri Oct 06 2006 Dave Lehman <dlehman@redhat.com> 1.0.0-1
- Initial build

