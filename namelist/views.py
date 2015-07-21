#encoding: utf8

from flask.ext.admin.contrib.mongoengine import ModelView
import sys
sys.path.append('..')
from filters import FilterGame

class NameListAdmin(ModelView):
    page_size = 15
    column_searchable_list = ['team_no', 'players', 'company']
    column_labels = {
            'game': u'赛事',
            'no': u'赛号',
            'company': u'单位名称',
            'team_no': u'队伍编号',
            'players': u'选手',
    }
    column_filters = [FilterGame('game', u'赛事')]