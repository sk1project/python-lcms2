/* _lcms2 - small module which provides binding to LittleCMS library version 2.
 *
 * Copyright (C) 2017 by Igor E.Novikov
 *
 * 	This program is free software: you can redistribute it and/or modify
 *	it under the terms of the GNU General Public License as published by
 *	the Free Software Foundation, either version 3 of the License, or
 *	(at your option) any later version.
 *
 *	This program is distributed in the hope that it will be useful,
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *	GNU General Public License for more details.
 *
 *	You should have received a copy of the GNU General Public License
 *	along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <Python.h>
#include <lcms2.h>

cmsUInt32Number
getLCMStype (char* mode) {

  if (strcmp(mode, "RGB") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(mode, "RGBA") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(mode, "RGBX") == 0) {
    return TYPE_RGBA_8;
  }
  else if (strcmp(mode, "RGBA;16") == 0) {
    return TYPE_RGBA_16;
  }
  else if (strcmp(mode, "CMYK") == 0) {
    return TYPE_CMYK_8;
  }
  else if (strcmp(mode, "CMYK;16") == 0) {
    return TYPE_CMYK_16;
  }
  else if (strcmp(mode, "L") == 0) {
    return TYPE_GRAY_8;
  }
  else if (strcmp(mode, "L;16") == 0) {
    return TYPE_GRAY_16;
  }
  else if (strcmp(mode, "LAB") == 0) {
    return TYPE_Lab_8;
  }
  else if (strcmp(mode, "LAB;float") == 0) {
    return TYPE_Lab_DBL;
  }
  else if (strcmp(mode, "XYZ;float") == 0) {
    return TYPE_XYZ_DBL;
  }

  else {
    return TYPE_GRAY_8;
  }
}


static PyObject *
pycms_OpenProfile(PyObject *self, PyObject *args) {

	char *profile = NULL;
	cmsHPROFILE hProfile;

	if (!PyArg_ParseTuple(args, "s", &profile)){
		Py_INCREF(Py_None);
		return Py_None;
	}

	hProfile = cmsOpenProfileFromFile(profile, "r");

	if(hProfile==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hProfile, (void *)cmsCloseProfile));
}

static PyObject *
pycms_CreateRGBProfile(PyObject *self, PyObject *args) {

	cmsHPROFILE hProfile;

	hProfile = cmsCreate_sRGBProfile();

	if(hProfile==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hProfile, (void *)cmsCloseProfile));
}

static PyObject *
pycms_CreateLabProfile(PyObject *self, PyObject *args) {

	cmsHPROFILE hProfile;

	hProfile = cmsCreateLab4Profile(0);

	if(hProfile==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hProfile, (void *)cmsCloseProfile));
}

static PyObject *
pycms_CreateGrayProfile(PyObject *self, PyObject *args) {

	cmsHPROFILE hProfile;
	cmsToneCurve *tonecurve;

	tonecurve = cmsBuildGamma(NULL, 2.2);
	hProfile = cmsCreateGrayProfile(0, tonecurve);
	cmsFreeToneCurve(tonecurve);

	if(hProfile==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hProfile, (void *)cmsCloseProfile));
}

static PyObject *
pycms_CreateXYZProfile(PyObject *self, PyObject *args) {

	cmsHPROFILE hProfile;

	hProfile = cmsCreateXYZProfile();

	if(hProfile==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hProfile, (void *)cmsCloseProfile));
}

static PyObject *
pycms_BuildTransform (PyObject *self, PyObject *args) {

	char *inMode;
	char *outMode;
	int renderingIntent;
	int inFlags;
	cmsUInt32Number flags;
	void *inputProfile;
	void *outputProfile;
	cmsHPROFILE hInputProfile, hOutputProfile;
	cmsHTRANSFORM hTransform;

	if (!PyArg_ParseTuple(args, "OsOsii", &inputProfile, &inMode, &outputProfile, &outMode, &renderingIntent, &inFlags)) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	hInputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(inputProfile);
	hOutputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(outputProfile);
	flags = (cmsUInt32Number) inFlags;

	hTransform = cmsCreateTransform(hInputProfile, getLCMStype(inMode),
			hOutputProfile, getLCMStype(outMode), renderingIntent, flags);

	if(hTransform==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hTransform, (void *)cmsDeleteTransform));
}

static PyObject *
pycms_BuildProofingTransform (PyObject *self, PyObject *args) {

	char *inMode;
	char *outMode;
	int renderingIntent;
	int proofingIntent;
	int inFlags;
	cmsUInt32Number flags;
	void *inputProfile;
	void *outputProfile;
	void *proofingProfile;

	cmsHPROFILE hInputProfile, hOutputProfile, hProofingProfile;
	cmsHTRANSFORM hTransform;

	if (!PyArg_ParseTuple(args, "OsOsOiii", &inputProfile, &inMode, &outputProfile, &outMode,
			&proofingProfile, &renderingIntent, &proofingIntent, &inFlags)) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	hInputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(inputProfile);
	hOutputProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(outputProfile);
	hProofingProfile = (cmsHPROFILE) PyCObject_AsVoidPtr(proofingProfile);
	flags = (cmsUInt32Number) inFlags;

	hTransform = cmsCreateProofingTransform(hInputProfile, getLCMStype(inMode),
			hOutputProfile, getLCMStype(outMode), hProofingProfile, renderingIntent, proofingIntent, flags);

	if(hTransform==NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	return Py_BuildValue("O", PyCObject_FromVoidPtr((void *)hTransform, (void *)cmsDeleteTransform));
}

static PyObject *
pycms_TransformPixel (PyObject *self, PyObject *args) {

	unsigned char *inbuf;
	int channel1,channel2,channel3,channel4;
	void *transform;
	cmsHTRANSFORM hTransform;
	PyObject *result;

	if (!PyArg_ParseTuple(args, "Oiiii", &transform, &channel1, &channel2, &channel3, &channel4)) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	inbuf=malloc(4);
	inbuf[0]=(unsigned char)channel1;
	inbuf[1]=(unsigned char)channel2;
	inbuf[2]=(unsigned char)channel3;
	inbuf[3]=(unsigned char)channel4;

	hTransform = (cmsHTRANSFORM) PyCObject_AsVoidPtr(transform);

	cmsDoTransform(hTransform, inbuf, inbuf, 1);

	result = Py_BuildValue("[iiii]", inbuf[0], inbuf[1], inbuf[2], inbuf[3]);
	free(inbuf);
	return result;
}


static PyObject *
pycms_TransformPixel2 (PyObject *self, PyObject *args) {

	double channel1,channel2,channel3,channel4;
	unsigned char *inbuf;
	void *transform;
	cmsHTRANSFORM hTransform;
	PyObject *result;

	if (!PyArg_ParseTuple(args, "Odddd", &transform, &channel1, &channel2, &channel3, &channel4)) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	inbuf=malloc(4);
	inbuf[0]=(unsigned char)(channel1*255);
	inbuf[1]=(unsigned char)(channel2*255);
	inbuf[2]=(unsigned char)(channel3*255);
	inbuf[3]=(unsigned char)(channel4*255);

	hTransform = (cmsHTRANSFORM) PyCObject_AsVoidPtr(transform);

	cmsDoTransform(hTransform, inbuf, inbuf, 1);

	result = Py_BuildValue("(dddd)", (double)inbuf[0]/255, (double)inbuf[1]/255,
			(double)inbuf[2]/255, (double)inbuf[3]/255);

	free(inbuf);
	return result;
}

static PyObject *
pycms_GetVersion (PyObject *self, PyObject *args) {
	return Py_BuildValue("i",  LCMS_VERSION);
}

static
PyMethodDef pycms_methods[] = {
	{"getVersion", pycms_GetVersion, METH_VARARGS},
	{"openProfile", pycms_OpenProfile, METH_VARARGS},
	{"createRGBProfile", pycms_CreateRGBProfile, METH_VARARGS},
	{"createLabProfile", pycms_CreateLabProfile, METH_VARARGS},
	{"createGrayProfile", pycms_CreateGrayProfile, METH_VARARGS},
	{"createXYZProfile", pycms_CreateXYZProfile, METH_VARARGS},
	{"buildTransform", pycms_BuildTransform, METH_VARARGS},
	{"buildProofingTransform", pycms_BuildProofingTransform, METH_VARARGS},
	{"transformPixel", pycms_TransformPixel, METH_VARARGS},
	{"transformPixel2", pycms_TransformPixel2, METH_VARARGS},
	{NULL, NULL}
};

void
init_lcms2(void)
{
    Py_InitModule("_lcms2", pycms_methods);
}
