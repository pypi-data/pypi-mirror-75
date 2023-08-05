from setuptools import setup

classifiers = [
  'Development Status :: 3 - Alpha',
  # 'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  'Environment :: Console',
  'Intended Audience :: Developers',
  'Intended Audience :: System Administrators',
  'Natural Language :: English',
  'Operating System :: OS Independent',
  'Programming Language :: Python',
  'Topic :: Software Development',
  'Topic :: Software Development :: Libraries :: Python Modules',
  'Topic :: Utilities',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
]

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
]

dependencies = [
]


setup(
	name='newparth',
	version='0.0.1',
	description='Say Hello',
	py_modules=["new"],
	package_dir={'':'src'},
	install_requires=dependencies,
	author= 'parth',
	author_email= 'parth_dani@yahoo.in',
	url= 'https://github.com/paarthdani/testparth',
)
