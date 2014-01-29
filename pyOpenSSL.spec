### RPM external pyOpenSSL 0.6.900 
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages
## INITENV +PATH PATH %{i}/bin

Summary: A Python wrapper for OpenSSL
Group: Development/Libraries
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/%n-%v.tar.gz
Requires: python 
%prep
%setup -n %n-%{v}

%build
CFLAGS="-I$OPENSSL_ROOT/include -I$OPENSSL_ROOT/include/openssl" LDFLAGS="-L$OPENSSL_ROOT/lib" \
python setup.py build 

%install
python setup.py install --prefix=%i
