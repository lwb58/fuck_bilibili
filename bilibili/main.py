# -*- coding:utf-8 -*-
from api import submit_video

def main():
    info = {
        "copyright": 2,  # 1:有版权  2:无
        "source": "转自网络",  # 如果填写了该项则无版权
        "videos": [{
            "filename": "/Users/tuweifeng/Desktop/work/python/code/tools/gify/test.mp4",
            "title": "这是视频",
            "desc": "",
        }],
        "no_reprint": 0,  # 1：不允许转载  0：允许转载
        "interactive": 0,
        "tid": 21,
        "cover": "",  # 由b站返回封面文件名 可以为空，b站会从视频里取一帧作为封面
        "title": "动物救援行动",
        "tag": "动物,狗狗",  # 视频标签
        "desc_format_id": 0,
        "desc": "",
        "dynamic": "",
        "open_elec": 1,  # 1：开启充电面板 0：不开启
        "subtitle": {
            "open": 0,  # 不开字幕
            "lan": "zh-CN"
        },
        "up_selection_reply": False,
        "up_close_reply": False,
        "up_close_danmu": False,
        "act_reserve_create": 0,
    }
    cookies = "_uuid=F3846222-EDAD-6B5A-7FA8-9FF4F26B16CB51047infoc; buvid3=195A042F-86D0-4FA5-8383-308F1E5C0AED167614infoc; blackside_state=1; rpdid=|(Rlllk)lJ)0J'uYJRJkJJRY; fingerprint_s=da3a2638c24dcca6b74258261428ccd8; LIVE_BUVID=AUTO5716358409259242; PVID=1; fingerprint=79eac04582f75e05c84f486913f2a173; buvid_fp_plain=CA3E8107-D4DD-434A-9C2C-79F6F0B00C5B148804infoc; SESSDATA=50ed2a21%2C1652951349%2C17fad%2Ab1; bili_jct=1f15d82812474b5265bf304ab4692aed; DedeUserID=30784374; DedeUserID__ckMd5=7bdf9ca5dbe22cdd; sid=76zhkfa3; video_page_version=v_old_home; bsource=search_baidu; fingerprint3=13218a4955b4eb32d3fb75d74e13e063; CURRENT_BLACKGAP=1; CURRENT_FNVAL=80; CURRENT_QUALITY=0; innersign=0; i-wanna-go-back=-1; b_ut=5; b_lsid=A6712E62_17ED9125187; buvid_fp=a78d307997c2d2d15b68f6ac90018e18; buvid4=B858F982-52B9-D052-66A0-2B4E55DE503265029-022020819-PFJkqvvsrkqgERnDm+/ksg%3D%3D"
    submit_video(cookies, info)


if __name__ == "__main__":
    main()