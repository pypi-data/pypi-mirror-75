#include "AdsAdmob.h"
#include "AdmobImpl.h"

#include "firebase/admob/interstitial_ad.h"
#include "firebase/admob/rewarded_video.h"
#include "firebase/admob/types.h"
#include "firebase/app.h"
#include "firebase/future.h"

namespace ads
{
	// The AdMob app IDs for the test app.
#if defined(__ANDROID__)
// If you change the AdMob app ID for your Android app, make sure to change it
// in AndroidManifest.xml as well.
	const char* kAdMobAppID = "YOUR_ANDROID_ADMOB_APP_ID";
#else
// If you change the AdMob app ID for your iOS app, make sure to change the
// value for "GADApplicationIdentifier" in your Info.plist as well.
	const char* kAdMobAppID = "YOUR_IOS_ADMOB_APP_ID";
#endif

	// These ad units IDs have been created specifically for testing, and will
	// always return test ads.
#if defined(__ANDROID__)
	const char* kBannerAdUnit = "ca-app-pub-3940256099942544/6300978111";
	const char* kInterstitialAdUnit = "ca-app-pub-3940256099942544/1033173712";
	const char* kRewardedVideoAdUnit = "ca-app-pub-3940256099942544/2888167318";
#else
	const char* kBannerAdUnit = "ca-app-pub-3940256099942544/2934735716";
	const char* kInterstitialAdUnit = "ca-app-pub-3940256099942544/4411468910";
	const char* kRewardedVideoAdUnit = "ca-app-pub-3940256099942544/6386090517";
#endif

	// Standard mobile banner size is 320x50.
	static const int kBannerWidth = 320;
	static const int kBannerHeight = 50;

	// Sample keywords to use in making the request.
	static const char* kKeywords[] = { "AdMob", "C++", "Fun" };

	// Sample test device IDs to use in making the request.
	static const char* kTestDeviceIDs[] = { "2077ef9a63d2b398840261c8221a0c9b",
										   "098fe087d987c9a878965454a65654d7" };

	// Sample birthday value to use in making the request.
	static const int kBirthdayDay = 10;
	static const int kBirthdayMonth = 11;
	static const int kBirthdayYear = 1976;
}

firebase::App * AdsAdmob::firebase_app = nullptr;
AdsAdmob* AdsAdmob::adsMobInstance = nullptr;

AdsAdmob::AdsAdmob()
	: m_appID(ads::kAdMobAppID)
	, m_bannerAdUnit(ads::kBannerAdUnit)
	, m_interstitialAdUnit(ads::kInterstitialAdUnit)
	, m_rewardedVideoAdUnit(ads::kRewardedVideoAdUnit)
	, m_gender(admob::kGenderUnknown)
	, m_childDirectedTreatmentState(admob::kChildDirectedTreatmentStateTagged)
	, m_bannerWidth(ads::kBannerWidth)
	, m_bannerHeight(ads::kBannerHeight)
	, m_keywords(ads::kKeywords)
	, m_keywordCount(sizeof(ads::kKeywords) / sizeof(ads::kKeywords[0]))
	, m_testDeviceIds(ads::kTestDeviceIDs)
	, m_testDeviceIdCount(sizeof(ads::kTestDeviceIDs) / sizeof(ads::kTestDeviceIDs[0]))
	, m_birthdayDay(ads::kBirthdayDay)
	, m_birthdayMonth(ads::kBirthdayMonth)
	, m_birthdayYear(ads::kBirthdayYear)
	, m_request()
    , m_banner_ad_size()
	, m_banner_listener(nullptr)
	, m_interstitial_listener(nullptr)
	, m_rewarded_listener(nullptr)
	, m_adsImpl(new AdmobImpl())
{
	LOG("FirebaseAdmob()");
    adsMobInstance = this;
}
AdsAdmob::~AdsAdmob()
{
	LOG("~FirebaseAdmob()");
	delete(adsMobInstance);
    adsMobInstance = nullptr;
}

void AdsAdmob::setupApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit)
{
    m_appID = adMobAppID;
	m_bannerAdUnit = bannerAdUnit;
	m_interstitialAdUnit = interstitialAdUnit;
	m_rewardedVideoAdUnit = rewardedVideoAdUnit;
}

void AdsAdmob::setBannerSize(uint32_t width, uint32_t height)
{
	m_bannerWidth = width;
	m_bannerHeight = height;
}

void AdsAdmob::setGender(admob::Gender gender)
{
	m_gender = gender;
}

void AdsAdmob::setChildDirectedTreatmentState(admob::ChildDirectedTreatmentState state)
{
	m_childDirectedTreatmentState = state;
}

void AdsAdmob::setKeywords(uint32_t count, const char** keywords)
{
	m_keywordCount = count;
	m_keywords = keywords;
}

void AdsAdmob::setTestDeviceIds(uint32_t count, const char** testDeviceIds)
{
	m_testDeviceIdCount = count;
	m_testDeviceIds = testDeviceIds;
}

void AdsAdmob::setBirthday(uint32_t day, uint32_t month, uint32_t year)
{
	m_birthdayDay = day;
	m_birthdayMonth = month;
	m_birthdayYear = year;
}

void AdsAdmob::init()
{
    m_adsImpl->Init();
	// If the app is aware of the user's gender, it can be added to the targeting
	// information. Otherwise, "unknown" should be used.
	m_request.gender = m_gender;

	// This value allows publishers to specify whether they would like the request
	// to be treated as child-directed for purposes of the Children’s Online
	// Privacy Protection Act (COPPA).
	// See http://business.ftc.gov/privacy-and-security/childrens-privacy.
	m_request.tagged_for_child_directed_treatment = m_childDirectedTreatmentState;

	// The user's birthday, if known. Note that months are indexed from one.
	m_request.birthday_day = m_birthdayDay;
	m_request.birthday_month = m_birthdayMonth;
	m_request.birthday_year = m_birthdayYear;

	// Additional keywords to be used in targeting.
	m_request.keyword_count = m_keywordCount;
	m_request.keywords = m_keywords;

	// This example uses ad units that are specially configured to return test ads
	// for every request. When using your own ad unit IDs, however, it's important
	// to register the device IDs associated with any devices that will be used to
	// test the app. This ensures that regardless of the ad unit ID, those
	// devices will always receive test ads in compliance with AdMob policy.
	//
	// Device IDs can be obtained by checking the logcat or the Xcode log while
	// debugging. They appear as a long string of hex characters.
	m_request.test_device_id_count = m_testDeviceIdCount;
	m_request.test_device_ids = m_testDeviceIds;

	// Create an ad size for the BannerView.	
	m_banner_ad_size.ad_size_type = admob::kAdSizeStandard;
	m_banner_ad_size.width = m_bannerWidth;
	m_banner_ad_size.height = m_bannerHeight;
    
    // Initializing the AdMob with Firebase API.
	m_adsImpl->PlatformInit(m_appID, m_bannerAdUnit, m_interstitialAdUnit, m_banner_ad_size);
	loadInterstitial();
	loadRewardedVideo();

    // Initializing the AdMob listener.

    m_banner_listener = new LoggingBannerViewListener();
    m_interstitial_listener = new LoggingInterstitialAdListener();
    m_rewarded_listener = new LoggingRewardedVideoListener();

	m_adsImpl->PlatformListener(m_banner_listener, m_rewarded_listener, m_interstitial_listener);
}

void AdsAdmob::release()
{
	LOG("FirebaseAdmob::release()");
	
	// cleanup the listener
	delete m_banner_listener;
	delete m_interstitial_listener;
	delete m_rewarded_listener;
    
    // platform release resource
	m_adsImpl->PlatformRelease();
}

//void AdsAdmob::registerEventListener(AdmobHandlerFunc handler)
//{
//	m_HandlerFunc = handler;
//	m_adsImpl->PlatformListener(m_banner_listener, m_rewarded_listener, m_interstitial_listener);
//}

void AdsAdmob::showBanner(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformShowBanner(m_request, position, left, top);
}

void AdsAdmob::showBanner(int x, int y)
{
	m_adsImpl->PlatformShowBanner(m_request, x, y);
}

void AdsAdmob::bannerMoveTo(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformBannerMoveTo(position, left, top);
}

void AdsAdmob::bannerMoveTo(int x, int y)
{
	m_adsImpl->PlatformBannerMoveTo(x, y);
}

void AdsAdmob::hideBanner()
{
	m_adsImpl->PlatformHideBanner();
}

void AdsAdmob::loadInterstitial()
{
    m_adsImpl->PlatformLoadInterstitial(m_interstitialAdUnit, m_request);
}

void AdsAdmob::showInterstitial()
{
	m_adsImpl->PlatformShowInterstitial(m_interstitialAdUnit, m_request);
}

void AdsAdmob::loadRewardedVideo()
{
    m_adsImpl->PlatformLoadRewardedVideo(m_rewardedVideoAdUnit, m_request);
}

void AdsAdmob::showRewardedVideo()
{
	m_adsImpl->PlatformShowRewardedVideo(m_rewardedVideoAdUnit, m_request);
}

void AdsAdmob::pauseRewardedVideo()
{
	rewarded_video::Pause();
	WaitForFutureCompletion(rewarded_video::PauseLastResult());
}

void AdsAdmob::resumeRewardedVideo()
{
	rewarded_video::Resume();
	WaitForFutureCompletion(rewarded_video::ResumeLastResult());
}

void AdsAdmob::testcase()
{
	showBanner(Ads::BannerPosition::kPositionTop, 0, 0);

	// Move to each of the six pre-defined positions.
	bannerMoveTo(Ads::BannerPosition::kPositionTop, 0, 0);
	bannerMoveTo(Ads::BannerPosition::kPositionTopLeft, 0, 0);
	bannerMoveTo(Ads::BannerPosition::kPositionTopRight, 0, 0);
	bannerMoveTo(Ads::BannerPosition::kPositionBottom, 0, 0);
	bannerMoveTo(Ads::BannerPosition::kPositionBottomLeft, 0, 0);
	bannerMoveTo(Ads::BannerPosition::kPositionBottomRight, 0, 0);

	// Try some coordinate moves.
	bannerMoveTo(100, 300);
	bannerMoveTo(100, 400);

	// Try hiding and showing the BannerView.
	hideBanner();
	showBanner(100, 300);
	// A few last moves after showing it again.
	bannerMoveTo(100, 300);
	bannerMoveTo(100, 400);
    hideBanner();
	
	// When the InterstitialAd is initialized, load an ad.
	showInterstitial();

	// Loading a rewarded video ad.
	showRewardedVideo();
	// Normally Pause and Resume would be called in response to the app pausing
	// or losing focus. This is just a test.
	pauseRewardedVideo();
	resumeRewardedVideo();
    
    // release the resource
    rewarded_video::Destroy();
    admob::Terminate();

	LOG("Done!");
}
