#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from slacker import Slacker
import re
from datetime import datetime
import csv
import os
import json
import urllib.request
import difflib

def diff_func(slack, URL, FilePath, WhiteList):

    old_dir = os.path.join(FilePath, "old")
    new_dir = os.path.join(FilePath, "new")

    if not os.path.isdir(FilePath): #folder tree init
        os.makedirs(old_dir)
        os.makedirs(new_dir)
        urllib.request.urlretrieve(URL, os.path.join(old_dir, "main.html"))

    urllib.request.urlretrieve(URL, os.path.join(new_dir, "main.html"))

    with open(os.path.join(old_dir, "main.html")) as old_f, open(os.path.join(new_dir, "main.html")) as new_f:
        d = difflib.Differ()
        diff = d.compare(old_f.read(), new_f.read())

    comlist = []
    for com in diff:
        if re.fullmatch("[0-9]+c[0-9]+",com):
            comlist.append(com)

    if list(set(comlist)-set(WhiteList)):
        moved_dir = os.path.join(old_dir, datetime.now().strftime('%Y%m%d_%H-00'))
        os.makedirs(moved_dir)
        shutil.move(os.path.join(old_dir, "main.html"), moved_dir)
        shutil.move(os.path.join(new_dir, "main.html"), old_dir)
        return True

    else:
        os.remove(os.path.join(new_dir, "main.html"))
        return False

def main():
    # APIトークンを設定する
    json_path = os.path.join(os.path.dirname(__file__), "token.json")
    token_json = json.load(open(json_path,'r'))
    slack = Slacker(token_json["slack_api"])

    FilePath = os.path.join(os.path.dirname(__file__), "diff_data/")
    post_messages = []

    csv_path = os.path.join(os.path.dirname(__file__), "sitedata.csv")
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            sitename, URL = row[:2]
            whitelist = row[2:]
            if diff_func(slack, URL, FilePath + sitename, whitelist):
                post_messages.append([sitename, URL])

    if post_messages:
        # メッセージを成型しSlackにメッセージを送信する
        ans_texts = "\n".join([  s + " : " + u  for s, u in post_messages])
        slack.chat.post_message("更新情報", "サイト情報 変更あり\n" + ans_texts ,as_user = True)
    else:
        #更新なしのメッセージを送信
        slack.chat.post_message("更新情報", "現在までの更新はありません。" ,as_user = True)




if __name__ == "__main__":
    main()