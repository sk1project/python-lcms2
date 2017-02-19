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
		self.transform_16b = lcms2.cmsCreateTransform(self.inProfile,
						lcms2.TYPE_RGBA_16, self.outProfile, lcms2.TYPE_CMYK_16,
						lcms2.INTENT_PERCEPTUAL, lcms2.cmsFLAGS_NOTPRECALC)


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

	#---8bit transform tests

	def test14_do_transform_with_null_input(self):
		rgb = lcms2.COLORB()
		cmyk = lcms2.COLORB()
		lcms2.cmsDoTransform(self.transform, rgb, cmyk)
		self.assertNotEqual(0, cmyk[0])
		self.assertNotEqual(0, cmyk[1])
		self.assertNotEqual(0, cmyk[2])
		self.assertNotEqual(0, cmyk[3])

	def test15_do_transform_with_maximum_allowed_input(self):
		rgb = lcms2.COLORB()
		cmyk = lcms2.COLORB()
		rgb[0] = 255
		rgb[1] = 255
		rgb[2] = 255
		lcms2.cmsDoTransform(self.transform, rgb, cmyk)
		self.assertEqual(0, cmyk[0])
		self.assertEqual(0, cmyk[1])
		self.assertEqual(0, cmyk[2])
		self.assertEqual(0, cmyk[3])

	def test16_do_transform_with_intermediate_input(self):
		rgb = lcms2.COLORB()
		cmyk = lcms2.COLORB()
		rgb[0] = 100
		rgb[1] = 190
		rgb[2] = 150
		lcms2.cmsDoTransform(self.transform, rgb, cmyk)
		self.assertNotEqual(0, cmyk[0])
		self.assertNotEqual(0, cmyk[1])
		self.assertNotEqual(0, cmyk[2])
		self.assertNotEqual(0, cmyk[3])

	def test17_do_transform_with_incorrect_input_buffer(self):
		cmyk = lcms2.COLORB()
		rgb = 255
		try:
			lcms2.cmsDoTransform(self.transform, rgb, cmyk)
		except lcms2.CmsError:
			return
		self.fail()

	def test18_do_transform_with_incorrect_output_buffer(self):
		rgb = lcms2.COLORB()
		rgb[0] = 255
		rgb[1] = 255
		rgb[2] = 255
		cmyk = 255
		try:
			lcms2.cmsDoTransform(self.transform, rgb, cmyk)
		except lcms2.CmsError:
			return
		self.fail()

	#---16bit transform tests

	def test19_do_transform_16b_with_null_input(self):
		rgb = lcms2.COLORW()
		cmyk = lcms2.COLORW()
		lcms2.cmsDoTransform(self.transform_16b, rgb, cmyk)
		self.assertNotEqual(0, cmyk[0])
		self.assertNotEqual(0, cmyk[1])
		self.assertNotEqual(0, cmyk[2])
		self.assertNotEqual(0, cmyk[3])

	def test20_do_transform_with_maximum_allowed_input(self):
		rgb = lcms2.COLORW()
		cmyk = lcms2.COLORW()
		rgb[0] = 65535
		rgb[1] = 65535
		rgb[2] = 65535
		lcms2.cmsDoTransform(self.transform_16b, rgb, cmyk)
		self.assertLess(cmyk[0], 10)
		self.assertLess(cmyk[1], 10)
		self.assertLess(cmyk[2], 10)
		self.assertLess(cmyk[3], 10)

	def test21_do_transform_with_intermediate_input(self):
		rgb = lcms2.COLORB()
		cmyk = lcms2.COLORB()
		rgb[0] = 25535
		rgb[1] = 35535
		rgb[2] = 30535
		lcms2.cmsDoTransform(self.transform_16b, rgb, cmyk)
		self.assertNotEqual(0, cmyk[0])
		self.assertNotEqual(0, cmyk[1])
		self.assertNotEqual(0, cmyk[2])
		self.assertNotEqual(0, cmyk[3])

	def test22_do_transform_with_incorrect_input_buffer(self):
		cmyk = lcms2.COLORW()
		rgb = 255
		try:
			lcms2.cmsDoTransform(self.transform_16b, rgb, cmyk)
		except lcms2.CmsError:
			return
		self.fail()

	def test23_do_transform_with_incorrect_output_buffer(self):
		rgb = lcms2.COLORW()
		rgb[0] = 65535
		rgb[1] = 65535
		rgb[2] = 65535
		cmyk = 255
		try:
			lcms2.cmsDoTransform(self.transform_16b, rgb, cmyk)
		except lcms2.CmsError:
			return
		self.fail()


	#---Profile info related tests

	def test30_get_profile_name(self):
		name = lcms2.cmsGetProfileName(self.outProfile)
		self.assertEqual(name, 'Fogra27L CMYK Coated Press')

	def test31_get_profile_info(self):
		name = lcms2.cmsGetProfileInfo(self.outProfile)
		self.assertEqual(name[:15], 'Offset printing')

	def test32_get_profile_copyright(self):
		name = lcms2.cmsGetProfileCopyright(self.outProfile)
		if os.name == 'nt':
			self.assertEqual(name, '')
		else:
			self.assertEqual(name, 'Public Domain')


def get_suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestCmsFunctions))
	return suite


if __name__ == '__main__':
	unittest.TextTestRunner(verbosity=2).run(get_suite())
