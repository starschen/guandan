#encoding: utf8
from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter
from game.models import Game
from flask_admin.babel import lazy_gettext

class FilterGame(BaseMongoEngineFilter):
    def apply(self, query, value):
        return query.filter(game__exact=Game.objects(name__exact=value).first().id)

    def operation(self):
        return lazy_gettext('exact')

    def get_options(self, view):
        game_list = [(obj.name, obj.name) for obj in Game.objects()]
        return game_list