//ads init
PyDoc_STRVAR(adsInit_doc,
	"init the ads system \n"\
	"\n"\
	"ads.init()");

//ads release
PyDoc_STRVAR(adsRelease_doc,
	"release the ads system\n"\
	"\n"\
	"ads.release()");

//ads release
PyDoc_STRVAR(adsUpdate_doc,
	"update the ads system\n"\
	"\n"\
	"ads.update()");

//ads admob registerEventListener_doc
PyDoc_STRVAR(adsAdmobRegisterEventListener_doc,
	"Register event listener to handle reward / presentation state changed.\n"\
	"\n"\
	"ads_admob.registerEventListener(func)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    func : func\n"\
	"        adsType : (string) defined Admob type(BannerView / Interstitial / RewardedVideo) ,\n"\
	"        amount : for rewarded video, it's reward amount the users get after video complete. For the presentation stage change, it's stage\n"\
	"            BannerView\n"\
	"                is currently hidden. kPresentationStateHidden = 0\n"\
	"                is visible, but does not contain an ad. kPresentationStateVisibleWithoutAd = 1\n"\
	"                is visible and contains an ad. kPresentationStateVisibleWithAd = 2\n"\
	"                is visible and has opened a partial overlay on the screen. kPresentationStateOpenedPartialOverlay = 3\n"\
	"                is completely covering the screen or has caused focus to leave the application (for example, when opening an external browser during a clickthrough). kPresentationStateCoveringUI = 4\n"\
	"            InterstitialAd\n"\
	"                is not currently being shown. kPresentationStateHidden = 0\n"\
	"                is being shown or has caused focus to leave the application (for example, when opening an external browser during a clickthrough).	kPresentationStateCoveringUI = 2\n"\
	"            RewardedVideo\n"\
	"                no ad is currently being shown. kPresentationStateHidden = 0\n"\
	"                is completely covering the screen or has caused focus to leave the application (for example, when opening an external browser during a clickthrough), but the video associated with the ad has yet to begin playing. kPresentationStateCoveringUI = 1\n"\
	"                all of the above conditions are true *except* that the video associated with the ad began playing at some point in the past. kPresentationStateVideoHasStarted = 2\n"\
	"                has played and completed. kPresentationStateVideoHasCompleted = 3");


//ads testcase
PyDoc_STRVAR(adsTestcase_doc,
	"The testcase for ads\n"\
	"\n"\
	"ads.testcase()");

//ads admob init
PyDoc_STRVAR(adsAdmobInit_doc,
	"init the ads Admob system \n"\
	"\n"\
	"ads_admob.init(adMobApp, bannerSize, gender, childDirectedTreatment, keywords, birthday, testDevicesIds)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    adMobApp : tuple\n"\
	"        4 Parameters : adMobAppID(char*) | bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)\n"\
	"    bannerSize : tuple (optional)\n"\
	"        The ads size for the BannerView.\n"\
	"        2 Parameters : width(int) | height(int)\n"\
    "    gender : int (optional)\n"\
	"        If the app is aware of the user's gender, it can be added to the targeting information. Otherwise, 'unknown' should be used.\n"\
	"        kGenderUnknown = 0, kGenderMale = 1, kGenderFemale = 2\n"\
    "    childDirectedTreatment : int (optional)\n"\
	"        Indicates whether an ad request is considered tagged for child-directed treatment.\n"\
	"        kChildDirectedTreatmentStateUnknown = 0, kChildDirectedTreatmentStateTagged = 1, kChildDirectedTreatmentStateNotTagged = 2\n"\
    "    keywords : tuple (optional)\n"\
	"        Keywords to be used in targeting.\n"\
    "    birthday : tuple (optional)\n"\
	"        The user's birthday, if known. Note that months are indexed from one.\n"\
	"        3 Parameters : day(int) | month(int) | year(int)\n"\
    "    testDevicesIds : tuple (optional)\n"\
	"        It's important to register the device IDs associated with any devices that will be used to test the app. This ensures that regardless of the ad unit ID, those devices will always receive test ads in compliance with AdMob policy.\n"\
    "Examples\n"\
	"----------\n"\
	"    ads_admob.init(('YOUR_IOS_ADMOB_APP_ID', 'ca-app-pub-3940256099942544/2934735716', 'ca-app-pub-3940256099942544/4411468910', 'ca-app-pub-3940256099942544/6386090517'), (320, 50), 1, 1, ('game', 'casual', 'hyper casual', 'mobile'), (1, 1, 2020), ('112F1C63CDDE8BAAEE287FDE3BA4C662',));\n"\
    );

//ads admob release
PyDoc_STRVAR(adsAdmobRelease_doc,
	"release the ads Admob system\n"\
	"\n"\
	"ads_admob.release()");

//ads admob testcase
PyDoc_STRVAR(adsAdmobTestcase_doc,
	"The testcase for ads Admob\n"\
	"\n"\
	"ads_admob.testcase()");

//ads admob showBanner
PyDoc_STRVAR(adsAdmobShowBanner_doc,
	"Loading then showing the banner ad.\n"\
	"\n"\
	"ads_admob.showBanner(x, y)\n"\
	"\n"\
    "Parameters\n"\
    "----------\n"\
    "    x : int\n"\
    "        The desired horizontal coordinate.\n"\
    "    y : int\n"\
    "        The desired vertical coordinate.\n"\
    "Show the @ref BannerView so that it's located at the given pre-defined position.\n"\
    "\n"\
    "ads_admob.showBanner(position)\n"\
    "\n"\
    "Parameters\n"\
    "----------\n"\
    "    position : int\n"\
    "        Top of the screen, horizontally centered. -> kPositionTop = 0,\n"\
    "        Bottom of the screen, horizontally centered. ->    kPositionBottom,\n"\
    "        Top-left corner of the screen. -> kPositionTopLeft,\n"\
    "        Top-right corner of the screen. -> kPositionTopRight,\n"\
    "        Bottom-left corner of the screen. -> kPositionBottomLeft,\n"\
    "        Bottom-right corner of the screen. -> kPositionBottomRight.");

//ads admob bannerMoveTo
PyDoc_STRVAR(adsAdmobBannerMoveTo_doc,
	"Moves the @ref BannerView so that its top-left corner is located at (x, y). Coordinates are in pixels from the top-left corner of the screen..\n"\
	"\n"\
	"ads_admob.bannerMoveTo(x, y)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    x : int\n"\
	"        The desired horizontal coordinate.\n"\
	"    y : int\n"\
	"        The desired vertical coordinate.\n"\
    "Moves the @ref BannerView so that it's located at the given pre-defined position.\n"\
	"\n"\
	"ads_admob.bannerMoveTo(position)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    position : int\n"\
	"        Top of the screen, horizontally centered. -> kPositionTop = 0,\n"\
	"        Bottom of the screen, horizontally centered. ->	kPositionBottom,\n"\
	"        Top-left corner of the screen. -> kPositionTopLeft,\n"\
	"        Top-right corner of the screen. -> kPositionTopRight,\n"\
	"        Bottom-left corner of the screen. -> kPositionBottomLeft,\n"\
	"        Bottom-right corner of the screen. -> kPositionBottomRight.");

//ads admob hideBanner
PyDoc_STRVAR(adsAdmobHideBanner_doc,
	"Hides the BannerView.\n"\
	"\n"\
	"ads_admob.hideBanner()");
    
//ads admob showInterstitial
PyDoc_STRVAR(adsAdmobShowInterstitial_doc,
	"Loading then showing the InterstitialAd ad.\n"\
	"\n"\
	"ads_admob.showInterstitial()");
    
//ads admob showRewardedVideo
PyDoc_STRVAR(adsAdmobShowRewardedVideo_doc,
	"Loading then showing the RewardedVideo ad.\n"\
	"\n"\
	"ads_admob.showRewardedVideo()");
    
//ads admob pauseRewardedVideo
PyDoc_STRVAR(adsAdmobPauseRewardedVideo_doc,
	"Pauses any background processing associated with rewarded video. Should be called whenever the C++ engine pauses or the application loses focus.\n"\
	"\n"\
	"ads_admob.pauseRewardedVideo()");

//ads admob resumeRewardedVideo
PyDoc_STRVAR(adsAdmobResumeRewardedVideo_doc,
	"Resumes the rewarded video system after pausing.\n"\
	"\n"\
	"ads_admob.resumeRewardedVideo()");    

//ads Applovin init
PyDoc_STRVAR(adsApplovinInit_doc,
	"init the ads applovin system \n"\
	"\n"\
	"ads_applovin.init(android=(bannerAdUnit, interstitialAdUnit, rewardedVideoAdUnit), ios=(bannerAdUnit, interstitialAdUnit, rewardedVideoAdUnit))\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    bannerAdUnit : string\n"\
	"    interstitialAdUnit : string\n"\
	"    rewardedVideoAdUnit : string\n"\
	"----------\n"\
	"    ads_applovin.init(android=('50781ce08cccd9e5', '5ad29e98a6ed623c', '1a61c958e699b07a'), ios=('543b53f89be58d39', 'ded4ed1fe2aa54e0', '3602eab376c95aa3'))");

//ads Applovin release
PyDoc_STRVAR(adsApplovinRelease_doc,
	"release the ads applovin system\n"\
	"\n"\
	"ads_applovin.release()");

//ads Applovin showBanner
PyDoc_STRVAR(adsApplovinShowBanner_doc,
	"Loading then showing the banner ad.\n"\
	"\n"\
	"ads_applovin.showBanner(position, left, top)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    position : int\n"\
	"        Top of the screen, horizontally centered. -> kPositionTop = 0,\n"\
	"        Bottom of the screen, horizontally centered. ->    kPositionBottom,\n"\
	"        Top-left corner of the screen. -> kPositionTopLeft,\n"\
	"        Top-right corner of the screen. -> kPositionTopRight,\n"\
	"        Bottom-left corner of the screen. -> kPositionBottomLeft,\n"\
	"        Bottom-right corner of the screen. -> kPositionBottomRight.\n"\
	"    left : int\n"\
	"        The desired horizontal coordinate.\n"\
	"    top : int\n"\
	"        The desired vertical coordinate.");

//ads Applovin bannerMoveTo
PyDoc_STRVAR(adsApplovinBannerMoveTo_doc,
	"Moves the @ref BannerView so that it's located at the given pre-defined position.\n"\
	"\n"\
	"ads_applovin.bannerMoveTo(position, left, top)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    position : int\n"\
	"        Top of the screen, horizontally centered. -> kPositionTop = 0,\n"\
	"        Bottom of the screen, horizontally centered. ->	kPositionBottom,\n"\
	"        Top-left corner of the screen. -> kPositionTopLeft,\n"\
	"        Top-right corner of the screen. -> kPositionTopRight,\n"\
	"        Bottom-left corner of the screen. -> kPositionBottomLeft,\n"\
	"        Bottom-right corner of the screen. -> kPositionBottomRight.\n"\
	"    left : int\n"\
	"        The desired horizontal coordinate.\n"\
	"    top : int\n"\
	"        The desired vertical coordinate.");

//ads Applovin hideBanner
PyDoc_STRVAR(adsApplovinHideBanner_doc,
	"Hides the BannerView.\n"\
	"\n"\
	"ads_applovin.hideBanner()");

//ads Applovin showInterstitial
PyDoc_STRVAR(adsApplovinShowInterstitial_doc,
	"Loading then showing the InterstitialAd ad.\n"\
	"\n"\
	"ads_applovin.showInterstitial()");

//ads Applovin showRewardedVideo
PyDoc_STRVAR(adsApplovinShowRewardedVideo_doc,
	"Loading then showing the RewardedVideo ad.\n"\
	"\n"\
	"ads_applovin.showRewardedVideo()");
