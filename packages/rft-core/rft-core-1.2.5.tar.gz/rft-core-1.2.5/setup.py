import subprocess
import collections
import json
import sys
import os

required_packages=collections.OrderedDict()

required_packages["atomicwrites"]="==1.3.0"
required_packages["attrs"]="==19.1.0"
required_packages["backports.functools-lru-cache"]="==1.5"
required_packages["colorama"]="==0.4.1"
required_packages["configparser"]="==3.7.4"
required_packages["contextlib2"]="==0.5.5"
required_packages["cryptography"]="==2.7"
required_packages["enum34"]="==1.1.6"
required_packages["funcsigs"]="==1.0.2"
required_packages["future"]="==0.17.1"
required_packages["importlib-metadata"]="==0.18"
required_packages["more-itertools"]="==5.0.0"
required_packages["MouseInfo"]="==0.0.4"
required_packages["packaging"]="==19.0"
required_packages["pexpect"]="==4.7.0"
required_packages["pluggy"]="==0.12.0"
required_packages["ply"]="==3.11"
required_packages["ptyprocess"]="==0.6.0"
required_packages["py"]="==1.8.0"
required_packages["PyAutoGUI"]="==0.9.47"
required_packages["PyGetWindow"]="==0.0.7"
required_packages["PyMsgBox"]="==1.0.7"
required_packages["pyparsing"]="==2.4.0"
required_packages["pyperclip"]="==1.7.0"
required_packages["PyRect"]="==0.1.4"
required_packages["PyScreeze"]="==0.1.22"
required_packages["pytest"]="==4.6.3"
required_packages["pytool"]="==3.15.0"
required_packages["PyTweening"]="==1.0.3"
required_packages["pytz"]="==2019.1"
required_packages["scandir"]="==1.10.0"
required_packages["scp"]="==0.13.2"
required_packages["setuptools"]="==42.0.2"
required_packages["simplejson"]="==3.16.0"
required_packages["soupsieve"]="==1.9.1"
required_packages["text-unidecode"]="==1.2"
required_packages["urllib3"]="==1.24.3"
required_packages["waitress"]="==1.3.0"
required_packages["wcwidth"]="==0.1.7"
required_packages["WebOb"]="==1.8.5"
required_packages["WebTest"]="==2.0.33"
required_packages["wheel"]="==0.33.4"
required_packages["wrapt"]="==1.11.2"
required_packages["zope.interface"]="==4.6.0"
required_packages['zipp']="==0.6.0"
required_packages['pillow']="==6.2.2"
required_packages['setuptools']="==42.0.2"
required_packages['influx-client']="==1.9"
required_packages['pytest']="<5.0.0"
required_packages['requests']="==2.22.0"
required_packages['adodbapi']="==2.6.0.7"
required_packages['asn1crypto']="==0.24.0"
required_packages['bcrypt']="==3.1.6"
required_packages['beautifulsoup4']="==4.7.1"
required_packages['certifi']="==2019.3.9"
required_packages['cffi']="==1.12.3"
required_packages['chardet']="==3.0.4"
required_packages['chromedriver']="==2.24.1"
required_packages['collections2']="==0.3.0"
required_packages['cx-oracle']="==7.1.3"
required_packages['datetime']="==4.3"
required_packages['decorator']="==4.4.0"
required_packages['dialogs']="==0.14"
required_packages['docutils']="==0.14"
required_packages['et_xmlfile']="==1.0.1"
required_packages['faker']="==1.0.7"
required_packages['idna']="==2.8"
required_packages['ipaddress']="==1.0.22"
required_packages['jdcal']="==1.4.1"
required_packages['jenkinsapi']="==0.3.9"
required_packages['jsonpatch']="==1.23"
required_packages['jsonpointer']="==2.0"
required_packages['ldap3']="==2.6"
required_packages['lxml']="==4.3.3"
required_packages['multi-key-dict']="==2.0.3"
required_packages['natsort']="==6.0.0"
required_packages['openpyxl']="==2.6.2"
required_packages['paramiko']="==2.4.2"
required_packages['pathlib2']="==2.3.3"
required_packages['pbr']="==5.2.0"
required_packages['pyasn1']="==0.4.5"
required_packages['pyasn1-modules']="==0.2.5"
required_packages['pycparser']="==2.19"
required_packages['pycryptodome']="==3.8.1"
required_packages['pygments']="==2.4.0"
required_packages['pymysql']="==0.9.3"
required_packages['pynacl']="==1.3.0"
required_packages['pyopenssl']="==19.0.0"
required_packages['pypubsub']="==3.3.0"
required_packages['pyrfc']="==0.1.2"
required_packages['python-dateutil']="==2.8.0"
required_packages['python-jenkins']="==1.4.0"
required_packages['robotframework']="==3.1.1"
required_packages['robotframework-archivelibrary']="==0.4.0"
required_packages['robotframework-databaselibrary']="==1.2"
required_packages['robotframework-excellib']="==1.1.0"
required_packages['robotframework-faker']="==4.2.0"
required_packages['robotframework-httplibrary3']="==0.6.0"
required_packages['robotframework-pabot']="== 0.86"
required_packages['robotframework-requests']="==0.5.0"
required_packages['robotframework-seleniumlibrary']="==3.3.1"
required_packages['robotframework-selenium2library']="==3.0.0"
required_packages['robotframework-sikulilibrary']="==1.0.8"
required_packages['robotframework-sshlibrary']="==3.3.0"
required_packages['robotframework-stringformat']="==0.1.8"
required_packages['robotframework-sudslibrary3']="==0.9"
required_packages['selenium']="==3.141.0"
required_packages['six']="==1.12.0"
required_packages['suds2']="==0.7.1"
required_packages['suds-jurko']="==0.6"
required_packages['tlslite']="==0.4.9"
required_packages['typing']="==3.6.6"
required_packages['xlrd']="==1.2.0"
required_packages['xlutils']="==2.0.0"
required_packages['xlwt']="==1.3.0"
required_packages['wheel']="==0.33.4"


from sys import platform
if platform == "win32":
	required_packages['pywin32']="==225"
	required_packages['autoitlibrary3']="==1.1.post1"
	required_packages['robotframework-autoitlibrary']="==1.2.4"
	required_packages['wxpython']="==4.0.4"
	required_packages['robotframework-ride']="==1.7.4.1"
	required_packages['psycopg2']="==2.8.4"
else:
	required_packages['pexpect']="==4.7.0"
	required_packages['ptyprocess']="==0.6.0"

from setuptools import setup
			
def pkg_list():
	a=[]
	for package in required_packages:
		a.append(package+required_packages[package])
	return a

setup(name='rft-core',
      version='1.2.5',
      description='RobotFramework Toolkit',
      url='https://github.com/ludovicurbain/rft-core.git',
      author='Ludovic Urbain',
      author_email='ludovic.urbain@swift.com',
      license='MIT',
      packages=['rft-core'],
	  install_requires=[
          pkg_list(),
      ],
      zip_safe=False)