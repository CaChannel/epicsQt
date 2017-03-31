%define name python-epicsQt
%define version 1.0.0
%define release 1

Summary: Qt widgets with epics
Name: %{name}
Version: %{version}
Release: %{release}
Source0: epicsQt-%{version}.tar.gz
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Xiaoqiang Wang <xiaoqiangwang@gmail.com>
Requires: PyQt4 python-CaChannel
Url: http://github.com/CaChanel/epicsQt/

%description
epicsQt
=======

`epicsQt` is a QObject representing an EPICS PV connection.

Based on it there is a set of PyQt widgets which has epics awareness.
They are here to integrate epics into existing PyQt applications.

+--------------+----------------+
| Widget type  |  Description   |
+==============+================+
| eButton      | Push button    |
+--------------+----------------+
| eButtonGroup | Choice button  |
+--------------+----------------+
| eCheckbox    | Boolean button |
+--------------+----------------+
| eCombo       | Choice menu    |
+--------------+----------------+
| eDoubleSpin  | Numeric input  |
+--------------+----------------+
| eIntSpin     | Integer input  |
+--------------+----------------+
| eLCD         | Integer dislay |
+--------------+----------------+
| eLabel       | Text display   |
+--------------+----------------+
| eTextEdit    | Text input     |
+--------------+----------------+

Their designer plugins can be used, if PyQt installed,
    $ export PYQTDESIGNERPATH=<epicsQt>/plugin/



%prep
%setup -n epicsQt-%{version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
