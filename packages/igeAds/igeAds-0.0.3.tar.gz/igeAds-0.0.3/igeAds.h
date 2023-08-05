#include <Python.h>
#include "Ads.h"
#include "AdsAdmob.h"
#include "AdsApplovin.h"
#include "AdsFacebook.h"

typedef struct {
	PyObject_HEAD
		Ads* ads;
} ads_obj;


typedef struct {
	PyObject_HEAD
		AdsAdmob* adsAdmob;
} adsAdmob_obj;

typedef struct {
	PyObject_HEAD
		AdsApplovin* adsApplovin;
} adsApplovin_obj;

typedef struct {
	PyObject_HEAD
	AdsFacebook* adsFacebook;
} adsFacebook_obj;

extern PyTypeObject AdsType;
extern PyTypeObject AdsAdmobType;
extern PyTypeObject AdsApplovinType;
extern PyTypeObject AdsFacebookType;
