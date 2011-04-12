### RPM external llvm 2.9rc3
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

# s/#/S/ to use the official version.
#ource0: http://llvm.org/releases/%realversion/llvm-%realversion.tgz
#ource1: http://llvm.org/releases/%realversion/clang-%realversion.tgz 
# SVN builds. Comment out to use the official version.
Source0: svn://llvm.org/svn/llvm-project/llvm/tags/RELEASE_29/rc3/?scheme=http&module=llvm-%realversion&output=/llvm-%realversion.tgz
Source1: svn://llvm.org/svn/llvm-project/cfe/tags/RELEASE_29/rc3/?scheme=http&module=clang-%realversion&output=/clang-%realversion.tgz
Patch0: llvm-2.9rc3-custom-gcc

%prep
%setup -T -b0 -n llvm-%realversion
%setup -T -D -a1 -c -n llvm-%realversion/tools
mv clang-%realversion clang
cd clang
case %cmsos in
  slc*)
%patch0 -p1
  ;;
esac
%setup -T -D -n llvm-%realversion

%build
mkdir objs ; cd objs
../configure --prefix=%i --enable-optimized
make %makeprocesses

%install
cd objs
make install
# Fix up a perl path
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/bin/llvm-config

case %cmsos in 
  osx*)
    #Fix up install names for some of the libraries.
    for x in BugpointPasses.dylib profile_rt.dylib LLVMHello.dylib
    do
      install_name_tool -change $x lib$x -id lib$x %i/lib/lib$x
    done
  ;;
esac
