# -*- coding: utf-8 -*-
import tkFileDialog
import xlwt

ROW_HEIGHT = 500

def export_ballot_result(game):
	filename = tkFileDialog.asksaveasfilename(initialdir = './', defaultextension='.xls', 
	initialfile='第%s轮抽签结果' % (game.get_stageno()+1))
	wbk = xlwt.Workbook(encoding='utf-8')
	sheet = wbk.add_sheet('sheet 1')

	#设定字体和边框
	style = xlwt.easyxf('font: height 250;'
		'alignment: horz  center, vert center;'
		'borders: left thin, right thin, top thin, bottom thin;')
	#设定列宽
	sheet.col(0).width = 2000  
	sheet.col(1).width = 2000
	sheet.col(2).width = 3333
	sheet.col(3).width = 3333
	sheet.col(4).width = 8888
	sheet.col(5).width = 2222


	sheet.row(0).height = ROW_HEIGHT
	sheet.write(0,0,'桌号', style)
	sheet.write(0,1,'赛号', style)
	sheet.write(0,2,'选手一', style)
	sheet.write(0,3,'选手二', style)
	sheet.write(0,4,'单位', style)
	sheet.write(0,5,'总得分', style)
	

	for i, desk in enumerate(game.get_ballot_result()):
		sheet.row(i*2+1).height = ROW_HEIGHT
		sheet.row(i*2+2).height = ROW_HEIGHT
		sheet.write_merge(i*2+1, i*2+2, 0, 0, str(desk.get_did()), style)
		for j, team in enumerate(desk.get_teams()):
			sheet.write(i*2+1+j, 1, team.get_no(), style)
			sheet.write(i*2+1+j, 2, team.get_p1(), style)
			sheet.write(i*2+1+j, 3, team.get_p2(), style)
			sheet.write(i*2+1+j, 4, team.get_cname(), style)
			sheet.write(i*2+1+j, 5, team.get_total_score(), style)

	wbk.save(filename)
	return filename
	