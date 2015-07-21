# -*- coding: utf-8 -*-
from Tkinter import * 
import tkFileDialog
import xlwt

def export_team_rank(game):
    if game is None:
        game.st.insert(END, '请先导入文件.\n')
        return 
    filename = tkFileDialog.asksaveasfilename(initialdir = './', defaultextension='.xls',  initialfile='队伍排名')
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('队伍排名')
    header = ['排名', '赛号', '选手一', '选手二', '单位', '总大分', '总小分', '总级差']
    for index, item in enumerate(header):
        sheet.write(0, index, header[index])

    teams = game.team_rank()
    for i, t in enumerate(teams):
        sheet.write(i+1, 0, i+1)
        sheet.write(i+1, 1, t.get_no())
        sheet.write(i+1, 2, t.get_p1())
        sheet.write(i+1, 3, t.get_p2())
        sheet.write(i+1, 4, t.get_cname())
        sheet.write(i+1, 5, t.get_total_score())
        sheet.write(i+1, 6, t.get_total_sscore())
        sheet.write(i+1, 7, t.get_total_diff())
    wbk.save(filename)
    return filename