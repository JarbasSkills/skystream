from ovos_utils.skills.templates.common_play import BetterCommonPlaySkill
from ovos_utils.playback import CPSMatchType, CPSPlayback, CPSMatchConfidence
from os.path import join, dirname


class SkyStream(BetterCommonPlaySkill):
    def __init__(self):
        super(SkyStream, self).__init__(name="SkyStream")
        self.url = "https://skynews2-plutolive-vo.akamaized.net" \
                 "/cdhlsskynewsamericas/1013/latest.m3u8?serverSideAds=true"
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.AUDIO,
                                CPSMatchType.VIDEO,
                                CPSMatchType.TV,
                                CPSMatchType.NEWS]
        self.default_image = join(dirname(__file__), "ui", "images",
                                  "logo.png")
        self.skill_logo = self.default_image
        self.skill_icon = self.default_image
        self.default_bg = join(dirname(__file__), "ui", "images",
                               "background.png")

    # better_cps
    def CPS_search(self, phrase, media_type):
        """Analyze phrase to see if it is a play-able phrase with this skill.

        Arguments:
            phrase (str): User phrase uttered after "Play", e.g. "some music"
            media_type (CPSMatchType): requested CPSMatchType to search for

        Returns:
            search_results (list): list of dictionaries with result entries
            {
                "match_confidence": CPSMatchConfidence.HIGH,
                "media_type":  CPSMatchType.MUSIC,
                "uri": "https://audioservice.or.gui.will.play.this",
                "playback": CPSPlayback.GUI,
                "image": "http://optional.audioservice.jpg",
                "bg_image": "http://optional.audioservice.background.jpg"
            }
        """
        score = 0
        if media_type == CPSMatchType.TV:
            score += 30
        if media_type == CPSMatchType.NEWS or self.voc_match(phrase, "news"):
            score += 60

        if self.voc_match(phrase, "skystream"):
            score += 80
        if score >= CPSMatchConfidence.AVERAGE:
            if media_type not in [CPSMatchType.AUDIO, CPSMatchType.VIDEO,
                                  CPSMatchType.TV]:
                # audio + video results
                results = [
                    {
                        # video match
                        "match_confidence": min(100, score),
                        "media_type": CPSMatchType.NEWS,
                        "uri": self.url,
                        "playback": CPSPlayback.GUI,
                        "image": self.default_image,
                        "bg_image": self.default_bg,
                        "skill_icon": self.skill_icon,
                        "skill_logo": self.skill_logo,
                        "length": 0,
                        "title": "SkyStream",
                        "author": "SkyStream",
                        "album": "SkyStream"
                    },
                    {  # audio match
                        "match_confidence": min(100, score - 5),
                        "media_type": CPSMatchType.NEWS,
                        "uri": self.url,
                        "playback": CPSPlayback.AUDIO,
                        "image": self.default_image,
                        "bg_image": self.default_bg,
                        "skill_icon": self.skill_icon,
                        "skill_logo": self.skill_logo,
                        "length": 0,
                        "title": "SkyStream (Audio)",
                        "author": "SkyStream",
                        "album": "SkyStream"
                    }
                ]
            elif media_type == CPSMatchType.AUDIO:
                # audio only results
                results = [
                    {
                        # video match
                        "match_confidence": min(100, score),
                        "media_type": CPSMatchType.NEWS,
                        "uri": self.url,
                        "playback": CPSPlayback.AUDIO,
                        "image": self.default_image,
                        "bg_image": self.default_bg,
                        "skill_icon": self.skill_icon,
                        "skill_logo": self.skill_logo,
                        "length": 0,
                        "title": "SkyStream",
                        "author": "SkyStream",
                        "album": "SkyStream"
                    }]
            else:
                # gui only results
                results = [
                    {
                        # video match
                        "match_confidence": min(100, score),
                        "media_type": CPSMatchType.NEWS,
                        "uri": self.url,
                        "playback": CPSPlayback.GUI,
                        "image": self.default_image,
                        "bg_image": self.default_bg,
                        "skill_icon": self.skill_icon,
                        "skill_logo": self.skill_logo,
                        "length": 0,
                        "title": "SkyStream",
                        "author": "SkyStream",
                        "album": "SkyStream"
                    }]
            return results
        return []


def create_skill():
    return SkyStream()
