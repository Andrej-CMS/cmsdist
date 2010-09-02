### RPM external oracle 100.0
## INITENV SET ORACLE_HOME %i
## INITENV +PATH SQLPATH %i/bin

# Notice that we have a dummy package version because the mac and linux clients
# are not in sync. Moreover, because it's a binary only package we need to
# point to different tarballs for different architecture.
# Do not even think about commenting out one of the sources, simply because
# it's not needed for your platform.
# Also notice that even if LCG provides a tarball named without references
# to CMS architecture, we need to have a -%%cmsos suffix in order to
# avoid that one overwrites the other.
%define macversion 10.2.0.4.0
%define linuxversion 11.2.0.1.0p2
Source0: http://cmsrep.cern.ch/cmssw/oracle-mirror/slc5_amd64/%{linuxversion}/oracle_lcg-slc5_amd64.tgz
Source1: http://cmsrep.cern.ch/cmssw/oracle-mirror/slc5_ia32/%{linuxversion}/oracle_lcg-slc5_ia32.tgz
Source2: http://cmsrep.cern.ch/cmssw/oracle-mirror/osx106_amd64/%{macversion}/oracle_lcg-osx106_amd64.tgz
Source9: oracle-license
Requires: fakesystem 

%prep

# We unpack only the sources for the architecture we are working on.  Do not
# change this to unpack all the architectures.  Notice also that you cannot put
# ;; on the same line as the %%setup macro, because the latter will swallow it
# as part of the arguments.
case %cmsos in
  slc5_amd64)
%setup -T -n %linuxversion -b 0 
  ;;
  slc5_ia32)
%setup -T -n %linuxversion -b 1 
  ;;
  osx106_amd64)
%setup -T -n %macversion -b 2 
  ;;
  *)
echo "Unsupported platform "%cmsos". Please put the oracle \
client tarball for this architecture in \
cmsrep.cern.ch:/data/cmssw/oracle-mirror/%cmsos \
and update the spec file accordingly." ; exit 1 ;; 
esac

%build

%install
mkdir -p %i/bin %i/lib %i/doc %i/include
cp %_sourcedir/oracle-license %{i}/oracle-license
cp -r bin/* %i/bin/
cp -r lib/* %i/lib/
cp -r doc/* %i/doc/
cp -r include/* %i/include/

case %cmsplatf in
  osx* )
    ln -sf libclntsh.dylib.10.1 %i/lib/libclntsh.dylib
    ln -sf libocci.dylib.10.1 %i/lib/libocci.dylib
  ;;
esac
