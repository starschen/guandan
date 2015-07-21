#encoding: utf8

import sys
sys.path.append('..')
from db import db
from namelist.models import NameList
from game.models import Game

class GameRecord(db.Document):
    game = db.ReferenceField(Game, verbose_name=u'赛事')
    round = db.IntField(verbose_name=u'轮次')
    desk_no = db.IntField(verbose_name=u'桌号')
    red = db.ReferenceField(NameList, verbose_name=u'红方')
    blue = db.ReferenceField(NameList, verbose_name=u'蓝方')
    result = db.StringField(choices=[(u'红方胜', u'红方胜'), (u'蓝方胜', u'蓝方胜'), (u'平局', u'平局'), (u'红方弃权', u'红方弃权'), (u'蓝方弃权', u'蓝方弃权')], verbose_name=u'赛果')
    diff = db.IntField(default=6, verbose_name=u'级差') #级差