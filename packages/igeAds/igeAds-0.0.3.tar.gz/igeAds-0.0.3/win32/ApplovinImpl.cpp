#include "ApplovinImpl.h"
#include "Ads.h"


void ApplovinImpl::Init()
{
}

void ApplovinImpl::PlatformInit(const char* appID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedAdUnit)
{
}

/*void ApplovinImpl::PlatformListener(AdsAdmob::LoggingBannerViewListener* banner_listener, AdsAdmob::LoggingRewardedVideoListener* rewarded_listener, AdsAdmob::LoggingInterstitialAdListener* interstitial_listener)
{

}*/

void ApplovinImpl::PlatformRelease()
{
}

void ApplovinImpl::PlatformShowBanner(const char* bannerAdUnit, Ads::BannerPosition position, int left, int top)
{
}

void ApplovinImpl::PlatformShowBanner(int x, int y)
{
}

void ApplovinImpl::PlatformHideBanner()
{
}

void ApplovinImpl::PlatformBannerMoveTo(Ads::BannerPosition position, int left, int top)
{
}

void ApplovinImpl::PlatformBannerMoveTo(int x, int y)
{
}

void ApplovinImpl::PlatformShowInterstitial(const char* interstitialAdUnit)
{
}

void ApplovinImpl::PlatformShowRewardedVideo(const char* rewardedVideoAdUnit)
{
}
