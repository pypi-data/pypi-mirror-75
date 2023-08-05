#pragma once
#include "Ads.h"
#include "json.hpp"
using json = nlohmann::json;

class ApplovinImpl;

class IGE_EXPORT AdsApplovin : public Ads
{
public:
	AdsApplovin();
	~AdsApplovin();
	void init();
	void release();
    
    void showBanner(Ads::BannerPosition position, int left, int top);
    void bannerMoveTo(Ads::BannerPosition position, int left, int top);
    void bannerMoveTo(int x, int y);
	void hideBanner();

	void showInterstitial();

	void showRewardedVideo();

	void setupApp(const char* appID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit);
	json dumpInfo() { return info_json; }

	static AdsApplovin* Instance()
	{
		if (instance == nullptr)
		{
			instance = new AdsApplovin();
		}
		return instance;
	}
    
private:
	const char* m_appID;
	const char* m_bannerAdUnit;
	const char* m_interstitialAdUnit;
	const char* m_rewardedVideoAdUnit;

    ApplovinImpl* m_adsImpl;
	json info_json;

	static AdsApplovin* instance;
};
