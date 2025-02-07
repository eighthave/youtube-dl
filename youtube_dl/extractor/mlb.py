from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    parse_duration,
    parse_iso8601,
    find_xpath_attr,
)


class MLBIE(InfoExtractor):
    _VALID_URL = r'http?://m\.mlb\.com/video/(?:topic/[\da-z_-]+/)?v(?P<id>n?\d+)'
    _TESTS = [
        {
            'url': 'http://m.mlb.com/video/topic/81536970/v34496663/mianym-stanton-practices-for-the-home-run-derby',
            'md5': 'd9c022c10d21f849f49c05ae12a8a7e9',
            'info_dict': {
                'id': '34496663',
                'ext': 'mp4',
                'title': 'Stanton prepares for Derby',
                'description': 'md5:d00ce1e5fd9c9069e9c13ab4faedfa57',
                'duration': 46,
                'timestamp': 1405105800,
                'upload_date': '20140711',
                'thumbnail': 're:^https?://.*\.jpg$',
            },
        },
        {
            'url': 'http://m.mlb.com/video/topic/vtp_hrd_sponsor/v34578115/hrd-cespedes-wins-2014-gillette-home-run-derby',
            'md5': '0e6e73d509321e142409b695eadd541f',
            'info_dict': {
                'id': '34578115',
                'ext': 'mp4',
                'title': 'Cespedes repeats as Derby champ',
                'description': 'md5:08df253ce265d4cf6fb09f581fafad07',
                'duration': 488,
                'timestamp': 1405399936,
                'upload_date': '20140715',
                'thumbnail': 're:^https?://.*\.jpg$',
            },
        },
        {
            'url': 'http://m.mlb.com/video/v34577915/bautista-on-derby-captaining-duties-his-performance',
            'md5': 'b8fd237347b844365d74ea61d4245967',
            'info_dict': {
                'id': '34577915',
                'ext': 'mp4',
                'title': 'Bautista on Home Run Derby',
                'description': 'md5:b80b34031143d0986dddc64a8839f0fb',
                'duration': 52,
                'timestamp': 1405390722,
                'upload_date': '20140715',
                'thumbnail': 're:^https?://.*\.jpg$',
            },
        },
    ]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        detail = self._download_xml(
            'http://m.mlb.com/gen/multimedia/detail/%s/%s/%s/%s.xml'
            % (video_id[-3], video_id[-2], video_id[-1], video_id), video_id)

        title = detail.find('./headline').text
        description = detail.find('./big-blurb').text
        duration = parse_duration(detail.find('./duration').text)
        timestamp = parse_iso8601(detail.attrib['date'][:-5])

        thumbnail = find_xpath_attr(
            detail, './thumbnailScenarios/thumbnailScenario', 'type', '45').text

        formats = []
        for media_url in detail.findall('./url'):
            playback_scenario = media_url.attrib['playback_scenario']
            fmt = {
                'url': media_url.text,
                'format_id': playback_scenario,
            }
            m = re.search(r'(?P<vbr>\d+)K_(?P<width>\d+)X(?P<height>\d+)', playback_scenario)
            if m:
                fmt.update({
                    'vbr': int(m.group('vbr')) * 1000,
                    'width': int(m.group('width')),
                    'height': int(m.group('height')),
                })
            formats.append(fmt)

        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'duration': duration,
            'timestamp': timestamp,
            'formats': formats,
            'thumbnail': thumbnail,
        }
