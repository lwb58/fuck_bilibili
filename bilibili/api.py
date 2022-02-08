import os
import copy
import base64
from bilibili.base.session import Session
from bilibili.base import api
import requests


class LocalVideo:
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(filepath)
        self.size = os.path.getsize(filepath)
        self.filetype = os.path.splitext(filepath)[-1].lstrip(".")

    def iter_content(self, chunk_size):
        with open(self.filepath, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                yield chunk
                chunk = f.read(chunk_size)


def upload_video(session, file):
    if file.startswith("http"):
        # todo 网络视频直接上传
        video = None
    elif os.path.exists(file) and os.path.isfile(file):
        video = LocalVideo(file)
    else:
        raise Exception(f"can not find: {file}")
    # 1. 预上传文件基本信息
    data = api.preupload_video(session, video.name, video.size)
    uri = data["upos_uri"][len("upos://"):]
    file_id = uri.split("/")[-1][:-len(video.filetype) - 1]
    biz_id = data["biz_id"]
    session.headers.update({"x-upos-auth": data["auth"]})

    # 2. 领取上传ID
    data = api.preupload_video_upos(session, uri)
    upload_id = data["upload_id"]

    # 3. 分块上传
    partinfo = api.preupload_video_upos_file(session, video.size,
                                             video.iter_content, uri,
                                             upload_id)

    # 4. 确定文件上传完成
    api.preupload_video_upos_file_sure(session, video.name, uri, upload_id,
                                       biz_id, partinfo)
    return file_id


def upload_cover(session, file):
    if file.startswith("http"):
        content = requests.get(file, timeout=20)
    elif os.path.exists(file) and os.path.isfile(file):
        with open(file, "rb") as f:
            content = f.read()
    else:
        raise Exception(f"can not find: {file}")
    cover_base64 = b'data:image/jpeg;base64,' + base64.b64encode(content)
    data = api.upload_video_cover(session, cover_base64)
    file_id = data["data"]["url"].split(":")[-1]
    return file_id


def submit_video(cookies, submit_info):
    '''视频投稿'''
    info = copy.deepcopy(submit_info)
    with Session(cookies=cookies, tries=5) as session:
        for video in info["videos"]:
            video["filename"] = upload_video(session, video["filename"])
        try:
            info["cover"] = upload_cover(session, info["cover"])
        except:
            info["cover"] = ""
        res = api.upload_video_submit(session, info)
    print(res)