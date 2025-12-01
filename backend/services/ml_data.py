
import math
import hashlib
from typing import List, Dict, Set, Optional, Any, Tuple
from dataclasses import dataclass, field


class BloomFilter:
    """
    Probabilistic data structure for fast set membership testing.
    False positive rate is configurable.
    """
    def __init__(self, items_count: int, fp_prob: float):
        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.byte_size = (self.size + 7) // 8
        self.bit_array = bytearray(self.byte_size)

    def _hash(self, item: str, seed: int) -> int:
        """Double hashing using sha256"""
        h = hashlib.sha256(item.encode('utf-8')).digest()
        h1 = int.from_bytes(h[:16], 'big')
        h2 = int.from_bytes(h[16:], 'big')
        return (h1 + seed * h2) % self.size

    def add(self, item: str):
        for i in range(self.hash_count):
            digest = self._hash(item, i)
            byte_index = digest // 8
            bit_index = digest % 8
            self.bit_array[byte_index] |= (1 << bit_index)

    def check(self, item: str) -> bool:
        for i in range(self.hash_count):
            digest = self._hash(item, i)
            byte_index = digest // 8
            bit_index = digest % 8
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True

    @classmethod
    def get_size(cls, n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return int(k)

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word = False
        self.category: Optional[str] = None
        self.weight: float = 0.0

class Trie:
    """
    Prefix tree for efficient keyword matching and categorization.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, category: str, weight: float = 1.0):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.category = category
        node.weight = weight

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def search_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Finds all occurrences of keywords in text.
        """
        matches = []
        words = text.split()
        for word in words:
            node = self.root
            for char in word:
                if char in node.children:
                    node = node.children[char]
                    if node.is_end_of_word:
                        matches.append({
                            'word': word,
                            'category': node.category,
                            'weight': node.weight
                        })
                else:
                    break
        return matches


class DomainDatabase:
    """
    Manages millions of blocked domains using Bloom Filters.
    """
    def __init__(self):
        self.filter = BloomFilter(1000000, 0.001)
        self._populate()

    def _populate(self):
        domains = [
            "pornhub.com", "xvideos.com", "xnxx.com", "xhamster.com", "redtube.com",
            "youporn.com", "brazzers.com", "realitykings.com", "bangbros.com",
            "naughtyamerica.com", "chaturbate.com", "myfreecams.com", "livejasmin.com",
            "adultfriendfinder.com", "ashleymadison.com", "onlyfans.com", "fansly.com",
            "justfor.fans", "admireme.vip", "fancentro.com", "manyvids.com",
            "clips4sale.com", "iwantclips.com", "loyalfans.com", "pocketstars.com",
            "avgle.com", "jable.tv", "missav.com", "spankbang.com", "eporner.com",
            "hqporner.com", "beeg.com", "yourporn.sexy", "porn.com", "tube8.com",
            "keezmovies.com", "spankwire.com", "xtube.com", "cliphunter.com",
            "extremetube.com", "sunporno.com", "yuvutu.com", "shufuni.com",
            "fux.com", "drtuber.com", "pornerbros.com", "pornhoarder.com",
            "pornrabbit.com", "porntrex.com", "thumbzilla.com", "tnaflix.com",
            "tubegalore.com", "vporn.com", "whoreshub.com", "wankoz.com",
            "zporn.com", "4tube.com", "alotporn.com", "anysex.com", "bellesa.co",
            "bravotube.net", "buver.com", "cineb.net", "cumlouder.com", "daftsex.com",
            "dansmovies.com", "definebabe.com", "deviantclip.com", "dpporn.com",
            "dump.xxx", "e-hentai.org", "nhentai.net", "hanime.tv", "gelbooru.com",
            "rule34.xxx", "sankakucomplex.com", "konachan.com", "yandere.re",
            "danbooru.donmai.us", "pixiv.net", "dmm.co.jp", "fanza.co.jp",
            "javbus.com", "javlibrary.com", "javdb.com", "jav321.com",
            "javguru.com", "javmost.com", "javthe.com", "javdoe.com",
            "javcl.com", "javseen.tv", "javbangers.com", "javhihi.com",
            "adult.com", "adultwork.com", "adultsearch.com", "adultdvdtalk.com",
            "adultempire.com", "adultism.com", "adultforce.com", "adultgalls.com",
            "adulthost.com", "adultlook.com", "adultmatchmaker.com", "adultsitetoplist.com",
            "adultswim.com", "adulttime.com", "adultvideo.com", "adultworld.com",
            "alotporn.com", "alphaporno.com", "amateureuro.com", "amateurindex.com",
            "amateurmatch.com", "amateurpages.com", "amateurpint.com", "amateurporn.net",
            "amateursex.com", "amateurstraight.com", "amateurvoyeur.com", "amateurzone.com",
            "anal-angel.com", "anal-beauty.com", "anal-center.com", "anal-city.com",
            "anal-delight.com", "anal-factory.com", "anal-fun.com", "anal-girls.com",
            "anal-heaven.com", "anal-home.com", "anal-house.com", "anal-hub.com",
            "anal-king.com", "anal-land.com", "anal-life.com", "anal-love.com",
            "anal-master.com", "anal-party.com", "anal-place.com", "anal-planet.com",
            "anal-pleasure.com", "anal-point.com", "anal-porn.com", "anal-power.com",
            "anal-pride.com", "anal-princess.com", "anal-queen.com", "anal-quest.com",
            "anal-room.com", "anal-rose.com", "anal-sex.com", "anal-site.com",
            "anal-sky.com", "anal-star.com", "anal-station.com", "anal-story.com",
            "anal-street.com", "anal-studio.com", "anal-style.com", "anal-sun.com",
            "anal-super.com", "anal-sweet.com", "anal-teen.com", "anal-time.com",
            "anal-top.com", "anal-town.com", "anal-toy.com", "anal-tube.com",
            "anal-tv.com", "anal-universe.com", "anal-video.com", "anal-view.com",
            "anal-village.com", "anal-vision.com", "anal-world.com", "anal-zone.com",
            "anysex.com", "anybunny.com", "anyporn.com", "anyxxx.com", "areaporn.com",
            "asian-angel.com", "asian-beauty.com", "asian-center.com", "asian-city.com",
            "asian-club.com", "asian-dolls.com", "asian-dream.com", "asian-fantasy.com",
            "asian-flow.com", "asian-flower.com", "asian-fun.com", "asian-gallery.com",
            "asian-garden.com", "asian-gate.com", "asian-girls.com", "asian-glory.com",
            "asian-gold.com", "asian-heart.com", "asian-heat.com", "asian-heaven.com",
            "asian-home.com", "asian-honey.com", "asian-hot.com", "asian-house.com",
            "asian-hub.com", "asian-idol.com", "asian-island.com", "asian-jewel.com",
            "asian-joy.com", "asian-kiss.com", "asian-lady.com", "asian-land.com",
            "asian-life.com", "asian-love.com", "asian-lust.com", "asian-magic.com",
            "asian-master.com", "asian-mate.com", "asian-model.com", "asian-moon.com",
            "asian-night.com", "asian-nude.com", "asian-ocean.com", "asian-palace.com",
            "asian-paradise.com", "asian-party.com", "asian-pearl.com", "asian-place.com",
            "asian-planet.com", "asian-pleasure.com", "asian-point.com", "asian-porn.com",
            "asian-power.com", "asian-pride.com", "asian-princess.com", "asian-queen.com",
            "asian-quest.com", "asian-rain.com", "asian-rose.com", "asian-secret.com",
            "asian-sex.com", "asian-shine.com", "asian-silk.com", "asian-site.com",
            "asian-sky.com", "asian-smile.com", "asian-soul.com", "asian-spice.com",
            "asian-star.com", "asian-story.com", "asian-street.com", "asian-style.com",
            "asian-sugar.com", "asian-sun.com", "asian-sweet.com", "asian-taste.com",
            "asian-teen.com", "asian-time.com", "asian-top.com", "asian-touch.com",
            "asian-town.com", "asian-toy.com", "asian-tube.com", "asian-tv.com",
            "asian-venus.com", "asian-video.com", "asian-view.com", "asian-village.com",
            "asian-vision.com", "asian-voice.com", "asian-way.com", "asian-web.com",
            "asian-world.com", "asian-xxx.com", "asian-zone.com", "ass-angel.com",
            "ass-beauty.com", "ass-center.com", "ass-city.com", "ass-club.com",
            "ass-delight.com", "ass-dream.com", "ass-factory.com", "ass-fantasy.com",
            "ass-fun.com", "ass-gallery.com", "ass-garden.com", "ass-gate.com",
            "ass-girls.com", "ass-glory.com", "ass-gold.com", "ass-heaven.com",
            "ass-home.com", "ass-house.com", "ass-hub.com", "ass-hunter.com",
            "ass-island.com", "ass-joy.com", "ass-king.com", "ass-land.com",
            "ass-life.com", "ass-love.com", "ass-lust.com", "ass-magic.com",
            "ass-master.com", "ass-model.com", "ass-night.com", "ass-ocean.com",
            "ass-palace.com", "ass-paradise.com", "ass-party.com", "ass-place.com",
            "ass-planet.com", "ass-pleasure.com", "ass-point.com", "ass-porn.com",
            "ass-power.com", "ass-pride.com", "ass-princess.com", "ass-queen.com",
            "ass-quest.com", "ass-room.com", "ass-rose.com", "ass-sex.com",
            "ass-site.com", "ass-sky.com", "ass-star.com", "ass-station.com",
            "ass-story.com", "ass-street.com", "ass-studio.com", "ass-style.com",
            "ass-sun.com", "ass-super.com", "ass-sweet.com", "ass-teen.com",
            "ass-time.com", "ass-top.com", "ass-town.com", "ass-toy.com",
            "ass-tube.com", "ass-tv.com", "ass-universe.com", "ass-video.com",
            "ass-view.com", "ass-village.com", "ass-vision.com", "ass-world.com",
            "ass-zone.com", "asshole.com", "assparade.com", "asspoint.com",
            "babe-angel.com", "babe-beauty.com", "babe-center.com", "babe-city.com",
            "babe-club.com", "babe-delight.com", "babe-dream.com", "babe-factory.com",
            "babe-fantasy.com", "babe-fun.com", "babe-gallery.com", "babe-garden.com",
            "babe-gate.com", "babe-girls.com", "babe-glory.com", "babe-gold.com",
            "babe-heaven.com", "babe-home.com", "babe-house.com", "babe-hub.com",
            "babe-hunter.com", "babe-island.com", "babe-joy.com", "babe-king.com",
            "babe-land.com", "babe-life.com", "babe-love.com", "babe-lust.com",
            "babe-magic.com", "babe-master.com", "babe-model.com", "babe-night.com",
            "babe-ocean.com", "babe-palace.com", "babe-paradise.com", "babe-party.com",
            "babe-place.com", "babe-planet.com", "babe-pleasure.com", "babe-point.com",
            "babe-porn.com", "babe-power.com", "babe-pride.com", "babe-princess.com",
            "babe-queen.com", "babe-quest.com", "babe-room.com", "babe-rose.com",
            "babe-sex.com", "babe-site.com", "babe-sky.com", "babe-star.com",
            "babe-station.com", "babe-story.com", "babe-street.com", "babe-studio.com",
            "babe-style.com", "babe-sun.com", "babe-super.com", "babe-sweet.com",
            "babe-teen.com", "babe-time.com", "babe-top.com", "babe-town.com",
            "babe-toy.com", "babe-tube.com", "babe-tv.com", "babe-universe.com",
            "babe-video.com", "babe-view.com", "babe-village.com", "babe-vision.com",
            "babe-world.com", "babe-zone.com", "babes.com", "babes.net",
            "babes.tv", "babesandstars.com", "babesnetwork.com", "babesporn.com",
            "babessex.com", "babestube.com", "babesvideo.com", "babesworld.com",
            "baby-angel.com", "baby-beauty.com", "baby-center.com", "baby-city.com",
            "baby-club.com", "baby-delight.com", "baby-dream.com", "baby-factory.com",
            "baby-fantasy.com", "baby-fun.com", "baby-gallery.com", "baby-garden.com",
            "baby-gate.com", "baby-girls.com", "baby-glory.com", "baby-gold.com",
            "baby-heaven.com", "baby-home.com", "baby-house.com", "baby-hub.com",
            "baby-hunter.com", "baby-island.com", "baby-joy.com", "baby-king.com",
            "baby-land.com", "baby-life.com", "baby-love.com", "baby-lust.com",
            "baby-magic.com", "baby-master.com", "baby-model.com", "baby-night.com",
            "baby-ocean.com", "baby-palace.com", "baby-paradise.com", "baby-party.com",
            "baby-place.com", "baby-planet.com", "baby-pleasure.com", "baby-point.com",
            "baby-porn.com", "baby-power.com", "baby-pride.com", "baby-princess.com",
            "baby-queen.com", "baby-quest.com", "baby-room.com", "baby-rose.com",
            "baby-sex.com", "baby-site.com", "baby-sky.com", "baby-star.com",
            "baby-station.com", "baby-story.com", "baby-street.com", "baby-studio.com",
            "baby-style.com", "baby-sun.com", "baby-super.com", "baby-sweet.com",
            "baby-teen.com", "baby-time.com", "baby-top.com", "baby-town.com",
            "baby-toy.com", "baby-tube.com", "baby-tv.com", "baby-universe.com",
            "baby-video.com", "baby-view.com", "baby-village.com", "baby-vision.com",
            "baby-world.com", "baby-zone.com", "babycakes.com", "babycenter.com",
            "babydoll.com", "babygirl.com", "babylove.com", "babyphat.com",
            "babysitter.com", "backroomfacials.com", "backroommilf.com", "backroomporn.com",
            "bad-angel.com", "bad-beauty.com", "bad-center.com", "bad-city.com",
            "bad-club.com", "bad-delight.com", "bad-dream.com", "bad-factory.com",
            "bad-fantasy.com", "bad-fun.com", "bad-gallery.com", "bad-garden.com",
            "bad-gate.com", "bad-girls.com", "bad-glory.com", "bad-gold.com",
            "bad-heaven.com", "bad-home.com", "bad-house.com", "bad-hub.com",
            "bad-hunter.com", "bad-island.com", "bad-joy.com", "bad-king.com",
            "bad-land.com", "bad-life.com", "bad-love.com", "bad-lust.com",
            "bad-magic.com", "bad-master.com", "bad-model.com", "bad-night.com",
            "bad-ocean.com", "bad-palace.com", "bad-paradise.com", "bad-party.com",
            "bad-place.com", "bad-planet.com", "bad-pleasure.com", "bad-point.com",
            "bad-porn.com", "bad-power.com", "bad-pride.com", "bad-princess.com",
            "bad-queen.com", "bad-quest.com", "bad-room.com", "bad-rose.com",
            "bad-sex.com", "bad-site.com", "bad-sky.com", "bad-star.com",
            "bad-station.com", "bad-story.com", "bad-street.com", "bad-studio.com",
            "bad-style.com", "bad-sun.com", "bad-super.com", "bad-sweet.com",
            "bad-teen.com", "bad-time.com", "bad-top.com", "bad-town.com",
            "bad-toy.com", "bad-tube.com", "bad-tv.com", "bad-universe.com",
            "bad-video.com", "bad-view.com", "bad-village.com", "bad-vision.com",
            "bad-world.com", "bad-zone.com", "badjojo.com", "badpuppy.com",
            "banged.com", "bangbros.com", "bangbus.com", "banggonewild.com",
            "bangland.com", "bangyoulater.com", "bareback.com", "barelylegal.com",
            "bbw-angel.com", "bbw-beauty.com", "bbw-center.com", "bbw-city.com",
            "bbw-club.com", "bbw-delight.com", "bbw-dream.com", "bbw-factory.com",
            "bbw-fantasy.com", "bbw-fun.com", "bbw-gallery.com", "bbw-garden.com",
            "bbw-gate.com", "bbw-girls.com", "bbw-glory.com", "bbw-gold.com",
            "bbw-heaven.com", "bbw-home.com", "bbw-house.com", "bbw-hub.com",
            "bbw-hunter.com", "bbw-island.com", "bbw-joy.com", "bbw-king.com",
            "bbw-land.com", "bbw-life.com", "bbw-love.com", "bbw-lust.com",
            "bbw-magic.com", "bbw-master.com", "bbw-model.com", "bbw-night.com",
            "bbw-ocean.com", "bbw-palace.com", "bbw-paradise.com", "bbw-party.com",
            "bbw-place.com", "bbw-planet.com", "bbw-pleasure.com", "bbw-point.com",
            "bbw-porn.com", "bbw-power.com", "bbw-pride.com", "bbw-princess.com",
            "bbw-queen.com", "bbw-quest.com", "bbw-room.com", "bbw-rose.com",
            "bbw-sex.com", "bbw-site.com", "bbw-sky.com", "bbw-star.com",
            "bbw-station.com", "bbw-story.com", "bbw-street.com", "bbw-studio.com",
            "bbw-style.com", "bbw-sun.com", "bbw-super.com", "bbw-sweet.com",
            "bbw-teen.com", "bbw-time.com", "bbw-top.com", "bbw-town.com",
            "bbw-toy.com", "bbw-tube.com", "bbw-tv.com", "bbw-universe.com",
            "bbw-video.com", "bbw-view.com", "bbw-village.com", "bbw-vision.com",
            "bbw-world.com", "bbw-zone.com", "bbwchan.com", "bbwhunter.com",
            "bbwlovers.com", "bbwmagazine.com", "bbwmatch.com", "bbwporn.com",
            "bbwsex.com", "bbwtube.com", "bbwvideos.com", "bbwworld.com",
            "bdsm-angel.com", "bdsm-beauty.com", "bdsm-center.com", "bdsm-city.com",
            "bdsm-club.com", "bdsm-delight.com", "bdsm-dream.com", "bdsm-factory.com",
            "bdsm-fantasy.com", "bdsm-fun.com", "bdsm-gallery.com", "bdsm-garden.com",
            "bdsm-gate.com", "bdsm-girls.com", "bdsm-glory.com", "bdsm-gold.com",
            "bdsm-heaven.com", "bdsm-home.com", "bdsm-house.com", "bdsm-hub.com",
            "bdsm-hunter.com", "bdsm-island.com", "bdsm-joy.com", "bdsm-king.com",
            "bdsm-land.com", "bdsm-life.com", "bdsm-love.com", "bdsm-lust.com",
            "bdsm-magic.com", "bdsm-master.com", "bdsm-model.com", "bdsm-night.com",
            "bdsm-ocean.com", "bdsm-palace.com", "bdsm-paradise.com", "bdsm-party.com",
            "bdsm-place.com", "bdsm-planet.com", "bdsm-pleasure.com", "bdsm-point.com",
            "bdsm-porn.com", "bdsm-power.com", "bdsm-pride.com", "bdsm-princess.com",
            "bdsm-queen.com", "bdsm-quest.com", "bdsm-room.com", "bdsm-rose.com",
            "bdsm-sex.com", "bdsm-site.com", "bdsm-sky.com", "bdsm-star.com",
            "bdsm-station.com", "bdsm-story.com", "bdsm-street.com", "bdsm-studio.com",
            "bdsm-style.com", "bdsm-sun.com", "bdsm-super.com", "bdsm-sweet.com",
            "bdsm-teen.com", "bdsm-time.com", "bdsm-top.com", "bdsm-town.com",
            "bdsm-toy.com", "bdsm-tube.com", "bdsm-tv.com", "bdsm-universe.com",
            "bdsm-video.com", "bdsm-view.com", "bdsm-village.com", "bdsm-vision.com",
            "bdsm-world.com", "bdsm-zone.com", "beeg.com", "beeg.net",
            "beeg.tv", "beegporn.com", "beegsex.com", "beegtube.com",
            "beegvideo.com", "beegworld.com", "behindthescenes.com", "best-angel.com",
            "best-beauty.com", "best-center.com", "best-city.com", "best-club.com",
            "best-delight.com", "best-dream.com", "best-factory.com", "best-fantasy.com",
            "best-fun.com", "best-gallery.com", "best-garden.com", "best-gate.com",
            "best-girls.com", "best-glory.com", "best-gold.com", "best-heaven.com",
            "best-home.com", "best-house.com", "best-hub.com", "best-hunter.com",
            "best-island.com", "best-joy.com", "best-king.com", "best-land.com",
            "best-life.com", "best-love.com", "best-lust.com", "best-magic.com",
            "best-master.com", "best-model.com", "best-night.com", "best-ocean.com",
            "best-palace.com", "best-paradise.com", "best-party.com", "best-place.com",
            "best-planet.com", "best-pleasure.com", "best-point.com", "best-porn.com",
            "best-power.com", "best-pride.com", "best-princess.com", "best-queen.com",
            "best-quest.com", "best-room.com", "best-rose.com", "best-sex.com",
            "best-site.com", "best-sky.com", "best-star.com", "best-station.com",
            "best-story.com", "best-street.com", "best-studio.com", "best-style.com",
            "best-sun.com", "best-super.com", "best-sweet.com", "best-teen.com",
            "best-time.com", "best-top.com", "best-town.com", "best-toy.com",
            "best-tube.com", "best-tv.com", "best-universe.com", "best-video.com",
            "best-view.com", "best-village.com", "best-vision.com", "best-world.com",
            "best-zone.com", "bestiality.com", "bestialityporn.com", "bestialitysex.com",
            "bestialitytube.com", "bestialityvideo.com", "bestialityworld.com", "big-angel.com",
            "big-beauty.com", "big-center.com", "big-city.com", "big-club.com",
            "big-delight.com", "big-dream.com", "big-factory.com", "big-fantasy.com",
            "big-fun.com", "big-gallery.com", "big-garden.com", "big-gate.com",
            "big-girls.com", "big-glory.com", "big-gold.com", "big-heaven.com",
            "big-home.com", "big-house.com", "big-hub.com", "big-hunter.com",
            "big-island.com", "big-joy.com", "big-king.com", "big-land.com",
            "big-life.com", "big-love.com", "big-lust.com", "big-magic.com",
            "big-master.com", "big-model.com", "big-night.com", "big-ocean.com",
            "big-palace.com", "big-paradise.com", "big-party.com", "big-place.com",
            "big-planet.com", "big-pleasure.com", "big-point.com", "big-porn.com",
            "big-power.com", "big-pride.com", "big-princess.com", "big-queen.com",
            "big-quest.com", "big-room.com", "big-rose.com", "big-sex.com",
            "big-site.com", "big-sky.com", "big-star.com", "big-station.com",
            "big-story.com", "big-street.com", "big-studio.com", "big-style.com",
            "big-sun.com", "big-super.com", "big-sweet.com", "big-teen.com",
            "big-time.com", "big-top.com", "big-town.com", "big-toy.com",
            "big-tube.com", "big-tv.com", "big-universe.com", "big-video.com",
            "big-view.com", "big-village.com", "big-vision.com", "big-world.com",
            "big-zone.com", "bigass.com", "bigassporn.com", "bigasssex.com",
            "bigasstube.com", "bigassvideo.com", "bigassworld.com", "bigboobs.com",
            "bigboobsporn.com", "bigboobssex.com", "bigboobstube.com", "bigboobsvideo.com",
            "bigboobsworld.com", "bigcock.com", "bigcockporn.com", "bigcocksex.com",
            "bigcocktube.com", "bigcockvideo.com", "bigcockworld.com", "bigdick.com",
            "bigdickporn.com", "bigdicksex.com", "bigdicktube.com", "bigdickvideo.com",
            "bigdickworld.com", "bigtits.com", "bigtitsporn.com", "bigtitssex.com",
            "bigtitstube.com", "bigtitsvideo.com", "bigtitsworld.com", "bikini-angel.com",
            "bikini-beauty.com", "bikini-center.com", "bikini-city.com", "bikini-club.com",
            "bikini-delight.com", "bikini-dream.com", "bikini-factory.com", "bikini-fantasy.com",
            "bikini-fun.com", "bikini-gallery.com", "bikini-garden.com", "bikini-gate.com",
            "bikini-girls.com", "bikini-glory.com", "bikini-gold.com", "bikini-heaven.com",
            "bikini-home.com", "bikini-house.com", "bikini-hub.com", "bikini-hunter.com",
            "bikini-island.com", "bikini-joy.com", "bikini-king.com", "bikini-land.com",
            "bikini-life.com", "bikini-love.com", "bikini-lust.com", "bikini-magic.com",
            "bikini-master.com", "bikini-model.com", "bikini-night.com", "bikini-ocean.com",
            "bikini-palace.com", "bikini-paradise.com", "bikini-party.com", "bikini-place.com",
            "bikini-planet.com", "bikini-pleasure.com", "bikini-point.com", "bikini-porn.com",
            "bikini-power.com", "bikini-pride.com", "bikini-princess.com", "bikini-queen.com",
            "bikini-quest.com", "bikini-room.com", "bikini-rose.com", "bikini-sex.com",
            "bikini-site.com", "bikini-sky.com", "bikini-star.com", "bikini-station.com",
            "bikini-story.com", "bikini-street.com", "bikini-studio.com", "bikini-style.com",
            "bikini-sun.com", "bikini-super.com", "bikini-sweet.com", "bikini-teen.com",
            "bikini-time.com", "bikini-top.com", "bikini-town.com", "bikini-toy.com",
            "bikini-tube.com", "bikini-tv.com", "bikini-universe.com", "bikini-video.com",
            "bikini-view.com", "bikini-village.com", "bikini-vision.com", "bikini-world.com",
            "bikini-zone.com", "bikiniporn.com", "bikinisex.com", "bikinitube.com",
            "bikinivideo.com", "bikiniworld.com", "bisexual.com", "bisexualporn.com",
            "bisexualsex.com", "bisexualtube.com", "bisexualvideo.com", "bisexualworld.com",
            "black-angel.com", "black-beauty.com", "black-center.com", "black-city.com",
            "black-club.com", "black-delight.com", "black-dream.com", "black-factory.com",
            "black-fantasy.com", "black-fun.com", "black-gallery.com", "black-garden.com",
            "black-gate.com", "black-girls.com", "black-glory.com", "black-gold.com",
            "black-heaven.com", "black-home.com", "black-house.com", "black-hub.com",
            "black-hunter.com", "black-island.com", "black-joy.com", "black-king.com",
            "black-land.com", "black-life.com", "black-love.com", "black-lust.com",
            "black-magic.com", "black-master.com", "black-model.com", "black-night.com",
            "black-ocean.com", "black-palace.com", "black-paradise.com", "black-party.com",
            "black-place.com", "black-planet.com", "black-pleasure.com", "black-point.com",
            "black-porn.com", "black-power.com", "black-pride.com", "black-princess.com",
            "black-queen.com", "black-quest.com", "black-room.com", "black-rose.com",
            "black-sex.com", "black-site.com", "black-sky.com", "black-star.com",
            "black-station.com", "black-story.com", "black-street.com", "black-studio.com",
            "black-style.com", "black-sun.com", "black-super.com", "black-sweet.com",
            "black-teen.com", "black-time.com", "black-top.com", "black-town.com",
            "black-toy.com", "black-tube.com", "black-tv.com", "black-universe.com",
            "black-video.com", "black-view.com", "black-village.com", "black-vision.com",
            "black-world.com", "black-zone.com", "blackcock.com", "blackcockporn.com",
            "blackcocksex.com", "blackcocktube.com", "blackcockvideo.com", "blackcockworld.com",
            "blacked.com", "blackedraw.com", "blackgfs.com", "blackisbetter.com",
            "blacksonblondes.com", "blacktgirls.com", "blackzilla.com", "blonde-angel.com",
            "blonde-beauty.com", "blonde-center.com", "blonde-city.com", "blonde-club.com",
            "blonde-delight.com", "blonde-dream.com", "blonde-factory.com", "blonde-fantasy.com",
            "blonde-fun.com", "blonde-gallery.com", "blonde-garden.com", "blonde-gate.com",
            "blonde-girls.com", "blonde-glory.com", "blonde-gold.com", "blonde-heaven.com",
            "blonde-home.com", "blonde-house.com", "blonde-hub.com", "blonde-hunter.com",
            "blonde-island.com", "blonde-joy.com", "blonde-king.com", "blonde-land.com",
            "blonde-life.com", "blonde-love.com", "blonde-lust.com", "blonde-magic.com",
            "blonde-master.com", "blonde-model.com", "blonde-night.com", "blonde-ocean.com",
            "blonde-palace.com", "blonde-paradise.com", "blonde-party.com", "blonde-place.com",
            "blonde-planet.com", "blonde-pleasure.com", "blonde-point.com", "blonde-porn.com",
            "blonde-power.com", "blonde-pride.com", "blonde-princess.com", "blonde-queen.com",
            "blonde-quest.com", "blonde-room.com", "blonde-rose.com", "blonde-sex.com",
            "blonde-site.com", "blonde-sky.com", "blonde-star.com", "blonde-station.com",
            "blonde-story.com", "blonde-street.com", "blonde-studio.com", "blonde-style.com",
            "blonde-sun.com", "blonde-super.com", "blonde-sweet.com", "blonde-teen.com",
            "blonde-time.com", "blonde-top.com", "blonde-town.com", "blonde-toy.com",
            "blonde-tube.com", "blonde-tv.com", "blonde-universe.com", "blonde-video.com",
            "blonde-view.com", "blonde-village.com", "blonde-vision.com", "blonde-world.com",
            "blonde-zone.com", "blondeporn.com", "blondesex.com", "blondetube.com",
            "blondevideo.com", "blondeworld.com", "blowjob-angel.com", "blowjob-beauty.com",
            "blowjob-center.com", "blowjob-city.com", "blowjob-club.com", "blowjob-delight.com",
            "blowjob-dream.com", "blowjob-factory.com", "blowjob-fantasy.com", "blowjob-fun.com",
            "blowjob-gallery.com", "blowjob-garden.com", "blowjob-gate.com", "blowjob-girls.com",
            "blowjob-glory.com", "blowjob-gold.com", "blowjob-heaven.com", "blowjob-home.com",
            "blowjob-house.com", "blowjob-hub.com", "blowjob-hunter.com", "blowjob-island.com",
            "blowjob-joy.com", "blowjob-king.com", "blowjob-land.com", "blowjob-life.com",
            "blowjob-love.com", "blowjob-lust.com", "blowjob-magic.com", "blowjob-master.com",
            "blowjob-model.com", "blowjob-night.com", "blowjob-ocean.com", "blowjob-palace.com",
            "blowjob-paradise.com", "blowjob-party.com", "blowjob-place.com", "blowjob-planet.com",
            "blowjob-pleasure.com", "blowjob-point.com", "blowjob-porn.com", "blowjob-power.com",
            "blowjob-pride.com", "blowjob-princess.com", "blowjob-queen.com", "blowjob-quest.com",
            "blowjob-room.com", "blowjob-rose.com", "blowjob-sex.com", "blowjob-site.com",
            "blowjob-sky.com", "blowjob-star.com", "blowjob-station.com", "blowjob-story.com",
            "blowjob-street.com", "blowjob-studio.com", "blowjob-style.com", "blowjob-sun.com",
            "blowjob-super.com", "blowjob-sweet.com", "blowjob-teen.com", "blowjob-time.com",
            "blowjob-top.com", "blowjob-town.com", "blowjob-toy.com", "blowjob-tube.com",
            "blowjob-tv.com", "blowjob-universe.com", "blowjob-video.com", "blowjob-view.com",
            "blowjob-village.com", "blowjob-vision.com", "blowjob-world.com", "blowjob-zone.com",
            "blowjobporn.com", "blowjobsex.com", "blowjobtube.com", "blowjobvideo.com",
            "blowjobworld.com", "bondage-angel.com", "bondage-beauty.com", "bondage-center.com",
            "bondage-city.com", "bondage-club.com", "bondage-delight.com", "bondage-dream.com",
            "bondage-factory.com", "bondage-fantasy.com", "bondage-fun.com", "bondage-gallery.com",
            "bondage-garden.com", "bondage-gate.com", "bondage-girls.com", "bondage-glory.com",
            "bondage-gold.com", "bondage-heaven.com", "bondage-home.com", "bondage-house.com",
            "bondage-hub.com", "bondage-hunter.com", "bondage-island.com", "bondage-joy.com",
            "bondage-king.com", "bondage-land.com", "bondage-life.com", "bondage-love.com",
            "bondage-lust.com", "bondage-magic.com", "bondage-master.com", "bondage-model.com",
            "bondage-night.com", "bondage-ocean.com", "bondage-palace.com", "bondage-paradise.com",
            "bondage-party.com", "bondage-place.com", "bondage-planet.com", "bondage-pleasure.com",
            "bondage-point.com", "bondage-porn.com", "bondage-power.com", "bondage-pride.com",
            "bondage-princess.com", "bondage-queen.com", "bondage-quest.com", "bondage-room.com",
            "bondage-rose.com", "bondage-sex.com", "bondage-site.com", "bondage-sky.com",
            "bondage-star.com", "bondage-station.com", "bondage-story.com", "bondage-street.com",
            "bondage-studio.com", "bondage-style.com", "bondage-sun.com", "bondage-super.com",
            "bondage-sweet.com", "bondage-teen.com", "bondage-time.com", "bondage-top.com",
            "bondage-town.com", "bondage-toy.com", "bondage-tube.com", "bondage-tv.com",
            "bondage-universe.com", "bondage-video.com", "bondage-view.com", "bondage-village.com",
            "bondage-vision.com", "bondage-world.com", "bondage-zone.com", "bondageporn.com",
            "bondagesex.com", "bondagetube.com", "bondagevideo.com", "bondageworld.com",
            "boobs-angel.com", "boobs-beauty.com", "boobs-center.com", "boobs-city.com",
            "boobs-club.com", "boobs-delight.com", "boobs-dream.com", "boobs-factory.com",
            "boobs-fantasy.com", "boobs-fun.com", "boobs-gallery.com", "boobs-garden.com",
            "boobs-gate.com", "boobs-girls.com", "boobs-glory.com", "boobs-gold.com",
            "boobs-heaven.com", "boobs-home.com", "boobs-house.com", "boobs-hub.com",
            "boobs-hunter.com", "boobs-island.com", "boobs-joy.com", "boobs-king.com",
            "boobs-land.com", "boobs-life.com", "boobs-love.com", "boobs-lust.com",
            "boobs-magic.com", "boobs-master.com", "boobs-model.com", "boobs-night.com",
            "boobs-ocean.com", "boobs-palace.com", "boobs-paradise.com", "boobs-party.com",
            "boobs-place.com", "boobs-planet.com", "boobs-pleasure.com", "boobs-point.com",
            "boobs-porn.com", "boobs-power.com", "boobs-pride.com", "boobs-princess.com",
            "boobs-queen.com", "boobs-quest.com", "boobs-room.com", "boobs-rose.com",
            "boobs-sex.com", "boobs-site.com", "boobs-sky.com", "boobs-star.com",
            "boobs-station.com", "boobs-story.com", "boobs-street.com", "boobs-studio.com",
            "boobs-style.com", "boobs-sun.com", "boobs-super.com", "boobs-sweet.com",
            "boobs-teen.com", "boobs-time.com", "boobs-top.com", "boobs-town.com",
            "boobs-toy.com", "boobs-tube.com", "boobs-tv.com", "boobs-universe.com",
            "boobs-video.com", "boobs-view.com", "boobs-village.com", "boobs-vision.com",
            "boobs-world.com", "boobs-zone.com", "boobsporn.com", "boobssex.com",
            "boobstube.com", "boobsvideo.com", "boobsworld.com", "booty-angel.com",
            "booty-beauty.com", "booty-center.com", "booty-city.com", "booty-club.com",
            "booty-delight.com", "booty-dream.com", "booty-factory.com", "booty-fantasy.com",
            "booty-fun.com", "booty-gallery.com", "booty-garden.com", "booty-gate.com",
            "booty-girls.com", "booty-glory.com", "booty-gold.com", "booty-heaven.com",
            "booty-home.com", "booty-house.com", "booty-hub.com", "booty-hunter.com",
            "booty-island.com", "booty-joy.com", "booty-king.com", "booty-land.com",
            "booty-life.com", "booty-love.com", "booty-lust.com", "booty-magic.com",
            "booty-master.com", "booty-model.com", "booty-night.com", "booty-ocean.com",
            "booty-palace.com", "booty-paradise.com", "booty-party.com", "booty-place.com",
            "booty-planet.com", "booty-pleasure.com", "booty-point.com", "booty-porn.com",
            "booty-power.com", "booty-pride.com", "booty-princess.com", "booty-queen.com",
            "booty-quest.com", "booty-room.com", "booty-rose.com", "booty-sex.com",
            "booty-site.com", "booty-sky.com", "booty-star.com", "booty-station.com",
            "booty-story.com", "booty-street.com", "booty-studio.com", "booty-style.com",
            "booty-sun.com", "booty-super.com", "booty-sweet.com", "booty-teen.com",
            "booty-time.com", "booty-top.com", "booty-town.com", "booty-toy.com",
            "booty-tube.com", "booty-tv.com", "booty-universe.com", "booty-video.com",
            "booty-view.com", "booty-village.com", "booty-vision.com", "booty-world.com",
            "booty-zone.com", "bootyporn.com", "bootysex.com", "bootytube.com",
            "bootyvideo.com", "bootyworld.com", "brazzers.com", "brazzersnetwork.com",
            "brazzersporn.com", "brazzerssex.com", "brazzerstube.com", "brazzersvideo.com",
            "brazzersworld.com", "busty-angel.com", "busty-beauty.com", "busty-center.com",
            "busty-city.com", "busty-club.com", "busty-delight.com", "busty-dream.com",
            "busty-factory.com", "busty-fantasy.com", "busty-fun.com", "busty-gallery.com",
            "busty-garden.com", "busty-gate.com", "busty-girls.com", "busty-glory.com",
            "busty-gold.com", "busty-heaven.com", "busty-home.com", "busty-house.com",
            "busty-hub.com", "busty-hunter.com", "busty-island.com", "busty-joy.com",
            "busty-king.com", "busty-land.com", "busty-life.com", "busty-love.com",
            "busty-lust.com", "busty-magic.com", "busty-master.com", "busty-model.com",
            "busty-night.com", "busty-ocean.com", "busty-palace.com", "busty-paradise.com",
            "busty-party.com", "busty-place.com", "busty-planet.com", "busty-pleasure.com",
            "busty-point.com", "busty-porn.com", "busty-power.com", "busty-pride.com",
            "busty-princess.com", "busty-queen.com", "busty-quest.com", "busty-room.com",
            "busty-rose.com", "busty-sex.com", "busty-site.com", "busty-sky.com",
            "busty-star.com", "busty-station.com", "busty-story.com", "busty-street.com",
            "busty-studio.com", "busty-style.com", "busty-sun.com", "busty-super.com",
            "busty-sweet.com", "busty-teen.com", "busty-time.com", "busty-top.com",
            "busty-town.com", "busty-toy.com", "busty-tube.com", "busty-tv.com",
            "busty-universe.com", "busty-video.com", "busty-view.com", "busty-village.com",
            "busty-vision.com", "busty-world.com", "busty-zone.com", "bustyporn.com",
            "bustysex.com", "bustytube.com", "bustyvideo.com", "bustyworld.com",
            "butt-angel.com", "butt-beauty.com", "butt-center.com", "butt-city.com",
            "butt-club.com", "butt-delight.com", "butt-dream.com", "butt-factory.com",
            "butt-fantasy.com", "butt-fun.com", "butt-gallery.com", "butt-garden.com",
            "butt-gate.com", "butt-girls.com", "butt-glory.com", "butt-gold.com",
            "butt-heaven.com", "butt-home.com", "butt-house.com", "butt-hub.com",
            "butt-hunter.com", "butt-island.com", "butt-joy.com", "butt-king.com",
            "butt-land.com", "butt-life.com", "butt-love.com", "butt-lust.com",
            "butt-magic.com", "butt-master.com", "butt-model.com", "butt-night.com",
            "butt-ocean.com", "butt-palace.com", "butt-paradise.com", "butt-party.com",
            "butt-place.com", "butt-planet.com", "butt-pleasure.com", "butt-point.com",
            "butt-porn.com", "butt-power.com", "butt-pride.com", "butt-princess.com",
            "butt-queen.com", "butt-quest.com", "butt-room.com", "butt-rose.com",
            "butt-sex.com", "butt-site.com", "butt-sky.com", "butt-star.com",
            "butt-station.com", "butt-story.com", "butt-street.com", "butt-studio.com",
            "butt-style.com", "butt-sun.com", "butt-super.com", "butt-sweet.com",
            "butt-teen.com", "butt-time.com", "butt-top.com", "butt-town.com",
            "butt-toy.com", "butt-tube.com", "butt-tv.com", "butt-universe.com",
            "butt-video.com", "butt-view.com", "butt-village.com", "butt-vision.com",
            "butt-world.com", "butt-zone.com", "buttman.com", "buttporn.com",
            "buttsex.com", "butttube.com", "buttvideo.com", "buttworld.com",
        ]
        for d in domains:
            self.filter.add(d)
            self.filter.add(f"www.{d}")
            self.filter.add(f"m.{d}")
            for prefix in ["cdn.", "img.", "video.", "api."]:
                self.filter.add(f"{prefix}{d}")

    def is_blocked(self, domain: str) -> bool:
        return self.filter.check(domain)

class KeywordDatabase:
    """
    Manages multi-language keywords using Trie structures.
    """
    def __init__(self):
        self.trie = Trie()
        self._populate()

    def _populate(self):
        self._add_keywords("en", {
            "porn": 1.0, "sex": 0.8, "xxx": 1.0, "nude": 0.9, "naked": 0.8,
            "erotic": 0.7, "hentai": 1.0, "milf": 0.9, "teen": 0.5, "amateur": 0.4,
            "cam": 0.5, "live": 0.3, "chat": 0.2, "dating": 0.4, "escort": 0.9,
            "massage": 0.3, "strip": 0.8, "club": 0.3, "adult": 0.6, "18+": 1.0,
            "nsfw": 1.0, "dick": 0.9, "cock": 0.9, "pussy": 0.9, "vagina": 0.8,
            "boobs": 0.8, "tits": 0.8, "ass": 0.6, "anal": 0.9, "oral": 0.7,
            "blowjob": 1.0, "handjob": 0.9, "cum": 0.9, "sperm": 0.7, "orgasm": 0.8,
            "masturbate": 0.9, "wank": 0.8, "jerk": 0.6, "fap": 0.8, "squirt": 0.9,
            "bondage": 0.8, "bdsm": 0.9, "fetish": 0.7, "kink": 0.6, "slave": 0.5,
            "dom": 0.5, "sub": 0.5, "incest": 1.0, "taboo": 0.4, "rape": 1.0,
            "violence": 0.6, "gore": 0.9, "blood": 0.5, "kill": 0.6, "suicide": 1.0,
            "drugs": 0.8, "cocaine": 0.9, "heroin": 0.9, "meth": 0.9, "weed": 0.6
        })
        
        self._add_keywords("es", {
            "porno": 1.0, "sexo": 0.8, "desnuda": 0.9, "puta": 0.9, "culo": 0.7,
            "tetas": 0.8, "verga": 0.9, "pene": 0.8, "vagina": 0.8, "follar": 1.0,
            "chupar": 0.6, "mamada": 1.0, "paja": 0.8, "corrida": 0.7, "leche": 0.3,
            "anal": 0.9, "oral": 0.7, "orgia": 1.0, "trrio": 0.8, "swinger": 0.8
        })
        
        self._add_keywords("fr", {
            "porno": 1.0, "sexe": 0.8, "nue": 0.9, "pute": 0.9, "cul": 0.7,
            "seins": 0.8, "bite": 0.9, "chatte": 0.8, "baise": 1.0, "sucer": 0.7,
            "fellation": 1.0, "branlette": 0.9, "sperme": 0.7, "orgie": 1.0,
            "echangisme": 0.8, "bondage": 0.8, "domination": 0.6, "soumission": 0.6
        })
        
        self._add_keywords("de", {
            "porno": 1.0, "sex": 0.8, "nackt": 0.9, "hure": 0.9, "arsch": 0.7,
            "titten": 0.8, "schwanz": 0.9, "fotze": 0.9, "ficken": 1.0, "blasen": 0.6,
            "wichsen": 0.9, "sperma": 0.7, "orgasmus": 0.8, "gangbang": 1.0,
            "swinger": 0.8, "fetisch": 0.7, "sklave": 0.5, "herr": 0.2
        })
        
        self._add_keywords("ru", {
            "порно": 1.0, "секс": 0.8, "голая": 0.9, "шлюха": 0.9, "жопа": 0.7,
            "сиськи": 0.8, "хуй": 1.0, "пизда": 1.0, "ебать": 1.0, "сосать": 0.7,
            "минет": 1.0, "дрочить": 0.9, "сперма": 0.7, "оргазм": 0.8, "групповуха": 1.0,
            "инцест": 1.0, "изнасилование": 1.0, "бдсм": 0.9, "фетиш": 0.7
        })
        
        self._add_keywords("jp", {
            "ポルノ": 1.0, "セックス": 0.8, "ヌード": 0.9, "エロ": 0.8, "ヘンタイ": 1.0,
            "巨乳": 0.8, "貧乳": 0.6, "中出し": 1.0, "フェラ": 1.0, "手コキ": 0.9,
            "パイズリ": 0.9, "アナル": 0.9, "オナニー": 0.9, "痴漢": 1.0, "盗撮": 1.0,
            "近親相姦": 1.0, "レイプ": 1.0, "調教": 0.8, "奴隷": 0.6, "触手": 0.8
        })
        
        self._add_keywords("cn", {
            "色情": 1.0, "性爱": 0.8, "裸体": 0.9, "妓女": 0.9, "乳房": 0.7,
            "阴茎": 0.8, "阴道": 0.8, "做爱": 1.0, "口交": 1.0, "手淫": 0.9,
            "射精": 0.7, "高潮": 0.8, "群交": 1.0, "乱伦": 1.0, "强奸": 1.0,
            "偷拍": 1.0, "援交": 0.9, "SM": 0.9, "调教": 0.8, "奴隶": 0.6
        })

    def _add_keywords(self, lang: str, keywords: Dict[str, float]):
        for word, weight in keywords.items():
            self.trie.insert(word, category="nsfw", weight=weight)

    def analyze_text(self, text: str) -> Tuple[float, List[str]]:
        """
        Returns (max_weight, matched_words).
        """
        matches = self.trie.search_text(text.lower())
        if not matches:
            return 0.0, []
        
        max_weight = max(m['weight'] for m in matches)
        matched_words = [m['word'] for m in matches]
        return max_weight, matched_words


@dataclass
class FeatureVector:
    id: str
    vector: List[float]
    label: str

class FeatureDatabase:
    """
    Stores pre-computed feature vectors for fast similarity search.
    """
    def __init__(self):
        self.vectors: List[FeatureVector] = []
        self._populate()

    def _populate(self):
        for i in range(1000):
            vec = [math.sin(i * j) for j in range(128)]
            self.vectors.append(FeatureVector(
                id=f"vec_{i}",
                vector=vec,
                label="nsfw" if i % 2 == 0 else "safe"
            ))

    def search(self, query_vector: List[float], k: int = 5) -> List[Dict]:
        """
        Brute-force cosine similarity search (O(N)).
        """
        results = []
        q_norm = math.sqrt(sum(x*x for x in query_vector))
        
        for fv in self.vectors:
            dot = sum(q * v for q, v in zip(query_vector, fv.vector))
            v_norm = math.sqrt(sum(x*x for x in fv.vector))
            similarity = dot / (q_norm * v_norm + 1e-10)
            results.append({
                'id': fv.id,
                'label': fv.label,
                'score': similarity
            })
            
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]
