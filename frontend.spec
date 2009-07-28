### RPM cms frontend 3.18
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rFRONTEND_CONF_3_18&output=/config.tar.gz
Source1: %cvsserver&module=COMP/WEBTOOLS/WelcomePages&export=htdocs&tag=-rFRONTEND_HTDOCS_1_2&output=/htdocs.tar.gz
Requires: apache2-conf mod_perl2 p5-apache2-modssl
Provides: perl(Compress::Zlib) perl(Digest::HMAC_SHA1)
Obsoletes: cms+frontend+3.17-cmp
Obsoletes: cms+frontend+3.16-cmp
Obsoletes: cms+frontend+3.15-cmp
Obsoletes: cms+frontend+3.14-cmp
Obsoletes: cms+frontend+3.13-cmp
Obsoletes: cms+frontend+3.12g-cmp
Obsoletes: cms+frontend+3.12f-cmp
Obsoletes: cms+frontend+3.12e-cmp
Obsoletes: cms+frontend+3.12d-cmp
Obsoletes: cms+frontend+3.12c-cmp
Obsoletes: cms+frontend+3.12b-cmp
Obsoletes: cms+frontend+3.12-cmp
Obsoletes: cms+frontend+3.11-cmp
Obsoletes: cms+frontend+3.10-cmp2
Obsoletes: cms+frontend+3.10-cmp
Obsoletes: cms+frontend+3.9-cmp

%prep
%setup -T -b 0 -n conf
%setup -D -T -b 1 -n htdocs

%build
%install
# Make directory for various resources of this package.
rm -fr %instroot/htdocs/*
rm -fr %instroot/apache2/*rewrites.d
rm -f %instroot/apache2/apps.d/*frontend.conf
rm -f %instroot/apache2/etc/startenv.d/01-mod_perl2.sh
rm -f %instroot/apache2/etc/startenv.d/02-p5-apache2-modssl.sh
rm -f %instroot/apache2/conf/testme
rm -f %instroot/apache2/*/CMSAuth.pm
rm -f %instroot/apache2/*/update-cookie-key
rm -f %instroot/apache2/*/update-and-sync-cookie-keys
rm -f %instroot/apache2/*/update-ca-files
rm -f %instroot/apache2/*/mkgridmap.conf
rm -f %instroot/apache2/*/voms-gridmap.txt

mkdir -p %instroot/apache2/apps.d
mkdir -p %instroot/apache2/rewrites.d
mkdir -p %instroot/apache2/ssl_rewrites.d
mkdir -p %instroot/apache2/var/cookie-keys
mkdir -p %instroot/apache2/htdocs
mkdir -p %instroot/apache2/auth

# Replace template variables in configuration files with actual paths.
perl -p -i -e "
  s|\@SERVER_ROOT\@|%instroot/apache2|g;
  s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;
  s|\@MOD_PERL2_ROOT\@|$MOD_PERL2_ROOT|g" \
  %_builddir/conf/*/*.conf

# Copy files to the server setup directory.
cp -p $MOD_PERL2_ROOT/etc/profile.d/init.sh %instroot/apache2/etc/startenv.d/01-mod_perl2.sh
cp -p $P5_APACHE2_MODSSL_ROOT/etc/profile.d/init.sh %instroot/apache2/etc/startenv.d/02-p5-apache2-modssl.sh
cp -p %_builddir/conf/testme %instroot/apache2/conf/
cp -p %_builddir/conf/CMSAuth.pm %instroot/apache2/conf/
cp -p %_builddir/conf/cms-centres.txt %instroot/apache2/etc/
cp -p %_builddir/conf/extra-certificates.txt %instroot/apache2/etc/
cp -p %_builddir/conf/mkgridmap.conf %instroot/apache2/etc/
cp -p %_builddir/conf/update-ca-files %instroot/apache2/etc/
cp -p %_builddir/conf/update-cookie-key %instroot/apache2/etc/
cp -p %_builddir/conf/update-and-sync-cookie-keys %instroot/apache2/etc/
cp -p %_builddir/conf/apps.d/*frontend.conf %instroot/apache2/apps.d/
cp -p %_builddir/conf/rewrites.d/*.conf %instroot/apache2/rewrites.d/
cp -p %_builddir/conf/ssl_rewrites.d/*.conf %instroot/apache2/ssl_rewrites.d/
cp -rp %_builddir/htdocs/* %instroot/apache2/htdocs/

touch %instroot/apache2/etc/voms-gridmap.txt

%post
# Relocate files.
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" \
  $RPM_INSTALL_PREFIX/apache2/*.d/*.conf \
  $RPM_INSTALL_PREFIX/apache2/etc/*.d/*.sh

# Deter attempts to modify installed files locally.
chmod a-w $RPM_INSTALL_PREFIX/apache2/*.d/*.conf
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/*.d/*.sh
chmod a-w $RPM_INSTALL_PREFIX/apache2/conf/testme
chmod a-wx $RPM_INSTALL_PREFIX/apache2/conf/CMSAuth.pm
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/update-ca-files
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/update-cookie-key
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/update-and-sync-cookie-keys

%files
%i/
%dir %instroot/apache2/var/cookie-keys
%dir %instroot/apache2/rewrites.d
%dir %instroot/apache2/ssl_rewrites.d
%dir %instroot/apache2/auth
%attr(444,-,-) %instroot/apache2/etc/startenv.d/01-mod_perl2.sh
%attr(444,-,-) %instroot/apache2/etc/startenv.d/02-p5-apache2-modssl.sh
%attr(555,-,-) %instroot/apache2/etc/update-ca-files
%attr(555,-,-) %instroot/apache2/etc/update-cookie-key
%attr(555,-,-) %instroot/apache2/etc/update-and-sync-cookie-keys
%config %instroot/apache2/etc/cms-centres.txt
%config %instroot/apache2/etc/extra-certificates.txt
%config %instroot/apache2/etc/voms-gridmap.txt
%config %attr(444,-,-) %instroot/apache2/etc/mkgridmap.conf
%config %attr(444,-,-) %instroot/apache2/apps.d/*frontend.conf
%config %attr(444,-,-) %instroot/apache2/rewrites.d/*.conf
%config %attr(444,-,-) %instroot/apache2/ssl_rewrites.d/*.conf
%config %attr(555,-,-) %instroot/apache2/conf/testme
%attr(444,-,-) %instroot/apache2/conf/CMSAuth.pm
%instroot/apache2/htdocs/*
