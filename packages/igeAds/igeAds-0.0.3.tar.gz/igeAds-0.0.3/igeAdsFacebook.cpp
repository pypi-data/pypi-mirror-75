#include "igeAds.h"
#include "igeAds_doc_en.h"

PyObject* adsFacebook_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	adsFacebook_obj* self = NULL;

	self = (adsFacebook_obj*)type->tp_alloc(type, 0);
	self->adsFacebook = new AdsFacebook();

	return (PyObject*)self;
}

void adsFacebook_dealloc(adsFacebook_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* adsFacebook_str(adsFacebook_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "ads Facebook object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* adsFacebook_Init(adsFacebook_obj* self, PyObject* args, PyObject* kwargs)
{
	//static char* kwlist[] = { "applovinApp","bannerSize", "gender", "childDirectedTreatment","keywords","birthday", "testDevicesIds", NULL };
	static char* kwlist[] = { "android","ios", NULL };
	
	PyObject* facebookAdsAndroid = nullptr;
	PyObject* facebookAdsIos= nullptr;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", kwlist, &facebookAdsAndroid, &facebookAdsIos)) return NULL;

	PyObject* facebookAdsApp = nullptr;
	PyObject* bannerSize = nullptr;
	int gender = 0;
	int childDirectedTreatment;
	PyObject* keywords = nullptr;
	PyObject* birthday = nullptr;
	PyObject* testDevicesIds = nullptr;	

	PyObject* facebookAdsAppPlatform = nullptr;
#if defined(_WIN32) || defined(__ANDROID__)
	if (facebookAdsAndroid && PyTuple_Check(facebookAdsAndroid))
	{
		facebookAdsAppPlatform = facebookAdsAndroid;
	}
#else
	if (facebookAdsIos && PyTuple_Check(facebookAdsIos))
	{
		facebookAdsAppPlatform = facebookAdsIos;
	}
	else
	{
		if (facebookAdsAndroid && PyTuple_Check(facebookAdsAndroid))
		{
			facebookAdsAppPlatform = facebookAdsAndroid;
		}
	}
#endif
	
	if (facebookAdsAppPlatform)
	{
		uint32_t numAttr = 0;
		numAttr = (uint32_t)PyTuple_Size(facebookAdsAppPlatform);

		if (numAttr != 7) {
			PyErr_SetString(PyExc_TypeError, "7 Parameters : applovinApp | bannerSize | gender | childDirectedTreatment | keywords | birthday | testDevicesIds");
			return NULL;
		}

		facebookAdsApp = PyTuple_GET_ITEM(facebookAdsAppPlatform, 0);
		bannerSize = PyTuple_GET_ITEM(facebookAdsAppPlatform, 1);
		gender = PyLong_AsLong(PyTuple_GET_ITEM(facebookAdsAppPlatform, 2));
		childDirectedTreatment = PyLong_AsLong(PyTuple_GET_ITEM(facebookAdsAppPlatform, 3));
		keywords = PyTuple_GET_ITEM(facebookAdsAppPlatform, 4);
		birthday = PyTuple_GET_ITEM(facebookAdsAppPlatform, 5);
		testDevicesIds = PyTuple_GET_ITEM(facebookAdsAppPlatform, 6);
	}
	//if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OiiOOO", kwlist, &applovinApp, &bannerSize, &gender, &childDirectedTreatment, &keywords, &birthday, &testDevicesIds)) return NULL;

	if (facebookAdsApp && PyTuple_Check(facebookAdsApp))
	{
        {
            uint32_t numAttr = 0;
            numAttr = (uint32_t) PyTuple_Size(facebookAdsApp);
            if (numAttr != 4) {
                PyErr_SetString(PyExc_TypeError,
                                "4 Parameters : applovinAppID(char*) | bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)");
                return NULL;
            }
            char **paramaters = new char *[numAttr];
            memset(paramaters, 0, sizeof(char *) * numAttr);
            for (uint32_t i = 0; i < numAttr; i++) {
                PyObject *v = PyTuple_GET_ITEM(facebookAdsApp, i);
                Py_ssize_t len;
                const char* temp_str = PyUnicode_AsUTF8AndSize(v, &len);
                paramaters[i] = (char *)PyObject_MALLOC(len + 1);
                memcpy(paramaters[i], temp_str, len + 1);
            }
            self->adsFacebook->setupApp(paramaters[0], paramaters[1], paramaters[2],
                                              paramaters[3]);
        }
	}

	self->adsFacebook->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_Release(adsFacebook_obj* self)
{
	self->adsFacebook->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_Testcase(adsFacebook_obj* self)
{
	//self->adsAdmob->testcase();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_ShowBanner(adsFacebook_obj* self, PyObject* args)
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
        self->adsFacebook->showBanner((Ads::BannerPosition)position, left, top);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsFacebook->showBanner((Ads::BannerPosition)position, 0, 0);
    }
	else
	{
		self->adsFacebook->showBanner((Ads::BannerPosition)0, 0, 0);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_BannerMoveTo(adsFacebook_obj* self, PyObject* args)
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
        self->adsFacebook->bannerMoveTo((Ads::BannerPosition)position, left, top);
    }
    else if (secondParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter))
    {
        int x = PyLong_AsLong(firstParameter);
        int y = PyLong_AsLong(secondParameter);
        self->adsFacebook->bannerMoveTo(x, y);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsFacebook->bannerMoveTo((Ads::BannerPosition)position, 0, 0);
    }

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_HideBanner(adsFacebook_obj* self)
{
	self->adsFacebook->hideBanner();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_ShowInterstitial(adsFacebook_obj* self)
{
    self->adsFacebook->showInterstitial();
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_ShowRewardedVideo(adsFacebook_obj* self)
{
	self->adsFacebook->showRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_PauseRewardedVideo(adsFacebook_obj* self)
{
	self->adsFacebook->pauseRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsFacebook_ResumeRewardedVideo(adsFacebook_obj* self)
{
	self->adsFacebook->resumeRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef adsFacebook_methods[] = {
	{ "init", (PyCFunction)adsFacebook_Init, METH_VARARGS | METH_KEYWORDS, adsAdmobInit_doc },
	{ "release", (PyCFunction)adsFacebook_Release, METH_NOARGS, adsAdmobRelease_doc },
	{ "testcase", (PyCFunction)adsFacebook_Testcase, METH_NOARGS, adsAdmobTestcase_doc },
	{ "showBanner", (PyCFunction)adsFacebook_ShowBanner, METH_VARARGS, adsAdmobShowBanner_doc },
	{ "bannerMoveTo", (PyCFunction)adsFacebook_BannerMoveTo, METH_VARARGS, adsAdmobBannerMoveTo_doc },
	{ "hideBanner", (PyCFunction)adsFacebook_HideBanner, METH_NOARGS, adsAdmobHideBanner_doc },
	{ "showInterstitial", (PyCFunction)adsFacebook_ShowInterstitial, METH_NOARGS, adsAdmobShowInterstitial_doc },
	{ "showRewardedVideo", (PyCFunction)adsFacebook_ShowRewardedVideo, METH_NOARGS, adsAdmobShowRewardedVideo_doc },
	{ "pauseRewardedVideo", (PyCFunction)adsFacebook_PauseRewardedVideo, METH_NOARGS, adsAdmobPauseRewardedVideo_doc },
	{ "resumeRewardedVideo", (PyCFunction)adsFacebook_ResumeRewardedVideo, METH_NOARGS, adsAdmobResumeRewardedVideo_doc },
	{ NULL,	NULL }
};

PyGetSetDef adsFacebook_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AdsFacebookType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAds.facebook",							/* tp_name */
	sizeof(adsFacebook_obj),					/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)adsFacebook_dealloc,			/* tp_dealloc */
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
	(reprfunc)adsFacebook_str,					/* tp_str */
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
	adsFacebook_methods,						/* tp_methods */
	0,											/* tp_members */
	adsFacebook_getsets,						/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	adsFacebook_new,							/* tp_new */
	0,											/* tp_free */
};
