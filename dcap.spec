### RPM external dcap 2.47.5.0
#get dcap from dcache svn repo now...
Source: http://cmsrep.cern.ch/cmssw/download/dcap/dcap.tgz
#Source: svn://svn.dcache.org/dCache/tags/dcap-2.47.5-0?scheme=http&module=dcap&output=/dcap.tgz
Patch0: dcap-2.47.5.0-macosx

# Unfortunately I could not find any rpm version invariant way to do and "if
# else if", so I ended up hardcoding all the possible variants.
# FIXME: move to multiple ifs once rpm 4.4.2.2 is deprecated.
Provides: libdcap.so
Provides: libpdcap.so
Provides: libdcap.so()(64bit)
Provides: libpdcap.so()(64bit)
Provides: libdcap.dylib
Provides: libpdcap.dylib

%prep
%setup -n dcap
# THIS PATCH IS COMPLETELY UNTESTED AND HAS THE SOLE PURPOSE OF BUILDING STUFF
# ON MAC, REGARDLESS WHETHER IT WORKS OR NOT. It is however safe to include,
# since every change is ifdeffed with __APPLE__.
%patch0 -p1

%build
# Since we are using the checked out code, we need to regenerate the auto-tools
# crap.
case %cmsos in
  osx*) LIBTOOLIZE=glibtoolize ;;
  slc*) LIBTOOLIZE=libtoolize ;;
esac
mkdir -p config
aclocal -I config
autoheader
$LIBTOOLIZE --automake
automake --add-missing --copy --foreign
autoconf
./configure --prefix %i

# We don't care about the plugins and other stuff and build only the source.
make -C src %makeprocesses
%install
make -C src install
