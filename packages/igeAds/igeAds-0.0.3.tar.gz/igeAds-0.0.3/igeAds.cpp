#include "igeAds.h"
#include "igeAds_doc_en.h"
#include <mutex>

static PyObject* onAdCallBack = nullptr;
static std::vector<AdsCallback> adsArgList;
static std::mutex adsEvent_mtx;

PyObject* ads_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	ads_obj* self = NULL;

	self = (ads_obj*)type->tp_alloc(type, 0);
	self->ads = new Ads();

	return (PyObject*)self;
}

void ads_dealloc(ads_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* ads_str(ads_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "ads object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

void ads_ProcessEventCallbackHandler(const char* provider, const char* adsType, int number, const char* name)
{
	std::lock_guard<std::mutex> uniq_lk(adsEvent_mtx);
	adsArgList.push_back({ provider, adsType, number, name });
}

static PyObject* ads_Init(ads_obj* self)
{
	self->ads->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* ads_Release(ads_obj* self)
{
	self->ads->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* ads_Update(ads_obj* self)
{
	std::lock_guard<std::mutex> uniq_lk(adsEvent_mtx);

	if (onAdCallBack)
	{
		for (auto it = adsArgList.begin(); it != adsArgList.end(); it++)
		{
			PyObject* arglist;
			arglist = Py_BuildValue("(ssis)", it->adsProvider, it->adsType, it->adsNumber, it->adsName);
			PyObject* result = PyEval_CallObject(onAdCallBack, arglist);

			Py_DECREF(arglist);
			Py_XDECREF(result);
		}		
	}	

	adsArgList.clear();	
	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* ads_RegisterEventListener(ads_obj* self, PyObject* args)
{
	if (!PyArg_ParseTuple(args, "O", &onAdCallBack))
		return NULL;

	if (!PyCallable_Check(onAdCallBack)) {
		PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
		return NULL;
	}
	Py_XINCREF(onAdCallBack);

	self->ads->registerEventListener(ads_ProcessEventCallbackHandler);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef ads_methods[] = {
	{ "init", (PyCFunction)ads_Init, METH_NOARGS, adsInit_doc },
	{ "release", (PyCFunction)ads_Release, METH_NOARGS, adsRelease_doc },
	{ "update", (PyCFunction)ads_Update, METH_NOARGS, adsUpdate_doc },
	{ "registerEventListener", (PyCFunction)ads_RegisterEventListener, METH_VARARGS, adsAdmobRegisterEventListener_doc },
	{ NULL,	NULL }
};

PyGetSetDef ads_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject AdsType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeAds",							/* tp_name */
	sizeof(ads_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)ads_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)ads_str,					/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	ads_methods,						/* tp_methods */
	0,                                  /* tp_members */
	ads_getsets,						/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	ads_new,							/* tp_new */
	0,									/* tp_free */
};

static PyModuleDef ads_module = {
	PyModuleDef_HEAD_INIT,
	"igeAds",						// Module name to use with Python import statements
	"Ads Module.",					// Module description
	0,
	ads_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeAds() {
	PyObject* module = PyModule_Create(&ads_module);

	if (PyType_Ready(&AdsType) < 0) return NULL;
	if (PyType_Ready(&AdsAdmobType) < 0) return NULL;
	if (PyType_Ready(&AdsApplovinType) < 0) return NULL;
	if (PyType_Ready(&AdsFacebookType) < 0) return NULL;

	Py_INCREF(&AdsAdmobType);
	PyModule_AddObject(module, "admob", (PyObject*)&AdsAdmobType);

	Py_INCREF(&AdsApplovinType);
	PyModule_AddObject(module, "applovin", (PyObject*)&AdsApplovinType);

	Py_INCREF(&AdsFacebookType);
	PyModule_AddObject(module, "facebook", (PyObject*)&AdsFacebookType);

	return module;
}