#encoding: utf8

from flask import request, abort
from flask.ext.admin import BaseView, expose
from bson.objectid import ObjectId
import sys
import random
from operator import attrgetter
sys.path.append('..')
from game_record.models import GameRecord
from game.models import Game
from namelist.models import NameList
from forms import BallotForm, RankForm
import json

class Team:
    def __init__(self, namelist):
        self.namelist = namelist
        self.total_score = 0
        self.total_sscore = 0
        self.total_diff = 0
        self.againsts = []

    def get_company(self):
        return self.namelist.company.strip()

    def has_competed_with(self, against):
        if against in self.againsts:
            return True
        else:
            return False

    def add_score(self, score):
        self.total_score += score

    def add_diff(self, diff):
        self.total_diff += diff

    def add_against(self, against):
        self.againsts.append(against)

    def compute_sscore(self):
        for a in self.againsts:
            #计算小分时，弃权所得负分不影响对手小分
            if a.total_score >= 0:
                self.total_sscore += a.total_score

class Company:
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.total_score = 0
        self.total_sscore = 0
        self.total_diff = 0

    def add_team(self, team):
        self.teams.append(team)

    def compute_score(self):
        for team in self.teams:
            self.total_score += team.total_score
            self.total_sscore += team.total_sscore
            self.total_diff += team.total_diff

class BallotView(BaseView):
    round = 0
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = BallotForm(request.form)
        form.game.choices = [(str(Game.objects(name=x).first().id), x) for x in Game.objects.distinct('name')]
        if request.method == 'POST' and form.validate():
            game = form.game.data
            ballot_type = form.ballot_type.data
            results = self.ballot(game, ballot_type)
            self._template_args['ballot_results'] = results
            self._template_args['round'] = self.round
        return self.render('ballot.html', form=form)


    def first_stage(self, game, ballot_type):
        """首轮抽签"""
        results = []
        teams = list(NameList.objects(game=game).order_by('no').all())
        team_count = len(teams) / 2 * 2
        if ballot_type == 'sequence':
            for i in range(0, team_count, 2):
                result = dict(desk_no=i/2+1, red=teams[i], blue=teams[i+1])
                results.append(result)
            return results
        else:
            return self.ballot_by_score(game, ballot_type)

    def ballot_by_score(self, game, ballot_type):
        """按照比分抽签"""
        results = []
        teams = RankView.get_ranked_teams(game)
        while len(teams) > 1:
            #处理后四名出现同一个单位的情况
            if len(teams) == 4 and (teams[0].get_company() == teams[1].get_company() or teams[2].get_company()  == teams[3].get_company()):
                results.append(dict(desk_no=len(results)+1, red=teams[0].namelist, blue=teams[2].namelist))
                results.append(dict(desk_no=len(results)+1, red=teams[1].namelist, blue=teams[3].namelist))
                break
            t1 = teams[0]
            for t2 in teams[1:]:
                #找到不同单位并且没有比赛过的对手
                if t1.get_company() != t2.get_company() and not t1.has_competed_with(t2):
                    break
            results.append(dict(desk_no=len(results)+1, red=t1.namelist, blue=t2.namelist))
            teams.remove(t1)
            teams.remove(t2)
        return results

    def ballot(self, game, ballot_type):
        """抽签算法"""
        if GameRecord.objects(game=game).count() == 0:
            self.round = 1
            return self.first_stage(game, ballot_type)
        else:
            self.round = max(GameRecord.objects(game=game).distinct('round')) + 1
            return self.ballot_by_score(game, ballot_type)

class RankView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = RankForm(request.form)
        form.game.choices = [(str(Game.objects(name=x).first().id), x) for x in Game.objects.distinct('name')]
        return self.render('rank.html', form=form)

    @expose('/team_rank_ajax')
    def team_rank_ajax(self):
        results = []
        game = request.args.get('game', '')
        ranked_teams = self.get_ranked_teams(game)
        for index, team in enumerate(ranked_teams):
            record = {}
            record['rank'] = index + 1
            record['rank_type'] = unicode(team.namelist)
            record['total_score'] = team.total_score
            record['total_sscore'] = team.total_sscore
            record['total_diff'] = team.total_diff
            results.append(record)

        return json.dumps(results)

    @expose('/company_rank_ajax')
    def company_rank_ajax(self):
        game = request.args.get('game', '')
        ranked_companys = self.get_ranked_companys(game)
        results = []
        for index, c in enumerate(ranked_companys):
            record = {}
            record['rank'] = index + 1
            record['rank_type'] = c.name
            record['total_score'] = c.total_score
            record['total_sscore'] = c.total_sscore
            record['total_diff'] = c.total_diff
            results.append(record)
        return json.dumps(results)

    @staticmethod
    def get_ranked_teams(game):
        teams = {x:Team(x) for x in NameList.objects(game=game)}
        for record in GameRecord.objects(game=game):
            if record.result == u'红方胜':
                teams[record.red].add_score(2)
                teams[record.red].add_diff(record.diff)
                teams[record.blue].add_diff(0 - record.diff)
            elif record.result == u'蓝方胜':
                teams[record.blue].add_score(2)
                teams[record.blue].add_diff(record.diff)
                teams[record.red].add_diff(0 - record.diff)
            elif record.result == u'平局':
                teams[record.blue].add_score(1)
                teams[record.red].add_score(1)
            elif record.result == u'红方弃权':
                teams[record.red].add_score(-1)
                teams[record.red].add_diff(-6)
                teams[record.blue].add_score(2)
                teams[record.blue].add_diff(6)
            elif record.result == u'蓝方弃权':
                teams[record.blue].add_score(-1)
                teams[record.blue].add_diff(-6)
                teams[record.red].add_score(2)
                teams[record.red].add_diff(6)
            teams[record.red].add_against(teams[record.blue])
            teams[record.blue].add_against(teams[record.red])

        for team in teams.values():
            team.compute_sscore()

        team_list = teams.values()
        random.shuffle(team_list)
        return sorted(team_list, key=attrgetter('total_score', 'total_sscore', 'total_diff'), reverse=True)

    @staticmethod
    def get_ranked_companys(game):
        companys = {}
        for team in RankView.get_ranked_teams(game):
            company_name = team.get_company()
            if company_name not in companys:
                companys[company_name] = Company(company_name)
            companys[company_name].add_team(team)

        [c.compute_score() for c in companys.values()]
        return sorted(companys.values(), key=attrgetter('total_score', 'total_sscore', 'total_diff'), reverse=True)