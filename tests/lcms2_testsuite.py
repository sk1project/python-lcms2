# -*- coding: utf-8 -*-
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

import lcms2
import unittest, os

_pkgdir = os.path.dirname(__file__)

def get_filepath(filename):
	return os.path.join(_pkgdir, 'cms_data', filename)

class TestCmsFunctions(unittest.TestCase):

	def setUp(self):
		rgb_profile = get_filepath('sRGB.icm')
		self.inProfile = lcms2.cmsOpenProfileFromFile(rgb_profile)
		cmyk_profile = get_filepath('CMYK.icm')
		self.outProfile = lcms2.cmsOpenProfileFromFile(cmyk_profile)
		self.transform = lcms2.cmsCreateTransform(self.inProfile,
						lcms2.TYPE_RGBA_8, self.outProfile, lcms2.TYPE_CMYK_8,
						lcms2.INTENT_PERCEPTUAL, lcms2.cmsFLAGS_NOTPRECALC)
		self.transform2 = lcms2.cmsCreateTransform(self.inProfile,
						lcms2.TYPE_RGBA_8, self.outProfile, lcms2.TYPE_CMYK_8,
						lcms2.INTENT_PERCEPTUAL, 0)


	def tearDown(self):
		pass

	def test01_open_profile(self):
		self.assertNotEqual(None, self.inProfile)
		self.assertNotEqual(None, self.outProfile)

	def test02_create_srgb_profile(self):
		self.assertNotEqual(None, lcms2.cmsCreate_sRGBProfile())

	def test03_create_gray_profile(self):
		self.assertNotEqual(None, lcms2.cmsCreateGrayProfile())

	def test04_create_lab_profile(self):
		self.assertNotEqual(None, lcms2.cmsCreateLabProfile())

	def test05_create_xyz_profile(self):
		self.assertNotEqual(None, lcms2.cmsCreateXYZProfile())

	def test06_open_invalid_profile(self):
		try:
			profile = get_filepath('empty.icm')
			lcms2.cmsOpenProfileFromFile(profile)
		except lcms2.CmsError:
			return
		self.fail()

	def test07_open_absent_profile(self):
		try:
			profile = get_filepath('xxx.icm')
			lcms2.cmsOpenProfileFromFile(profile)
		except lcms2.CmsError:
			return
		self.fail()

	def test08_create_transform(self):
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGBA_8, self.outProfile, lcms2.TYPE_CMYK_8))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.outProfile,
				lcms2.TYPE_CMYK_8, self.inProfile, lcms2.TYPE_RGBA_8))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.outProfile,
				lcms2.TYPE_CMYK_8, self.inProfile, lcms2.TYPE_RGB_8))

	def test09_create_transform_16b(self):
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_16, self.outProfile, lcms2.TYPE_CMYK_16))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGBA_16, self.outProfile, lcms2.TYPE_CMYK_16))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.outProfile,
				lcms2.TYPE_CMYK_16, self.inProfile, lcms2.TYPE_RGBA_16))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.outProfile,
				lcms2.TYPE_CMYK_16, self.inProfile, lcms2.TYPE_RGB_16))

	def test10_create_transform_dbl(self):
		lab_profile = lcms2.cmsCreateLabProfile()
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_16, lab_profile, lcms2.TYPE_Lab_DBL))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.outProfile,
				lcms2.TYPE_CMYK_16, lab_profile, lcms2.TYPE_Lab_DBL))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(lab_profile,
				lcms2.TYPE_Lab_DBL, self.inProfile, lcms2.TYPE_RGB_16))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(lab_profile,
				lcms2.TYPE_Lab_DBL, self.outProfile, lcms2.TYPE_CMYK_16))

	def test11_create_transform_with_custom_intent(self):
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_PERCEPTUAL))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_RELATIVE_COLORIMETRIC))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_SATURATION))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_ABSOLUTE_COLORIMETRIC))

	def test12_create_transform_with_custom_flags(self):
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_PERCEPTUAL,
				lcms2.cmsFLAGS_NOTPRECALC | lcms2.cmsFLAGS_GAMUTCHECK))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_PERCEPTUAL,
				lcms2.cmsFLAGS_PRESERVEBLACK | lcms2.cmsFLAGS_BLACKPOINTCOMPENSATION))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_PERCEPTUAL,
				lcms2.cmsFLAGS_NOTPRECALC | lcms2.cmsFLAGS_HIGHRESPRECALC))
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8,
				lcms2.INTENT_PERCEPTUAL,
				lcms2.cmsFLAGS_NOTPRECALC | lcms2.cmsFLAGS_LOWRESPRECALC))

	def test13_create_transform_with_invalid_intent(self):
		self.assertNotEqual(None, lcms2.cmsCreateTransform(self.inProfile,
				lcms2.TYPE_RGB_8, self.outProfile, lcms2.TYPE_CMYK_8, 3))
		try:
			lcms2.cmsCreateTransform(self.inProfile, lcms2.TYPE_RGB_8,
									self.outProfile, lcms2.TYPE_CMYK_8, 4)
		except lcms2.CmsError:
			return
		self.fail()


def get_suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestCmsFunctions))
	return suite


if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(get_suite())
