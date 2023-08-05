#pragma once
#include "Ads.h"
#include "firebase/admob.h"
#include "firebase/admob/banner_view.h"

namespace admob = firebase::admob;
namespace rewarded_video = admob::rewarded_video;

class AdmobImpl;

class IGE_EXPORT AdsAdmob : public Ads
{
public:
    class LoggingRewardedVideoListener
            : public admob::rewarded_video::Listener {
    public:
        LoggingRewardedVideoListener() {}
        void OnRewarded(admob::rewarded_video::RewardItem reward) override {
            LOG("Rewarding user with %f %s.", reward.amount,
                reward.reward_type.c_str());
            Ads::AdsCallback("Admob", "RewardedVideo", reward.amount, reward.reward_type.c_str());
        }
        void OnPresentationStateChanged(
                admob::rewarded_video::PresentationState state) override {
            LOG("Rewarded video PresentationState has changed to %d.", state);
            Ads::AdsCallback("Admob", "RewardedVideo", state, "PresentationStateChanged");

			if(state == admob::rewarded_video::PresentationState::kPresentationStateHidden && adsMobInstance)
			{
				adsMobInstance->loadRewardedVideo();
			}
        }
    };

    class LoggingInterstitialAdListener
            : public admob::InterstitialAd::Listener {
    public:
        LoggingInterstitialAdListener() {}
        void OnPresentationStateChanged(
                admob::InterstitialAd* interstitial_ad,
                admob::InterstitialAd::PresentationState state) override {
            LOG("InterstitialAd PresentationState has changed to %d.", state);
            Ads::AdsCallback("Admob", "Interstitial", state, "PresentationStateChanged");

            if(state == admob::InterstitialAd::PresentationState::kPresentationStateHidden && adsMobInstance)
			{
				adsMobInstance->loadInterstitial();
			}
        }
    };

    class LoggingBannerViewListener : public admob::BannerView::Listener {
    public:
        LoggingBannerViewListener() {}
        void OnPresentationStateChanged(
                admob::BannerView* banner_view,
                admob::BannerView::PresentationState state) override {
            LOG("BannerView PresentationState has changed to %d.", state);
            Ads::AdsCallback("Admob", "BannerView", state, "PresentationStateChanged");
        }
        void OnBoundingBoxChanged(admob::BannerView* banner_view,
                                  admob::BoundingBox box) override {
            LOG("BannerView BoundingBox has changed to (x: %d, y: %d, width: %d, height %d).", box.x, box.y, box.width, box.height);
        }
    };

public:
	AdsAdmob();
	~AdsAdmob();
	void init();
	void release();
	void testcase();

    void showBanner(Ads::BannerPosition position, int left, int top);
    void showBanner(int x, int y);
	void bannerMoveTo(Ads::BannerPosition position, int left, int top);
	void bannerMoveTo(int x, int y);
	void hideBanner();

	void loadInterstitial();
	void showInterstitial();

	void loadRewardedVideo();
	void showRewardedVideo();
	void pauseRewardedVideo();
	void resumeRewardedVideo();

	void setupApp(const char* adMobAppID, const char* bannerAdUnit, const char* interstitialAdUnit, const char* rewardedVideoAdUnit);
	void setBannerSize(uint32_t width, uint32_t height);
	void setGender(admob::Gender gender);
	void setChildDirectedTreatmentState(admob::ChildDirectedTreatmentState state);
	void setKeywords(uint32_t count, const char** keywords);
	void setTestDeviceIds(uint32_t count, const char** testDeviceIds);
	void setBirthday(uint32_t day, uint32_t month, uint32_t year);
private:
	const char* m_appID;
	const char* m_bannerAdUnit;
	const char* m_interstitialAdUnit;
	const char* m_rewardedVideoAdUnit;
	admob::Gender m_gender;
	admob::ChildDirectedTreatmentState m_childDirectedTreatmentState;
	uint32_t m_bannerWidth;
	uint32_t m_bannerHeight;
	const char** m_keywords;
	uint32_t m_keywordCount;
	const char** m_testDeviceIds;
	uint32_t m_testDeviceIdCount;
	uint32_t m_birthdayDay;
	uint32_t m_birthdayMonth;
	uint32_t m_birthdayYear;
    
    firebase::admob::AdRequest m_request;
    admob::AdSize m_banner_ad_size;

	LoggingBannerViewListener* m_banner_listener;
	LoggingInterstitialAdListener* m_interstitial_listener;
	LoggingRewardedVideoListener* m_rewarded_listener;

    AdmobImpl* m_adsImpl;
public:
    
    static firebase::App* firebase_app;
    static AdsAdmob* adsMobInstance;
};
