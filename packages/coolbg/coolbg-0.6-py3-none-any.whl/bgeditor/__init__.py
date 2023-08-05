import os

os.environ["IMAGEMAGICK_BINARY"] = "magick"
from bgeditor.dao.FFmpeg import create_source_can_loop, create_loop
from bgeditor.dao.Lyric import Lyric
from bgeditor.common.utils import download_file
import tempfile


class BGEditor():
    def __init__(self):
        self.root_dir = tempfile.TemporaryDirectory()

    def create_source_can_loop_by_file(self, ori_file, is_delete=True):
        if ori_file:
            path_loop = create_source_can_loop(self.root_dir.name, ori_file, is_delete)
            return path_loop
        else:
            return None

    def download_video(self, url):
        return download_file(url, self.root_dir.name)

    def loop_video(self, ori_file, duration, can_loopable):
        return create_loop(ori_file, duration, can_loopable)

    def create_lyric_bg_video(self, lyric_data, font_url, font_size, color, duration, w=1920, h=1080):
        lyric = Lyric(lyric_data, font_url, font_size, color, duration, w, h)
        if lyric.init():
            return lyric.make()
        return None

    def close(self):
        self.root_dir.cleanup()




