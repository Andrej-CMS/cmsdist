### RPM external py2-pymongo 1.11
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/p/pymongo/pymongo-%realversion.tar.gz
Requires: python elementtree py2-setuptools

%prep
%setup -n pymongo-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
