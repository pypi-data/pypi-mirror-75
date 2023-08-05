#include "igeAds.h"
#include "igeAds_doc_en.h"

PyObject* adsApplovin_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	adsApplovin_obj* self = NULL;

	self = (adsApplovin_obj*)type->tp_alloc(type, 0);
	self->adsApplovin = AdsApplovin::Instance();

	return (PyObject*)self;
}

void adsApplovin_dealloc(adsApplovin_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* adsApplovin_str(adsApplovin_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "ads Applovin object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* adsApplovin_Init(adsApplovin_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "android","ios", NULL };
	
	PyObject* applovinAndroid = nullptr;
	PyObject* applovinIos= nullptr;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", kwlist, &applovinAndroid, &applovinIos)) return NULL;

	PyObject* applovinApp = nullptr;
	PyObject* bannerSize = nullptr;
	int gender = 0;
	int childDirectedTreatment;
	PyObject* keywords = nullptr;
	PyObject* birthday = nullptr;
	PyObject* testDevicesIds = nullptr;	

	PyObject* applovinAppPlatform = nullptr;
#if defined(_WIN32) || defined(__ANDROID__)
	if (applovinAndroid && PyTuple_Check(applovinAndroid))
	{
		applovinAppPlatform = applovinAndroid;
	}
#else
	if (applovinIos && PyTuple_Check(applovinIos))
	{
		applovinAppPlatform = applovinIos;
	}
	else
	{
		if (applovinAndroid && PyTuple_Check(applovinAndroid))
		{
			applovinAppPlatform = applovinAndroid;
		}
	}
#endif

	if (applovinAppPlatform && PyTuple_Check(applovinAppPlatform))
	{
        {
            uint32_t numAttr = 0;
            numAttr = (uint32_t) PyTuple_Size(applovinAppPlatform);
            if (numAttr != 3) {
                PyErr_SetString(PyExc_TypeError,
                                "3 Parameters : bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)");
                return NULL;
            }
            char **paramaters = new char *[numAttr];
            memset(paramaters, 0, sizeof(char *) * numAttr);
            for (uint32_t i = 0; i < numAttr; i++) {
                PyObject *v = PyTuple_GET_ITEM(applovinAppPlatform, i);
                Py_ssize_t len;
                const char* temp_str = PyUnicode_AsUTF8AndSize(v, &len);
                paramaters[i] = (char *)PyObject_MALLOC(len + 1);
                memcpy(paramaters[i], temp_str, len + 1);
            }
            self->adsApplovin->setupApp("", paramaters[0], paramaters[1],
                                              paramaters[2]);
        }
	}

	self->adsApplovin->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_Release(adsApplovin_obj* self)
{
	self->adsApplovin->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_ShowBanner(adsApplovin_obj* self, PyObject* args)
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
        self->adsApplovin->showBanner((Ads::BannerPosition)position, left, top);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsApplovin->showBanner((Ads::BannerPosition)position, 0, 0);
    }
    else
    {
        self->adsApplovin->showBanner((Ads::BannerPosition)0, 0, 0);
    }

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_BannerMoveTo(adsApplovin_obj* self, PyObject* args)
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
        self->adsApplovin->bannerMoveTo((Ads::BannerPosition)position, left, top);
    }
    else if (secondParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter))
    {
        int x = PyLong_AsLong(firstParameter);
        int y = PyLong_AsLong(secondParameter);
        self->adsApplovin->bannerMoveTo(x, y);
    }
    else if (firstParameter && PyLong_Check(firstParameter))
    {
        int position = PyLong_AsLong(firstParameter);
        self->adsApplovin->bannerMoveTo((Ads::BannerPosition)position, 0, 0);
    }

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_HideBanner(adsApplovin_obj* self)
{
	self->adsApplovin->hideBanner();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_ShowInterstitial(adsApplovin_obj* self)
{
    self->adsApplovin->showInterstitial();
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* adsApplovin_ShowRewardedVideo(adsApplovin_obj* self)
{
	self->adsApplovin->showRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef adsApplovin_methods[] = {
	{ "init", (PyCFunction)adsApplovin_Init, METH_VARARGS | METH_KEYWORDS, adsApplovinInit_doc },
	{ "release", (PyCFunction)adsApplovin_Release, METH_NOARGS, adsApplovinRelease_doc },
	{ "showBanner", (PyCFunction)adsApplovin_ShowBanner, METH_VARARGS, adsApplovinShowBanner_doc },
	{ "bannerMoveTo", (PyCFunction)adsApplovin_BannerMoveTo, METH_VARARGS, adsApplovinBannerMoveTo_doc },
	{ "hideBanner", (PyCFunction)adsApplovin_HideBanner, METH_NOARGS, adsApplovinHideBanner_doc },
	{ "showInterstitial", (PyCFunction)adsApplovin_ShowInterstitial, METH_NOARGS, adsApplovinShowInterstitial_doc },
	{ "showRewardedVideo", (PyCFunction)adsApplovin_ShowRewardedVideo, METH_NOARGS, adsApplovinShowRewardedVideo_doc },
	{ NULL,	NULL }
};

PyGetSetDef adsApplovin_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AdsApplovinType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAds.applovin",							/* tp_name */
	sizeof(adsApplovin_obj),					/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)adsApplovin_dealloc,			/* tp_dealloc */
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
	(reprfunc)adsApplovin_str,					/* tp_str */
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
	adsApplovin_methods,						/* tp_methods */
	0,											/* tp_members */
	adsApplovin_getsets,						/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	adsApplovin_new,							/* tp_new */
	0,											/* tp_free */
};
