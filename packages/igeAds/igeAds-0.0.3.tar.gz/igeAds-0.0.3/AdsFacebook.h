#pragma once
#include "Ads.h"

class FacebookAdsImpl;

class IGE_EXPORT AdsFacebook : public Ads
{
public:
	AdsFacebook();
	~AdsFacebook();
	void init();
	void release();
	void testcase();
    
    void showBanner(Ads::BannerPosition position, int left, int top);
    void bannerMoveTo(Ads::BannerPosition position, int left, int top);
	void bannerMoveTo(int x, int y);
	void hideBanner();

	void showInterstitial();

	void showRewardedVideo();
	void pauseRewardedVideo();
	void resumeRewardedVideo();

	void setupApp(const char* appID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit);
private:
	const char* m_appID;
	const char* m_bannerAdUnit;
	const char* m_interstitialAdUnit;
	const char* m_rewardedVideoAdUnit;
	uint32_t m_bannerWidth;
	uint32_t m_bannerHeight;
	const char** m_keywords;
	uint32_t m_keywordCount;
	const char** m_testDeviceIds;
	uint32_t m_testDeviceIdCount;
	uint32_t m_birthdayDay;
	uint32_t m_birthdayMonth;
	uint32_t m_birthdayYear;

	//LoggingBannerViewListener* m_banner_listener;
	//LoggingInterstitialAdListener* m_interstitial_listener;
	//LoggingRewardedVideoListener* m_rewarded_listener;

    FacebookAdsImpl* m_adsImpl;
public:

    //static AdmobHandlerFunc m_HandlerFunc;
};
