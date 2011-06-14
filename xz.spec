### RPM external xz 5.0.3
Source: http://tukaani.org/%n/%n-%realversion.tar.bz2

%prep
%setup -n %n-%realversion
perl -p -i -e '/LZMA_PROG_ERROR\s+=/ && s/,$//' src/liblzma/api/lzma/base.h

%build
./configure CFLAGS='-fPIC' --prefix=%i
make %makeprocesses

%install
make %makeprocesses install
