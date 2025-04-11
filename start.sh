#!/bin/bash
python geekaiapp/g_jiekou.py &
python geekaiapp/jimeng_video_service.py &
wait  # 等待所有后台进程完成