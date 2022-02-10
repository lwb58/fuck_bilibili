import math

BILIBILI_SEARCH_URL = "https://api.bilibili.com/x/web-interface/search/type"
BILIBILI_LOGIN_URL = "https://passport.bilibili.com/login"
BILIBILI_UPLOADER_MANAGER_URL = "https://member.bilibili.com/platform/upload-manager/article"
BILIBILI_LOGIN_SUCCESS_URL = "https://passport.bilibili.com/account/security#/home"
BILIBILI_PREUPLOAD_URL = "https://member.bilibili.com/preupload"
BILIBILI_UPOS_URL = "https://upos-sz-upcdnbda2.bilivideo.com/"
BILIBILI_UPLOAD_COVER_URL = "https://member.bilibili.com/x/vu/web/cover/up"
BILIBILI_UPLOAD_SUBMIT_URL = "https://member.bilibili.com/x/vu/web/add"


def search_users(session, user):
    '''查找用户'''
    res = session.get(url=BILIBILI_SEARCH_URL,
                      params={
                          "search_type": "bili_user",
                          "page": 1,
                          "keyword": user,
                          "highlight": 1,
                          "single_column": 0,
                      },
                      timeout=20)
    data = res.json().get("data") or {}
    users = data.get("result") or []
    return users


def preupload_video(session, video_name, video_size):
    '''获取预上传信息，上传权限，文件大小，文件资源名称等'''
    res = session.get(BILIBILI_PREUPLOAD_URL,
                      params={
                          "name": video_name,
                          "size": video_size,
                          "r": "upos",
                          "profile": "ugcupos/bup",
                          "ssl": "0",
                          "version": "2.10.4",
                          "build": "2100400",
                          "upcdn": "bda2",
                          "probe_version": "20200810"
                      },
                      timeout=3)
    return res.json()


def preupload_video_upos(session, uri):
    '''获取上传ID'''
    res = session.post(BILIBILI_UPOS_URL + uri,
                       params={
                           "uploads": "",
                           "output": "json"
                       },
                       timeout=3)
    return res.json()


def preupload_video_upos_file(session, video_size, iter_content, uri,
                              upload_id):
    '''上传视频文件'''
    chunk_size = 1024 * 1024
    total_chunks = math.ceil(video_size * 1.0 / chunk_size)
    partinfo = []
    for i, data in enumerate(iter_content(chunk_size)):
        session.put(BILIBILI_UPOS_URL + uri,
                    params={
                        "partNumber": i + 1,
                        "uploadId": upload_id,
                        "chunk": i,
                        "chunks": total_chunks,
                        "size": len(data),
                        "start": i * chunk_size,
                        "end": i * chunk_size + len(data),
                        "total": video_size
                    },
                    data=data,
                    timeout=20)
        partinfo.append({'partNumber': i + 1, 'eTag': 'etag'})
    if not partinfo:
        raise Exception("partinfo error")
    return partinfo


def preupload_video_upos_file_sure(session, video_name, uri, upload_id, biz_id,
                                   partinfo):
    '''确认文件上传完成'''
    session.post(BILIBILI_UPOS_URL + uri,
                 params={
                     "output": "json",
                     "name": video_name,
                     "profile": "ugcupos/bup",
                     "uploadId": upload_id,
                     "biz_id": biz_id
                 },
                 json={"parts": partinfo},
                 timeout=3)


def upload_video_cover(session, cover_base64):
    '''上传封面'''
    csrf = session.cookies.get("bili_jct")
    res = session.post(BILIBILI_UPLOAD_COVER_URL,
                       data={
                           'cover': cover_base64,
                           'csrf': csrf,
                       },
                       timeout=20)
    return res.json()


def upload_video_submit(session, upload_info):
    '''提交视频信息，版权，标签，简介等'''
    csrf = session.cookies.get("bili_jct")
    res = session.post(BILIBILI_UPLOAD_SUBMIT_URL,
                       params={
                           "csrf": csrf,
                       },
                       json=upload_info)
    return res.json()
