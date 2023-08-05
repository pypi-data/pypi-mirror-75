#include "FacebookAdsImpl.h"
#include "Ads.h"

void FacebookAdsImpl::Init()
{
}

void FacebookAdsImpl::PlatformInit(const char* appID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedAdUnit)//, firebase::admob::AdSize banner_ad_size)
{
}

/*void FacebookAdsImpl::PlatformListener(AdsAdmob::LoggingBannerViewListener* banner_listener, AdsAdmob::LoggingRewardedVideoListener* rewarded_listener, AdsAdmob::LoggingInterstitialAdListener* interstitial_listener)
{

}*/

void FacebookAdsImpl::PlatformRelease()
{
}

void FacebookAdsImpl::PlatformShowBanner(const char* bannerAdUnit, Ads::BannerPosition position, int left, int top)
{
}

void FacebookAdsImpl::PlatformShowBanner(int x, int y)
{
}

void FacebookAdsImpl::PlatformHideBanner()
{
}

void FacebookAdsImpl::PlatformBannerMoveTo(Ads::BannerPosition position, int left, int top)
{
}

void FacebookAdsImpl::PlatformBannerMoveTo(int x, int y)
{
}

void FacebookAdsImpl::PlatformShowInterstitial(const char* interstitialAdUnit)
{
}

void FacebookAdsImpl::PlatformShowRewardedVideo(const char* rewardedVideoAdUnit)
{
}
