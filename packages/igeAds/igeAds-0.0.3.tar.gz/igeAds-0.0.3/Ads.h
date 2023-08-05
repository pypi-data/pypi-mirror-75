#pragma once

#include <stdio.h>
#include <assert.h>
#include <stdint.h>

#if defined _WIN32
    #include <time.h>
#elif defined(__ANDROID__)
    #include <jni.h>
    #include <sys/time.h>
    #include <time.h>
#elif defined __APPLE__
	#include <objc/objc.h>
	#include <mach/mach_time.h>
#endif

#ifdef _WIN32
    #define IGE_EXPORT __declspec(dllexport)
#else
    #define IGE_EXPORT
#endif


#ifdef NDEBUG
    #define LOG_VERBOSE(...)
    #define LOG_DEBUG(...)
    #define LOG(...)
    #define LOG_WARN(...)
    #define LOG_ERROR(...)
#else
    #if defined(__ANDROID__)
        #include <android/log.h>

        #define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "Ads", __VA_ARGS__);
        #define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "Ads", __VA_ARGS__);
        #define LOG(...) __android_log_print(ANDROID_LOG_INFO, "Ads", __VA_ARGS__);
        #define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "Ads", __VA_ARGS__);
        #define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "Ads", __VA_ARGS__);
    #else
        void AdsLogMessage(const char* format, ...);

        #define LOG_VERBOSE(...) AdsLogMessage(__VA_ARGS__);
        #define LOG_DEBUG(...) AdsLogMessage(__VA_ARGS__);
        #define LOG(...) AdsLogMessage(__VA_ARGS__);
        #define LOG_WARN(...) AdsLogMessage(__VA_ARGS__);
        #define LOG_ERROR(...) AdsLogMessage(__VA_ARGS__);
    #endif
#endif

// WindowContext represents the handle to the parent window.  It's type
// (and usage) vary based on the OS.
#if defined(__ANDROID__)
    typedef jobject WindowContext;  // A jobject to the Java Activity.

    JNIEnv* AdsGetJniEnv(bool &envAttached);
    jobject AdsGetActivity();
    void AdsDetachVM(bool envAttached);
#elif defined(__APPLE__)
    typedef id WindowContext;  // A pointer to an iOS UIView.
#else
    typedef void* WindowContext;  // A void* for any other environments.
#endif
WindowContext AdsGetWindowContext();

typedef void (*AdHandlerFunc)(const char* provider, const char* adsType, int number, const char* name);
bool AdsProcessEvents(int msec);

namespace firebase
{
	class FutureBase;
	class App;
}

struct AdsCallback
{
	const char* adsProvider;
	const char* adsType;
	int adsNumber;
	const char* adsName;

	AdsCallback(const char* provider, const char* type, int number, const char* name)
		: adsProvider(provider)
		, adsType(type)
		, adsNumber(number)
		, adsName(name)
	{
	}
};

class IGE_EXPORT Ads
{
public:

    enum BannerPosition         /// The possible screen positions for a @ref BannerView.
    {
        kPositionTop = 0,       /// Top of the screen, horizontally centered.
        kPositionBottom,        /// Bottom of the screen, horizontally centered.
        kPositionTopLeft,       /// Top-left corner of the screen.
        kPositionTopRight,      /// Top-right corner of the screen.
        kPositionBottomLeft,    /// Bottom-left corner of the screen.
        kPositionBottomRight,   /// Bottom-right corner of the screen.
    };

	Ads();
	~Ads();
	void init();
	void release();

	void registerEventListener(AdHandlerFunc handler);

    static void WaitForFutureCompletion(firebase::FutureBase future, int msec = 1000, bool timeout = true, double value = 5.0);
    static double GetTime();
    static void AdsCallback(const char* provider, const char* adsType, int number, const char* name);
public:
	static AdHandlerFunc m_HandlerFunc;

    static const char* BANNER_TYPE_CB;
    static const char* INTERSTITIAL_TYPE_CB;
    static const char* REWARDED_TYPE_CB;

    static const char* APPLOVIN_TYPE;
    static const char* FACEBOOK_TYPE;

    static const char* STATE_CHANGED;
    static const char* STATE_REWARDED;
    static const char* STATE_ERROR;

    enum class RewardPresentationState : int
    {
        kPresentationStateHidden = 0,
        kPresentationStateCoveringUI,
        kPresentationStateVideoHasStarted,
        kPresentationStateVideoHasCompleted,
        kPresentationStateCoveringUIClicked,
    };

    enum class InterstitialPresentationState : int
    {
        kPresentationStateHidden = 0,
        kPresentationStateCoveringUI,
        kPresentationStateCoveringUIClicked,
    };

    enum class BannerPresentationState : int
    {
        kPresentationStateHidden = 0,
        kPresentationStateVisibleWithoutAd,
        kPresentationStateVisibleWithAd,
        kPresentationStateOpenedPartialOverlay,
        kPresentationStateCoveringUI,
    };
};
