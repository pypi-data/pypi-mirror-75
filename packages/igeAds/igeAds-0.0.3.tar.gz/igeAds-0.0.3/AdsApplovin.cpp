#include "AdsApplovin.h"
#include "ApplovinImpl.h"

AdsApplovin* AdsApplovin::instance = nullptr;

AdsApplovin::AdsApplovin()
	: m_appID("")
	, m_bannerAdUnit("")
	, m_interstitialAdUnit("")
	, m_rewardedVideoAdUnit("")
	, m_adsImpl(new ApplovinImpl())
{
	LOG("AdsApplovin()");
}
AdsApplovin::~AdsApplovin()
{
	LOG("~AdsApplovin()");
}

void AdsApplovin::setupApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit)
{
	m_appID = adMobAppID;
	m_bannerAdUnit = bannerAdUnit;
	m_interstitialAdUnit = interstitialAdUnit;
	m_rewardedVideoAdUnit = rewardedVideoAdUnit;
}

void AdsApplovin::init()
{
    m_adsImpl->Init();

	m_adsImpl->PlatformInit(m_appID, m_bannerAdUnit, m_interstitialAdUnit, m_rewardedVideoAdUnit);

	info_json["banner"] = m_bannerAdUnit;
	info_json["interstitial"] = m_interstitialAdUnit;
	info_json["rewarded"] = m_rewardedVideoAdUnit;
}

void AdsApplovin::release()
{
	m_adsImpl->PlatformRelease();
}

void AdsApplovin::showBanner(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformShowBanner(m_bannerAdUnit, position, left, top);
}

void AdsApplovin::bannerMoveTo(Ads::BannerPosition position, int left, int top)
{
	m_adsImpl->PlatformBannerMoveTo(position, left, top);
}

void AdsApplovin::bannerMoveTo(int x, int y)
{
}

void AdsApplovin::hideBanner()
{
	m_adsImpl->PlatformHideBanner();
}

void AdsApplovin::showInterstitial()
{
	m_adsImpl->PlatformShowInterstitial(m_interstitialAdUnit);
}

void AdsApplovin::showRewardedVideo()
{
	m_adsImpl->PlatformShowRewardedVideo(m_rewardedVideoAdUnit);
}