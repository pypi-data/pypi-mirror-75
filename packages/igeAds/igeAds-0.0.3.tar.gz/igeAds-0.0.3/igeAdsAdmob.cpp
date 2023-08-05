#include "igeAds.h"
#include "igeAds_doc_en.h"

namespace ads
{
	int pyObjToIntArray(PyObject* obj, uint32_t* idx) {

		int totalCount = 0;
		int type = -1;
		if (PyTuple_Check(obj)) type = 0;
		else if (PyList_Check(obj))  type = 1;
		if (type == -1) return 0;

		int elementCount = 0;
		int numElem = (type == 0) ? PyTuple_Size(obj) : PyList_Size(obj);
		for (int i = 0; i < numElem; i++) {
			PyObject* element = (type == 0) ? PyTuple_GET_ITEM(obj, i) : PyList_GET_ITEM(obj, i);
			if (PyLong_Check(element)) {
				if (idx)idx[totalCount] = PyLong_AsLong(element);
				totalCount++;
				elementCount++;
				if (elementCount >= 3) elementCount = 0;
			}
			else if (PyTuple_Check(element)) {
				int d = (int)PyTuple_Size(element);
				for (int j = 0; j < d; j++) {
					PyObject* val = PyTuple_GET_ITEM(element, j);
					if (idx)idx[totalCount] = PyLong_AsLong(val);
					totalCount++;
					elementCount++;
					if (elementCount >= 3) break;
				}
				elementCount = 0;
			}
			else if (PyList_Check(element)) {
				int d = (int)PyList_Size(element);
				for (int j = 0; j < d; j++) {
					PyObject* val = PyList_GET_ITEM(element, j);
					if (idx)idx[totalCount] = PyLong_AsLong(val);
					totalCount++;
					elementCount++;
					if (elementCount >= 3) break;
				}
				elementCount = 0;
			}
		}
		return totalCount;
	}
}

PyObject* adsAdmob_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	adsAdmob_obj* self = NULL;

	self = (adsAdmob_obj*)type->tp_alloc(type, 0);
	self->adsAdmob = new AdsAdmob();

	return (PyObject*)self;
}

void adsAdmob_dealloc(adsAdmob_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* adsAdmob_str(adsAdmob_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "ads admob object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* adsAdmob_Init(adsAdmob_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "android","ios", NULL };
	
	PyObject* adMobAndroid = nullptr;
	PyObject* adMobIos= nullptr;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", kwlist, &adMobAndroid, &adMobIos)) return NULL;

	PyObject* adMobApp = nullptr;
	PyObject* bannerSize = nullptr;
	int gender = 0;
	int childDirectedTreatment;
	PyObject* keywords = nullptr;
	PyObject* birthday = nullptr;
	PyObject* testDevicesIds = nullptr;	

	PyObject* adMobAppPlatform = nullptr;
#if defined(_WIN32) || defined(__ANDROID__)
	if (adMobAndroid && PyTuple_Check(adMobAndroid))
	{
		adMobAppPlatform = adMobAndroid;
	}
#else
	if (adMobIos && PyTuple_Check(adMobIos))
	{
		adMobAppPlatform = adMobIos;
	}
	else
	{
		if (adMobAndroid && PyTuple_Check(adMobAndroid))
		{
			adMobAppPlatform = adMobAndroid;
		}
	}
#endif
	
	if (adMobAppPlatform)
	{
		uint32_t numAttr = 0;
		numAttr = (uint32_t)PyTuple_Size(adMobAppPlatform);

		if (numAttr != 7) {
			PyErr_SetString(PyExc_TypeError, "7 Parameters : adMobApp | bannerSize | gender | childDirectedTreatment | keywords | birthday | testDevicesIds");
			return NULL;
		}

		adMobApp = PyTuple_GET_ITEM(adMobAppPlatform, 0);
		bannerSize = PyTuple_GET_ITEM(adMobAppPlatform, 1);
		gender = PyLong_AsLong(PyTuple_GET_ITEM(adMobAppPlatform, 2));
		childDirectedTreatment = PyLong_AsLong(PyTuple_GET_ITEM(adMobAppPlatform, 3));
		keywords = PyTuple_GET_ITEM(adMobAppPlatform, 4);
		birthday = PyTuple_GET_ITEM(adMobAppPlatform, 5);
		testDevicesIds = PyTuple_GET_ITEM(adMobAppPlatform, 6);
	}

	if (adMobApp && PyTuple_Check(adMobApp))
	{
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(adMobApp);
			if (numAttr != 4) {
				PyErr_SetString(PyExc_TypeError, "4 Parameters : adMobAppID(char*) | bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)");
				return NULL;
			}
			char** paramaters = new char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(adMobApp, i);
				Py_ssize_t len;
                const char* temp_str = PyUnicode_AsUTF8AndSize(v, &len);
                paramaters[i] = (char *)PyObject_MALLOC(len + 1);
                memcpy(paramaters[i], temp_str, len + 1);
			}
			self->adsAdmob->setupApp(paramaters[0], paramaters[1], paramaters[2], paramaters[3]);
		}		
		
		if (bannerSize)
		{
			int bufferSize = ads::pyObjToIntArray(bannerSize, nullptr);
			if (bufferSize != 2) {
				PyErr_SetString(PyExc_TypeError, "2 Parameters : width(int) | height(int)");
				return NULL;
			}
			uint32_t* buffer = (uint32_t*)malloc(bufferSize * sizeof(int));
			ads::pyObjToIntArray(bannerSize, buffer);
			self->adsAdmob->setBannerSize(buffer[0], buffer[1]);
		}

		{
			self->adsAdmob->setGender((firebase::admob::Gender)gender);
		}

		{
			self->adsAdmob->setChildDirectedTreatmentState((firebase::admob::ChildDirectedTreatmentState)childDirectedTreatment);
		}

		if (keywords)
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(keywords);
			if (numAttr == 0) {
				PyErr_SetString(PyExc_TypeError, "Parameter error.");
				return NULL;
			}
			const char** paramaters = new const char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(keywords, i);
				paramaters[i] = PyUnicode_AsUTF8(v);
			}
			self->adsAdmob->setKeywords(numAttr, paramaters);
		}

		if (birthday)
		{
			int birthdaySize = ads::pyObjToIntArray(birthday, nullptr);
			if (birthdaySize != 3) {
				PyErr_SetString(PyExc_TypeError, "3 Parameters : day(int) | month(int) | year(int)");
				return NULL;
			}
			uint32_t* buffer = (uint32_t*)malloc(birthdaySize * sizeof(int));
			ads::pyObjToIntArray(birthday, buffer);
			self->adsAdmob->setBirthday(buffer[0], buffer[1], buffer[2]);
		}

		if (testDevicesIds)
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(testDevicesIds);
			if (numAttr == 0) {
				PyErr_SetString(PyExc_TypeError, "Parameter error.");
				return NULL;
			}
			const char** paramaters = new const char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(testDevicesIds, i);
				paramaters[i] = PyUnicode_AsUTF8(v);
			}
			self->adsAdmob->setTestDeviceIds(numAttr, paramaters);
		}
	}

	self->adsAdmob->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_Release(adsAdmob_obj* self)
{
	self->adsAdmob->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_Testcase(adsAdmob_obj* self)
{
	self->adsAdmob->testcase();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_ShowBanner(adsAdmob_obj* self, PyObject* args)
{
    PyObject* firstParameter = nullptr;
    PyObject* secondParameter = nullptr;
    PyObject* thirdParameter = nullptr;

    if (!PyArg_ParseTuple(args, "|OOO", &firstParameter, &secondParameter, &thirdParameter)) return NULL;
    if (thirdParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter) && PyLong_Check(thirdParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        int left = PyLong_AsLong(secondParameter);
        int top = PyLong_AsLong(thirdParameter);
        self->adsAdmob->showBanner((Ads::BannerPosition)position, left, top);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsAdmob->showBanner((Ads::BannerPosition)position, 0, 0);
    }
    else
    {
        self->adsAdmob->showBanner((Ads::BannerPosition)0, 0, 0);
    }

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_BannerMoveTo(adsAdmob_obj* self, PyObject* args)
{	
	/// Top of the screen, horizontally centered. -> kPositionTop = 0,
	/// Bottom of the screen, horizontally centered. ->	kPositionBottom,
	/// Top-left corner of the screen. -> kPositionTopLeft,
	/// Top-right corner of the screen. -> kPositionTopRight,
	/// Bottom-left corner of the screen. -> kPositionBottomLeft,
	/// Bottom-right corner of the screen. -> kPositionBottomRight,

	PyObject* firstParameter = nullptr;
    PyObject* secondParameter = nullptr;
    PyObject* thirdParameter = nullptr;

    if (!PyArg_ParseTuple(args, "|OOO", &firstParameter, &secondParameter, &thirdParameter)) return NULL;
    if (thirdParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter) && PyLong_Check(thirdParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        int left = PyLong_AsLong(secondParameter);
        int top = PyLong_AsLong(thirdParameter);
        self->adsAdmob->bannerMoveTo((Ads::BannerPosition)position, left, top);
    }
    else if (secondParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter))
    {
        int x = PyLong_AsLong(firstParameter);
        int y = PyLong_AsLong(secondParameter);
        self->adsAdmob->bannerMoveTo(x, y);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsAdmob->bannerMoveTo((Ads::BannerPosition)position, 0, 0);
    }

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_HideBanner(adsAdmob_obj* self)
{
	self->adsAdmob->hideBanner();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_ShowInterstitial(adsAdmob_obj* self)
{
    self->adsAdmob->showInterstitial();
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_ShowRewardedVideo(adsAdmob_obj* self)
{
	self->adsAdmob->showRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_PauseRewardedVideo(adsAdmob_obj* self)
{
	self->adsAdmob->pauseRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsAdmob_ResumeRewardedVideo(adsAdmob_obj* self)
{
	self->adsAdmob->resumeRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef adsAdmob_methods[] = {
	{ "init", (PyCFunction)adsAdmob_Init, METH_VARARGS | METH_KEYWORDS, adsAdmobInit_doc },
	{ "release", (PyCFunction)adsAdmob_Release, METH_NOARGS, adsAdmobRelease_doc },
	{ "testcase", (PyCFunction)adsAdmob_Testcase, METH_NOARGS, adsAdmobTestcase_doc },
	{ "showBanner", (PyCFunction)adsAdmob_ShowBanner, METH_VARARGS, adsAdmobShowBanner_doc },
	{ "bannerMoveTo", (PyCFunction)adsAdmob_BannerMoveTo, METH_VARARGS, adsAdmobBannerMoveTo_doc },
	{ "hideBanner", (PyCFunction)adsAdmob_HideBanner, METH_NOARGS, adsAdmobHideBanner_doc },
	{ "showInterstitial", (PyCFunction)adsAdmob_ShowInterstitial, METH_NOARGS, adsAdmobShowInterstitial_doc },
	{ "showRewardedVideo", (PyCFunction)adsAdmob_ShowRewardedVideo, METH_NOARGS, adsAdmobShowRewardedVideo_doc },
	{ "pauseRewardedVideo", (PyCFunction)adsAdmob_PauseRewardedVideo, METH_NOARGS, adsAdmobPauseRewardedVideo_doc },
	{ "resumeRewardedVideo", (PyCFunction)adsAdmob_ResumeRewardedVideo, METH_NOARGS, adsAdmobResumeRewardedVideo_doc },
	{ NULL,	NULL }
};

PyGetSetDef adsAdmob_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AdsAdmobType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAds.admob",								/* tp_name */
	sizeof(adsAdmob_obj),						/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)adsAdmob_dealloc,				/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)adsAdmob_str,						/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	adsAdmob_methods,							/* tp_methods */
	0,											/* tp_members */
	adsAdmob_getsets,							/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	adsAdmob_new,								/* tp_new */
	0,											/* tp_free */
};
