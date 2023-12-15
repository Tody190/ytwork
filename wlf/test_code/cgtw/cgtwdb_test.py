# coding:utf-8
import sys

sys.path.append('C:/CgTeamWork_v7/bin/base')

import cgtw2

t_tw = cgtw2.tw(http_ip="192.168.55.12:18383",
                account="yangtao",
                password="Yt20231204")
print(t_tw.get_version())
print(cgtw2.G_tw_http_ip)
print(cgtw2.G_tw_account_id)