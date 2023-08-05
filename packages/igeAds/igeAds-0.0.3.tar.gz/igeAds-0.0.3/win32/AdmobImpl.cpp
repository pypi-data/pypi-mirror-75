#include "AdmobImpl.h"
#include "Ads.h"
#include "AdsAdmob.h"

#include <windows.h>

// --- caching for fast access ---
static firebase::admob::BannerView* s_banner;
static firebase::admob::InterstitialAd* s_interstitial;

void AdsLogMessage(const char* format, ...) {
	va_list list;
	va_start(list, format);
	vprintf(format, list);
	va_end(list);
	printf("\n");
	fflush(stdout);
}

bool AdsProcessEvents(int msec)
{
    Sleep(msec);
    return false;
}

void AdmobImpl::Init()
{
	AdsAdmob::firebase_app = ::firebase::App::GetInstance();
    if(AdsAdmob::firebase_app == nullptr)
    {
		AdsAdmob::firebase_app = ::firebase::App::Create();
    }
}

void AdmobImpl::PlatformInit(const char* appID, const char* bannerAdUnit, const char* interstitialAdUnit, firebase::admob::AdSize banner_ad_size)
{
    LOG("Initializing the AdMob with Firebase API.");
    firebase::admob::Initialize(*AdsAdmob::firebase_app, appID);

    LOG("Initializing the AdMob banner.");
    s_banner = new firebase::admob::BannerView();
    s_banner->Initialize(AdsGetWindowContext(), bannerAdUnit, banner_ad_size);
    Ads::WaitForFutureCompletion(s_banner->InitializeLastResult());

    LOG("Initializing rewarded video.");
    namespace rewarded_video = firebase::admob::rewarded_video;
    rewarded_video::Initialize();
	Ads::WaitForFutureCompletion(rewarded_video::InitializeLastResult());

    LOG("Initializing interstitial video.");
    s_interstitial = new firebase::admob::InterstitialAd();
    s_interstitial->Initialize(AdsGetWindowContext(), interstitialAdUnit);
	Ads::WaitForFutureCompletion(s_interstitial->InitializeLastResult());
}

void AdmobImpl::PlatformListener(AdsAdmob::LoggingBannerViewListener* banner_listener, AdsAdmob::LoggingRewardedVideoListener* rewarded_listener, AdsAdmob::LoggingInterstitialAdListener* interstitial_listener)
{
    s_banner->SetListener(banner_listener);
    s_interstitial->SetListener(interstitial_listener);
    firebase::admob::rewarded_video::SetListener(rewarded_listener);
}

void AdmobImpl::PlatformRelease()
{
    delete s_banner;
    delete s_interstitial;
    firebase::admob::rewarded_video::Destroy();
    firebase::admob::Terminate();
}

void AdmobImpl::PlatformShowBanner(firebase::admob::AdRequest request, Ads::BannerPosition position, int left, int top)
{
    // Load the banner ad.
    LOG("Loading a banner ad.");
    s_banner->LoadAd(request);
    Ads::WaitForFutureCompletion(s_banner->LoadAdLastResult());

    // Make the BannerView visible.
    LOG("Showing the banner ad.");
    s_banner->Show();
    s_banner->MoveTo((firebase::admob::BannerView::Position)position);
}

void AdmobImpl::PlatformShowBanner(firebase::admob::AdRequest request, int x, int y)
{
    // Load the banner ad.
    LOG("Loading a banner ad.");
    s_banner->LoadAd(request);
	Ads::WaitForFutureCompletion(s_banner->LoadAdLastResult());

    // Make the BannerView visible.
    LOG("Showing the banner ad.");
    s_banner->Show();
    s_banner->MoveTo(x, y);
}

void AdmobImpl::PlatformHideBanner()
{
    s_banner->Hide();
    Ads::WaitForFutureCompletion(s_banner->HideLastResult());
}

void AdmobImpl::PlatformBannerMoveTo(Ads::BannerPosition position, int left, int top)
{
    s_banner->MoveTo((firebase::admob::BannerView::Position )position);
	Ads::WaitForFutureCompletion(s_banner->MoveToLastResult());
}

void AdmobImpl::PlatformBannerMoveTo(int x, int y)
{
    s_banner->MoveTo(x, y);
	Ads::WaitForFutureCompletion(s_banner->MoveToLastResult());
}

void AdmobImpl::PlatformLoadInterstitial(const char* interstitialAdUnit, firebase::admob::AdRequest request)
{
    s_interstitial->LoadAd(request);
}

void AdmobImpl::PlatformShowInterstitial(const char* interstitialAdUnit, firebase::admob::AdRequest request)
{
    //s_interstitial->LoadAd(request);
	Ads::WaitForFutureCompletion(s_interstitial->LoadAdLastResult());

    // When the InterstitialAd has loaded an ad, show it.
    LOG("Showing the interstitial ad.");
    s_interstitial->Show();
	Ads::WaitForFutureCompletion(s_interstitial->ShowLastResult());
}

void AdmobImpl::PlatformLoadRewardedVideo(const char* rewardedVideoAdUnit, firebase::admob::AdRequest request)
{
    namespace rewarded_video = firebase::admob::rewarded_video;

    LOG("Loading a rewarded video ad.");
    rewarded_video::LoadAd(rewardedVideoAdUnit, request);
}

void AdmobImpl::PlatformShowRewardedVideo(const char* rewardedVideoAdUnit, firebase::admob::AdRequest request)
{
    namespace rewarded_video = firebase::admob::rewarded_video;
    
    //LOG("Loading a rewarded video ad.");
    //rewarded_video::LoadAd(rewardedVideoAdUnit, request);
	Ads::WaitForFutureCompletion(rewarded_video::LoadAdLastResult());
    
    if (rewarded_video::LoadAdLastResult().error() == firebase::admob::kAdMobErrorNone)
    {
      LOG("Showing a rewarded video ad.");
      rewarded_video::Show(AdsGetWindowContext());
	  Ads::WaitForFutureCompletion(rewarded_video::ShowLastResult());
    }
}
