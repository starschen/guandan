#encoding: utf8
import xlrd
import sys
sys.path.append('..')
from mongodb import guandan_db

def import_namelist():
    book = xlrd.open_workbook(u'掼蛋比赛名单.xls')
    table = book.sheet_by_index(0)

    nrows = table.nrows
    ncols = table.ncols
    game = guandan_db.game.find_one({'name':u'徐州市第十六届“中国大地保险杯”掼蛋比赛'})

    for i in range(1, nrows):
        record = {}
        record['game'] = game['_id']
        record['no'] = i
        record['company'] = table.cell(i,0).value
        record['team_no'] = table.cell(i,1).value
        record['players'] = table.cell(i,2).value
        guandan_db.name_list.insert(record)

def import_gamerecord():
    book = xlrd.open_workbook(u'第二轮汇总表.xls')
    table = book.sheet_by_index(0)
    calced_teams = set()

    nrows = table.nrows
    ncols = table.ncols

    count = 0
    for i in range(1, nrows):
        if table.cell(i,3).value in calced_teams:
            continue
        record = {}
        record['round'] = 1
        record['red'] = guandan_db.name_list.find_one(dict(team_no=table.cell(i,1).value))['_id']
        record['blue'] = guandan_db.name_list.find_one(dict(team_no=table.cell(i,3).value))['_id']
        scores = table.cell(i,4).value.split('/')
        if int(scores[0]) == 2:
            record['result'] = u'红方胜'
        elif int(scores[0]) == 0:
            record['result'] = u'蓝方胜'
        elif int(scores[0]) == 1:
            record['result'] = u'平局'
        elif int(scores[0]) == -1:
            record['result'] = u'红方弃权'
        record['diff'] = abs(int(scores[1]))
        count += 1
        record['desk_no'] = count
        calced_teams.add(table.cell(i,1).value)
        calced_teams.add(table.cell(i,3).value)
        #print record
        guandan_db.game_record.insert(record)

import_gamerecord()