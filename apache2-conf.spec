### RPM cms apache2-conf 2.2f
# Configuration for additional apache2 modules
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true
Source0: %cvsserver&module=COMP/WEBTOOLS/Configuration&export=conf&tag=-rSERVER_CONF_2_2&output=/config.tar.gz
Requires: apache2
Obsoletes: cms+apache2-conf+2.2e-cmp
Obsoletes: cms+apache2-conf+2.2d-cmp
Obsoletes: cms+apache2-conf+2.2c-cmp
Obsoletes: cms+apache2-conf+2.2b-cmp
Obsoletes: cms+apache2-conf+2.2-cmp

%prep
%setup -T -b 0 -n conf

%build

%install
# Make directory for various resources of this package.
rm -f %instroot/apache2/etc/startenv.d/00-core-server.sh
rm -f %instroot/apache2/etc/init.d/httpd
rm -f %instroot/apache2/etc/archive-log-files
rm -f %instroot/apache2/conf/apache2.conf

mkdir -p %i/bin
mkdir -p %instroot/apache2/apps.d
mkdir -p %instroot/apache2/htdocs
mkdir -p %instroot/apache2/conf
mkdir -p %instroot/apache2/logs
mkdir -p %instroot/apache2/var
mkdir -p %instroot/apache2/etc/init.d
mkdir -p %instroot/apache2/etc/startenv.d

# Replace template variables in configuration files with actual paths.
perl -p -i -e "s|\@SERVER_ROOT\@|%instroot/apache2|g;s|\@APACHE2_ROOT\@|$APACHE2_ROOT|g;" %_builddir/conf/apache2.conf

# Generate dependencies-setup.{sh,csh}.
rm -fr %i/etc/profile.d
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`; do
  eval toolroot=\$$(echo $tool | tr a-z- A-Z_)_ROOT
  if [ X"${toolroot:+set}" = Xset ] && [ -d "$toolroot" ]; then
    echo ". $toolroot/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "source $toolroot/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

# Generate server startup script.
sed "s/^  //; s|@APACHE2_ROOT@|$APACHE2_ROOT|g" << \EOF > %instroot/apache2/etc/init.d/httpd
  #!/bin/bash
  # chkconfig: - 85 15
  # description: CMS custom web server.
  # processname: httpd
  # config: %instroot/apache2/conf/apache2.conf
  # pidfile: %instroot/apache2/var/httpd.pid

  # Source function library.
  . /etc/rc.d/init.d/functions

  # Source run time environment.
  for file in %instroot/apache2/etc/startenv.d/*.sh; do
    [ -f $file ] || continue
    . $file
  done

  # Set server options.
  OPTIONS="-f %instroot/apache2/conf/apache2.conf"
  OPTIONS="$OPTIONS $(cat %instroot/apache2/conf/server-opts.txt)"

  # Path to the server binary, and short-form for messages.
  prog=httpd
  httpd=@APACHE2_ROOT@/bin/httpd
  pidfile=%instroot/apache2/var/httpd.pid
  lockfile=%instroot/apache2/var/httpd.lock
  RETVAL=0

  # The semantics of these two functions differ from the way apachectl does
  # things -- attempting to start while running is a failure, and shutdown
  # when not running is also a failure.  So we just do it the way init scripts
  # are expected to behave here.
  start() {
    echo -n $"Starting $prog: "
    LANG=C daemon $httpd $OPTIONS
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && touch ${lockfile}
    return $RETVAL
  }
  stop() {
    echo -n $"Stopping $prog: "
    killproc $httpd
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && rm -f ${lockfile} ${pidfile}
  }
  reload() {
    echo -n $"Reloading $prog: "
    if ! LANG=C $httpd $OPTIONS -t >&/dev/null; then
      RETVAL=$?
      echo $"not reloading due to configuration syntax error"
      failure $"not reloading $httpd due to configuration syntax error"
    else
      killproc $httpd -HUP
      RETVAL=$?
    fi
    echo
  }
  status() {
    local base=${1##*/}
    local pid

    # First try "pidof"
    pid=`pidof -o $$ -o $PPID -o %PPID -x $1 || \
         pidof -o $$ -o $PPID -o %PPID -x ${base}`
    if [ -n "$pid" ]; then
      echo $"${base} (pid $pid) is running..."
      return 0
    fi

    # Next try "*.pid" files
    if [ -f $pidfile ] ; then
      read pid < $pidfile
      if [ -n "$pid" ]; then
        echo $"${base} dead but pid file exists"
        return 1
      fi
    fi

    # See if $lockfile exists
    if [ -f $lockfile ]; then
      echo $"${base} dead but subsys locked"
      return 2
    fi
    echo $"${base} is stopped"
    return 3
  }

  
  # See how we were called.
  case "$1" in
    start)
      start
      ;;
    stop)
      stop
      ;;
    status)
      status $httpd
      RETVAL=$?
      ;;
    restart)
      stop
      start
      ;;
    condrestart)
      if [ -f ${pidfile} ] ; then
        stop
        start
      fi
      ;;
    reload)
      reload
      ;;
    graceful)
      LANG=C $httpd $OPTIONS -k $@
      RETVAL=$?
      ;;
    configtest)
      LANG=C $httpd $OPTIONS -t
      RETVAL=$?
      ;;
    help)
      LANG=C $httpd $OPTIONS $@
      RETVAL=$?
      ;;
    fullstatus)
      ${LYNX-"lynx -dump"} ${STATUSURL-"http://localhost:80/server-status"}
      ;;
    *)
      echo $"Usage: $prog {start|stop|restart|condrestart|reload|status|fullstatus|graceful|help|configtest}"
      exit 1
  esac

  exit $RETVAL
EOF

# Create server options file.
echo "-DPRODUCTION" > %instroot/apache2/conf/server-opts.txt

# Copy files to the server setup directory.
cp -p %_builddir/conf/apache2.conf %instroot/apache2/conf/
cp -p %_builddir/conf/archive-log-files %instroot/apache2/etc/
cp -p %i/etc/profile.d/dependencies-setup.sh %instroot/apache2/etc/startenv.d/00-core-server.sh

%post
# Relocate files.
CFG=$RPM_INSTALL_PREFIX/apache2/conf
perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g"	\
  $RPM_INSTALL_PREFIX/%pkgrel/etc/profile.d/*-*.*sh	\
  $RPM_INSTALL_PREFIX/apache2/conf/apache2.conf		\
  $RPM_INSTALL_PREFIX/apache2/etc/init.d/httpd		\
  $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/00-core-server.sh

# Set ServerName.
H=$(hostname -f)
if [ -r /etc/grid-security/hostcert.pem ]; then
  CN=$(openssl x509 -noout -subject -in /etc/grid-security/hostcert.pem 2>/dev/null | sed 's|.*/CN=||')
  case $CN in *.*.* ) H=$CN ;; esac
fi

echo "Adjusting ServerName to $H."
perl -p -i -e 's/^ServerName (\S+)$/ServerName '$H'/g' $CFG/apache2.conf

# Deter attempts to modify installed files locally.
chmod a-w $RPM_INSTALL_PREFIX/apache2/conf/apache2.conf
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/archive-log-files
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/init.d/httpd
chmod a-w $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/00-core-server.sh

%files
%i/
%dir %instroot/apache2
%dir %instroot/apache2/etc
%dir %instroot/apache2/etc/init.d
%dir %instroot/apache2/etc/startenv.d
%dir %instroot/apache2/var
%dir %instroot/apache2/logs
%dir %instroot/apache2/conf
%dir %instroot/apache2/htdocs
%dir %instroot/apache2/apps.d
%attr(444,-,-) %config %instroot/apache2/conf/apache2.conf
%attr(444,-,-) %instroot/apache2/etc/startenv.d/00-core-server.sh
%attr(555,-,-) %instroot/apache2/etc/init.d/httpd
%attr(555,-,-) %instroot/apache2/etc/archive-log-files
%config %instroot/apache2/conf/server-opts.txt
