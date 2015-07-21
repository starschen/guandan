#encoding: utf8

import sys
sys.path.append('..')
from db import db

class Game(db.Document):
    name = db.StringField(verbose_name=u'赛事名称')

    def __unicode__(self):
        return self.name