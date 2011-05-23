### RPM external py2-cjson 1.0.5
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages

Source: http://pypi.python.org/packages/source/p/python-cjson/python-cjson-%{realversion}.tar.gz
Requires: python

%prep
%setup -n python-cjson-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
