import re
import sys
import argparse
import os
import json
import time
import shutil

from bilili.utils.base import repair_filename, touch_dir, touch_file, size_format
from bilili.utils.quality import quality_sequence_default
from bilili.utils.playlist import Dpl, M3u
from bilili.utils.thread import ThreadPool, Flag
from bilili.utils.console import Console, Font, Line, String, ProgressBar, List, DynamicSign
from bilili.api.subtitle import get_subtitle
from bilili.api.danmaku import get_danmaku
from bilili.tools import (spider, ass, regex_acg_video_av, regex_acg_video_av_short,
                          regex_acg_video_bv, regex_acg_video_bv_short, regex_bangumi)
from bilili.video import global_middleware
from bilili.events.downloader import RemoteFile
from bilili.events.merger import MergingFile


def parse_episodes(episodes_str, total):
    """ 将选集字符串转为列表 """

    # 解析字符串为列表
    print("全 {} 话".format(total))
    if episodes_str == "all":
        episode_list = list(range(1, total+1))
    elif re.match(r"\d+~\d+", episodes_str):
        start, end = episodes_str.split("~")
        start, end = int(start), int(end)
        assert end > start, "终点值应大于起点值"
        episode_list = list(range(start, end+1))
    elif re.match(r"\d+(,\d+)*", episodes_str):
        episode_list = episodes_str.split(",")
        episode_list = list(map(int, episode_list))
    else:
        episode_list = []

    # 筛选满足条件的剧集
    out_of_range = []
    episodes = []
    for episode in episode_list:
        if episode in range(1, total+1):
            if episode not in episodes:
                episodes.append(episode)
        else:
            out_of_range.append(episode)
    if out_of_range:
        print("warn: 剧集 {} 不存在".format(",".join(list(map(str, out_of_range)))))

    print("已选择第 {} 话".format(",".join(list(map(str, episodes)))))
    assert episodes, "没有选中任何剧集"
    return episodes


def main():
    """ 解析命令行参数并调用相关模块进行下载 """

    parser = argparse.ArgumentParser(description="bilili B 站视频、弹幕下载器")
    parser.add_argument("url", help="视频主页地址")
    parser.add_argument('-f', '--format', default='m4s',
                        choices=['flv', 'm4s', 'mp4'], help="选择下载源格式（m4s 或 flv 或 mp4）")
    parser.add_argument("-d", "--dir", default=r"", help="下载目录")
    parser.add_argument("-q", "--quality", default='120', choices=['120', '116', '112', '80', '74', '64', '32', '16', '6'],
                        help="视频清晰度 120:4K, 116:1080P60, 112:1080P+, 80:1080P, 74:720P60, 64:720P, 32:480P, 16:360P, 6:240P")
    parser.add_argument("-t", "--num-threads", default=30,
                        type=int, help="最大下载线程数")
    parser.add_argument("-p", "--episodes", default="all", help="选集")
    parser.add_argument("-w", "--overwrite",
                        action="store_true", help="强制覆盖已下载视频")
    parser.add_argument("-c", "--sess-data", default=None, help="输入 cookies")
    parser.add_argument("--playlist-type", default="dpl",
                        choices=["dpl", "m3u", "no"], help="播放列表类型，支持 dpl 和 m3u，输入 no 不生成播放列表")
    parser.add_argument("--path-type", default="rp",
                        help="播放列表路径类型（rp：相对路径，ap：绝对路径）")
    parser.add_argument("--danmaku", default="xml",
                        choices=["xml", "ass", "no"], help="弹幕类型，支持 xml 和 ass，如果设置为 no 则不下载弹幕")
    parser.add_argument("--debug", action="store_true", help="debug 模式")
    parser.add_argument("-y", "--yes", action="store_true", help="跳过下载询问")

    args = parser.parse_args()
    cookies = {
        "SESSDATA": args.sess_data
    }

    config = {
        "url": args.url,
        "dir": args.dir,
        "quality_sequence": quality_sequence_default[quality_sequence_default.index(int(args.quality)):] +
        list(reversed(quality_sequence_default[:quality_sequence_default.index(int(args.quality))])),
        "episodes": args.episodes,
        "playlist_type": args.playlist_type,
        "playlist_path_type": args.path_type.upper(),
        "overwrite": args.overwrite,
        "cookies": cookies,
        "format": args.format.lower(),
    }

    if regex_acg_video_av.match(args.url) or \
       regex_acg_video_av_short.match(args.url) or \
       regex_acg_video_bv.match(args.url) or \
       regex_acg_video_bv_short.match(args.url):
        bili_type = "acg_video"
        from bilili.api.acg_video import get_title, get_context, get_containers, parse_segments
    elif regex_bangumi.match(args.url):
        bili_type = "bangumi"
        from bilili.api.bangumi import get_title, get_context, get_containers, parse_segments
    else:
        print("视频地址有误！")
        sys.exit(1)

    home_url = args.url

    # 获取标题
    spider.set_cookies(config["cookies"])
    title = get_title(home_url)
    print(title)

    # 创建所需目录结构
    base_dir = touch_dir(os.path.join(
        config['dir'], repair_filename(title + " - bilibili")))
    video_dir = touch_dir(os.path.join(base_dir, "Videos"))
    if args.overwrite:
        shutil.rmtree(video_dir)
        touch_dir(video_dir)
    if config['playlist_type'] == 'dpl':
        playlist = Dpl(os.path.join(base_dir, 'Playlist.dpl'),
                       path_type=config["playlist_path_type"])
    elif config["playlist_type"] == "m3u":
        playlist = M3u(os.path.join(base_dir, 'Playlist.m3u'),
                       path_type=config["playlist_path_type"])
    else:
        playlist = None

    # 获取需要的信息
    context = get_context(home_url)
    containers = get_containers(context, video_dir, config['format'], playlist)

    # 解析并过滤不需要的选集
    episodes = parse_episodes(config["episodes"], len(containers))
    containers, containers_need_filter = [], containers
    for container in containers_need_filter:
        if container.id not in episodes:
            container._.downloaded = True
            container._.merged = True
        else:
            containers.append(container)

    # 解析片段信息及视频 url
    for i, container in enumerate(containers):
        print("{:02}/{:02} parsing segments info...".format(i,
                                                            len(containers)), end="\r")
        if bili_type == 'acg_video':
            get_subtitle(container)
        if args.danmaku != 'no':
            get_danmaku(container)

        parse_segments(container, config['quality_sequence'])

        if args.danmaku == 'ass':
            ass.convert_danmaku_from_xml(
                os.path.splitext(container.path)[0]+'.xml', container.height, container.width)

    # 准备下载
    if containers:
        # 状态检查与校正
        for i, container in enumerate(containers):
            container_downloaded = os.path.exists(container.path)
            sign = "✓" if container_downloaded else "✖"
            if container_downloaded:
                container._.merged = True
            print("{} {}".format(sign, str(container)))
            for media in container.medias:
                media_downloaded = os.path.exists(media.path)
                sign = "✓" if media_downloaded else "✖"
                media._.downloaded = media_downloaded or container_downloaded
                if not container_downloaded:
                    print("    {} {}".format(sign, media.name))

        # 询问是否下载，通过参数 -y 可以跳过
        if not args.yes:
            answer = None
            while answer is None:
                result = input("以上标 ✖ 为需要进行下载的视频，是否立刻进行下载？[Y/n]")
                if result == '' or result[0].lower() == 'y':
                    answer = True
                elif result[0].lower() == 'n':
                    answer = False
                else:
                    answer = None
            if not answer:
                sys.exit(0)

        # 部署下载与合并任务
        merge_wait_flag = Flag(False)                       # 合并线程池不能因为没有任务就结束
        merge_pool = ThreadPool(3, wait=merge_wait_flag)    # 因此要设定一个 flag，待最后合并结束后改变其值
        download_pool = ThreadPool(args.num_threads)
        for container in containers:
            merging_file = MergingFile(container.format,
                            [media.path for media in container.medias], container.path)
            for media in container.medias:
                remote_file = RemoteFile(media.url, media.path)

                # 为下载挂载各种钩子，以修改状态
                @remote_file.on('before_download')
                def before_download(file, middleware=media._):
                    middleware.downloading = True

                @remote_file.on('updated', middleware=media._)
                def updated(file, middleware=None):
                    middleware.size = file.size

                @remote_file.on('downloaded', middleware=media._, merging_file=merging_file)
                def downloaded(file, middleware=None, merging_file=None):
                    middleware.downloaded = True
                    middleware.downloading = False

                    # 下载完的，部署合并任务
                    if middleware.parent.downloaded and not middleware.parent.merged:

                        # 为合并挂载各种钩子
                        @merging_file.on('before_merge', middleware=middleware.parent)
                        def before_merge(file, middleware=None):
                            for child in middleware.children:
                                child.merging = True

                        @merging_file.on('merged', middleware=middleware.parent)
                        def merged(file, middleware=None):
                            middleware.merging = False
                            middleware.merged = True

                        merge_pool.add_task(merging_file.merge, args=())

                # 下载过的不应继续部署任务
                if media._.downloaded:
                    continue
                download_pool.add_task(remote_file.download, args=(spider, ))

        # 启动线程池
        merge_pool.run()
        download_pool.run()

        # 初始化界面
        console = Console(debug=args.debug)
        console.add_component(
            Line(center=Font(char_a='𝓪', char_A='𝓐'), fillchar='='))
        console.add_component(Line(left=String(), fillchar=' '))
        console.add_component(
            List(Line(left=String(), right=String(), fillchar='-')))
        console.add_component(Line(left=ProgressBar(
            width=65), right=String(), fillchar=' '))
        console.add_component(Line(left=String(), fillchar=' '))
        console.add_component(
            List(Line(left=String(), right=DynamicSign(), fillchar=' ')))
        console.add_component(Line(left=ProgressBar(
            width=65), right=String(), fillchar=' '))

        # 准备监控
        size, t = global_middleware.size, time.time()
        while True:
            now_size, now_t = global_middleware.size, time.time()
            delta_size, delta_t = max(
                now_size - size, 0), (now_t - t) if now_t - t > 1e-6 else 1e-6
            speed = delta_size / delta_t
            size, t = now_size, now_t

            # 数据传入，界面渲染
            console.refresh([
                {
                    'center': ' 🍻 bilili ',
                },
                {
                    'left': '🌠 Downloading videos: '
                } if global_middleware.downloading else None,
                [
                    {
                        'left': '{} '.format(str(container)),
                        'right': ' {}/{}'.format(
                            size_format(container._.size),
                            size_format(container._.total_size)
                        )
                    } if container._.downloading else None for container in containers
                ] if global_middleware.downloading else None,
                {
                    'left': global_middleware.size / global_middleware.total_size,
                    'right': " {}/{} {}/s ⚡".format(
                        size_format(global_middleware.size),
                        size_format(global_middleware.total_size),
                        size_format(speed)
                    )
                } if global_middleware.downloading else None,
                {
                    'left': '🍰 Merging videos: '
                } if global_middleware.merging else None,
                [
                    {
                        'left': '{} '.format(str(container)),
                        'right': True
                    } if container._.merging else None for container in containers
                ] if global_middleware.merging else None,
                {
                    'left': sum([container._.merged for container in containers]) / len(containers),
                    'right': " {}/{} 🚀".format(
                        sum([container._.merged for container in containers]),
                        len(containers)
                    )
                } if global_middleware.merging else None,
            ])

            # 检查是否已经全部完成
            if global_middleware.downloaded and global_middleware.merged:
                merge_wait_flag.value = True
                break
            try:
                # 将刷新率稳定在 1fps
                time.sleep(max(1-(time.time()-now_t), 0.01))
            except (SystemExit, KeyboardInterrupt):
                raise
        print("已全部下载完成！")
    else:
        print("没有需要下载的视频！")


if __name__ == "__main__":
    main()
