#encoding: utf8

import sys
sys.path.append('..')
from db import db
from game.models import Game

class NameList(db.Document):
    game = db.ReferenceField(Game, verbose_name=u'赛事')
    no = db.IntField(unique_with='game', verbose_name=u'赛号')
    company = db.StringField(verbose_name=u'单位名称')
    team_no = db.StringField(verbose_name=u'队伍编号')
    players = db.StringField(verbose_name=u'选手')

    def __unicode__(self):
        return u'赛号：%d 选手：%s 单位：%s' % (self.no, self.players, self.company)
