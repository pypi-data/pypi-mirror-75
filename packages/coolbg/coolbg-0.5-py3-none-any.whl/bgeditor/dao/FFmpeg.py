import math
from moviepy.editor import VideoFileClip
from moviepy.video.fx import make_loopable
from bgeditor.common.utils import get_dir
import uuid
import os
import shutil

def create_source_can_loop(dir_path, clip_path, is_delete = True):
    tmp_clip_path_z_resync = None
    try:
        clip = VideoFileClip(clip_path)
        clip = make_loopable.make_loopable(clip, 0.5)
        tmp_clip_path_z = dir_path + "/" + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
        tmp_clip_path_z_resync = dir_path + "/" + str(uuid.uuid4()) + '-re-sync-' + \
                                  os.path.basename(clip_path).split(".")[0] + ".avi"
        clip.write_videofile(tmp_clip_path_z, fps=clip.fps, codec='libx264')
        clip.close()
        cmd = "ffmpeg -y -i \"%s\" \"%s\"" % (tmp_clip_path_z, tmp_clip_path_z_resync)
        os.system(cmd)
        os.remove(tmp_clip_path_z)
        if is_delete:
            os.remove(clip_path)
        try:
            clip = VideoFileClip(tmp_clip_path_z_resync)
            if clip.duration is None or clip.duration < 0.1:
                tmp_clip_path_z_resync = None
        except:
            tmp_clip_path_z_resync = None
            pass
    except:
        pass
    return tmp_clip_path_z_resync

def create_loop(clip_path, loop_duration, can_loopable = True):
    try:
        clip = VideoFileClip(clip_path)
        if not can_loopable:
            try:
                if clip.duration > loop_duration:
                    return clip_path
                clip = make_loopable.make_loopable(clip, 0.5)
                tmp_clip_path_z = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
                #tmp_clip_path_z_resync = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-re-sync-' + os.path.basename(clip_path).split(".")[0]+".avi"
                clip.write_videofile(tmp_clip_path_z, fps=clip.fps, codec='libx264')
                clip.close()
                # cmd = "ffmpeg -y -i \"%s\" \"%s\"" % (tmp_clip_path_z, tmp_clip_path_z_resync)
                # os.system(cmd)
                # os.remove(tmp_clip_path_z)
                clip = VideoFileClip(tmp_clip_path_z)
                tmp_clip_path = tmp_clip_path_z
            except:
                pass
        else:
            tmp_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(clip_path)
            shutil.copyfile(clip_path, tmp_clip_path)

        clip_duration = clip.duration
        clip.close()
        times = int(math.ceil(loop_duration / clip_duration))
        file_merg_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4())
        final_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-final-' + os.path.basename(clip_path)
        file_merg = open(file_merg_path, "a")
        for i in range(times):
            file_merg.write("file '%s'\n" % os.path.basename(tmp_clip_path))
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        os.remove(tmp_clip_path)
        os.remove(file_merg_path)
        clip = VideoFileClip(final_clip_path)
        clip_duration = clip.duration
        clip.close()
        if clip_duration < loop_duration:
            return None
        return final_clip_path
    except:
        return None
