#include "AdsFacebook.h"
#include "FacebookAdsImpl.h"

AdsFacebook::AdsFacebook()
	: m_appID("")
	, m_bannerAdUnit("")
	, m_interstitialAdUnit("")
	, m_rewardedVideoAdUnit("")
	, m_adsImpl(new FacebookAdsImpl())
{
	LOG("AdsFacebook()");
}
AdsFacebook::~AdsFacebook()
{
	LOG("~AdsFacebook()");
}

void AdsFacebook::setupApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit)
{
	m_appID = adMobAppID;
	m_bannerAdUnit = bannerAdUnit;
	m_interstitialAdUnit = interstitialAdUnit;
	m_rewardedVideoAdUnit = rewardedVideoAdUnit;
}

void AdsFacebook::init()
{
    m_adsImpl->Init();

	m_adsImpl->PlatformInit(m_appID, m_bannerAdUnit, m_interstitialAdUnit, m_rewardedVideoAdUnit);

}

void AdsFacebook::release()
{
	m_adsImpl->PlatformRelease();
}

/*
void AdsFacebook::registerEventListener(AdmobHandlerFunc handler)
{
	//m_HandlerFunc = handler;
	//m_adsImpl->PlatformListener(m_banner_listener, m_rewarded_listener, m_interstitial_listener);
}*/

void AdsFacebook::showBanner(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformShowBanner(m_bannerAdUnit, position, left, top);
}

void AdsFacebook::bannerMoveTo(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformBannerMoveTo(position, left, top);
}

void AdsFacebook::bannerMoveTo(int x, int y)
{
}

void AdsFacebook::hideBanner()
{
	m_adsImpl->PlatformHideBanner();
}

void AdsFacebook::showInterstitial()
{
	m_adsImpl->PlatformShowInterstitial(m_interstitialAdUnit/*, m_request*/);
}

void AdsFacebook::showRewardedVideo()
{
	m_adsImpl->PlatformShowRewardedVideo(m_rewardedVideoAdUnit/*, m_request*/);
}

void AdsFacebook::pauseRewardedVideo()
{
}

void AdsFacebook::resumeRewardedVideo()
{
}
