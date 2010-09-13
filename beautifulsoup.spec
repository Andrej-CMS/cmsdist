### RPM external beautifulsoup 3.1.0.1
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://www.crummy.com/software/BeautifulSoup/download/3.1.x/BeautifulSoup-%{realversion}.tar.gz
Requires: python

%prep
%setup -n BeautifulSoup-%{realversion}
%build
%install
python setup.py install --prefix=%i 
