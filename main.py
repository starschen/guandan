#encoding: utf8

from flask import Flask, render_template
from flask.ext.basicauth import BasicAuth
from flask.ext.babel import Babel
from flask.ext.admin import Admin, AdminIndexView
import namelist
import game_record
import game
from views import *
from db import db

app = Flask(__name__)
app.config.from_object("settings")

basic_auth = BasicAuth(app)
db.init_app(app)
babel = Babel(app)

#admin
admin = Admin(app, u'掼蛋赛事管理系统', template_mode='bootstrap3',  index_view=AdminIndexView(
                    name=u'主页',
                    template='admin/index.html',
                    url='/'
                ))
admin.add_view(game.views.GameAdmin(game.models.Game, name=u'赛事', endpoint='game'))
admin.add_view(namelist.views.NameListAdmin(namelist.models.NameList, name=u'比赛名单', endpoint='namelist'))
admin.add_view(game_record.views.GameRecordAdmin(game_record.models.GameRecord, name=u'比赛记录', endpoint='game-record'))
admin.add_view(BallotView(name=u'抽签', endpoint='ballot'))
admin.add_view(RankView(name=u'排名', endpoint='rank'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
