#encoding: utf8

from wtforms import Form, SelectField

class BallotForm(Form):
    game = SelectField(u'赛事')
    ballot_type = SelectField(u'首轮抽签方式', choices=[('random', u'随机'), ('sequence', u'顺序')])

class RankForm(Form):
    game = SelectField(u'赛事')
    rank_type = SelectField(u'排名类型', choices=[('team', u'队伍排名'), ('company', u'团体排名')])