#include "Ads.h"
#include "AdmobImpl.h"

#include "firebase/app.h"
#include "firebase/future.h"
#include "firebase/admob.h"
#include "firebase/internal/platform.h"

#if defined(_WIN32)
#include <windows.h>
#include <stdarg.h>

WindowContext AdsGetWindowContext()
{
    return nullptr;
}

static LARGE_INTEGER freq;
#elif defined(__ANDROID__)
#include <unistd.h>
#include <jni.h>
#include "SDL.h"

jobject AdsGetActivity()
{
    return (jobject)SDL_AndroidGetActivity();
}

// Get the window context. For Android, it's a jobject pointing to the Activity.
jobject AdsGetWindowContext()
{
    return AdsGetActivity();
}
#elif defined(__APPLE__)
#include <unistd.h>
#include <stdarg.h>
#include <mach/mach_time.h>

extern "C" WindowContext GetWindowContext();
WindowContext AdsGetWindowContext()
{
#if FIREBASE_PLATFORM_IOS
    return GetWindowContext();
#else // not yet supported MacOS
    return nullptr;
#endif
}
mach_timebase_info_data_t timebase;
#endif // __APPLE__

AdHandlerFunc Ads::m_HandlerFunc;

const char* Ads::BANNER_TYPE_CB = "BannerView";
const char* Ads::INTERSTITIAL_TYPE_CB = "Interstitial";
const char* Ads::REWARDED_TYPE_CB = "RewardedVideo";

const char* Ads::APPLOVIN_TYPE = "Applovin";
const char* Ads::FACEBOOK_TYPE = "Facebook";

const char* Ads::STATE_CHANGED = "PresentationStateChanged";
const char* Ads::STATE_REWARDED = "Rewarded";
const char* Ads::STATE_ERROR = "Error";

Ads::Ads()
{
#if defined(_WIN32)
    QueryPerformanceFrequency(&freq);
#elif defined(__APPLE__)
    mach_timebase_info(&timebase);
#endif
}

Ads::~Ads()
{
}

void Ads::init()
{
}

void Ads::release()
{
}

void Ads::WaitForFutureCompletion(firebase::FutureBase future, int msec, bool timeout, double value)
{
    double time = GetTime();
    while (!AdsProcessEvents(msec))
    {
        double elapsedTime = GetTime() - time;
        if (future.status() != firebase::kFutureStatusPending || (timeout && elapsedTime > value))
        {
            break;
        }
    }

    if (future.error() != firebase::admob::kAdMobErrorNone)
    {
        LOG("ADMOB ERROR: Action failed with error code %d and message \"%s\".\n",
            future.error(), future.error_message());
    }
}

double Ads::GetTime()
{
#if defined(_WIN32)
    static LARGE_INTEGER cuurentTime;
    QueryPerformanceCounter(&cuurentTime);
    return (double)cuurentTime.QuadPart / (double)freq.QuadPart;
#elif defined __ANDROID__
    struct timespec tv;
    clock_gettime(CLOCK_MONOTONIC, &tv);
    return (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
    uint64_t t = mach_absolute_time();
    double tsec = (double)t * (double)timebase.numer / (double)timebase.denom / 1000000000.0;
    return tsec;
#endif
}

void Ads::registerEventListener(AdHandlerFunc handler)
{
	m_HandlerFunc = handler;
}

void Ads::AdsCallback(const char* provider, const char* adsType, int number, const char* name)
{
    if(m_HandlerFunc != nullptr)
    {
        m_HandlerFunc(provider, adsType, number, name);
    }
}
