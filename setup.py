# -*- coding: utf-8 -*-
#
# 	python-lcms2 build script
#
# 	Copyright (C) 2017 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup, Extension
import commands

def get_pkg_libs(pkg_names):
	libs = []
	for item in pkg_names:
		output = commands.getoutput("pkg-config --libs-only-l %s" % item)
		names = output.replace('-l', '').strip().split(' ')
		for name in names:
			if not name in libs: libs.append(name)
	return libs


src_path = 'src/'
lcms2_src = src_path + 'lcms2/'

lcms2_module = Extension('lcms2._lcms2',
		define_macros=[('MAJOR_VERSION', '0'),
					('MINOR_VERSION', '1')],
		sources=[lcms2_src + '_lcms2.c'],
		libraries=get_pkg_libs(['lcms2', ]),
		extra_compile_args=["-Wall"])

setup (name='lcms2',
		version='0.1',
		description='lcms2 python extention',
		author='Igor E. Novikov',
		author_email='sk1.project.org@gmail.com',
		maintainer='Igor E. Novikov',
		maintainer_email='sk1.project.org@gmail.com',
		license='GPL v3',
		url='http://sk1project.net',
		download_url='http://sk1project.net/',
		long_description='''
		lcms2 is a python extention which provides binding to lcms2 library. 
		sK1 Team (http://sk1project.net), copyright (c) 2017 by Igor E. Novikov.
		''',
	classifiers=[
		'Development Status :: 5 - Stable',
		'Environment :: Console',
		'License :: OSI Approved :: GPL v3',
		'Operating System :: POSIX',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python',
		'Programming Language :: C',
		'Topic :: Multimedia :: Graphics :: Graphics Conversion',
		],

	packages=['lcms2'],

	package_dir={'lcms2': 'src/lcms2'},

	ext_modules=[lcms2_module])
