# -*- coding: utf-8 -*-
import tkFileDialog
import xlwt
from format import NLIST

ROW_HEIGHT = 500

def export_all_info(game):
	filename = tkFileDialog.asksaveasfilename(initialdir = './', defaultextension='.xls',  initialfile='比赛汇总' )
	wbk = xlwt.Workbook(encoding='utf-8')
	sheet = wbk.add_sheet('比赛汇总')

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
	for index, item in enumerate(NLIST):
		sheet.write(0, index, item , style)
	stageno = game.get_stageno()
	for i in range(stageno):
		 sheet.write(0, len(NLIST) + i*3, '第%d轮对手' % (i+1) ,style)
		 sheet.write(0, len(NLIST) + i*3 + 1, '第%d轮积分' % (i+1) ,style)
		 sheet.write(0, len(NLIST) + i*3 + 2, '第%d轮级差' % (i+1) ,style)

	sheet.write(0, len(NLIST) + stageno*3, '总大分' ,style)
	sheet.write(0, len(NLIST) + stageno*3 + 1, '总小分',style)
	sheet.write(0, len(NLIST) + stageno*3 + 2, '总级差',style)
	for i, t in enumerate(game.get_teams_order_by_no()):
		sheet.write(i + 1, 0, t.get_no() , style)
		sheet.write(i + 1, 1, t.get_tid() , style)
		sheet.write(i + 1, 2, t.get_p1() , style)
		sheet.write(i + 1, 3, t.get_p2() , style)
		sheet.write(i + 1, 4, t.get_cname() , style)

		for j in range(stageno):
			r =  t.get_record(j)
			a = t.get_against(j)
			sheet.write(i + 1, j*3 + 5, a.get_no(),style)
		 	sheet.write(i + 1, j*3 + 6, r.get_score(),style)
		 	sheet.write(i + 1, j*3 + 7, r.get_diff() ,style)

		sheet.write(i + 1, len(NLIST) + stageno*3, t.get_total_score() ,style)
		sheet.write(i + 1, len(NLIST) + stageno*3 + 1, t.get_total_sscore() ,style)
		sheet.write(i + 1, len(NLIST) + stageno*3 + 2, t.get_total_diff() ,style)

	wbk.save(filename)
	return filename