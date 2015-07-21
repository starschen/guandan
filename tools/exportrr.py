# -*- coding: utf-8 -*-
from Tkinter import * 
import tkFileDialog
import xlwt

ROW_HEIGHT = 500
def export_round_record(game):
    filename = tkFileDialog.asksaveasfilename(initialdir = './', defaultextension='.xls',  initialfile='第%d轮比赛记录表' % (game.get_stageno() + 1))
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('扑克牌掼蛋比赛记分表')
    
    sheet.set_row_default_height(ROW_HEIGHT)
    #设定列宽
    sheet.col(0).width = 1111  #赛号
    sheet.col(1).width = 3333  #姓名
    sheet.col(2).width = 3333  #单位 
    sheet.col(19).width = 1111  #级差
    for i in range(16):
        sheet.col(i+3).width = 999

    #设定字体
    al = xlwt.Alignment()  
    al.horz = xlwt.Alignment.HORZ_CENTER  
    al.vert = xlwt.Alignment.VERT_CENTER  
    font = xlwt.Font() 
    font.bold = True
    font.height = 300
    borders = xlwt.Borders() # Create Borders
    borders.left = xlwt.Borders.THIN# May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    title_style = xlwt.XFStyle() 
    title_style.font = font
    title_style.alignment = al
    border_style = xlwt.XFStyle() 
    border_style.borders = borders

    #写入内容
    rows_every_desk = 10
    for i, desk in enumerate(game.get_ballot_result()):
        for no in range(10):
            sheet.row(i*10+no).height = ROW_HEIGHT

        #第一行标题
        sheet.write_merge(rows_every_desk*i, rows_every_desk*i, 0, 19, game.config.get_title(), title_style)
        #第二行
        sheet.write(rows_every_desk*i + 1, 1, '第%d轮' % (game.get_stageno()  + 1))
        sheet.write_merge(rows_every_desk*i + 1, rows_every_desk*i + 1,  3,  5, '时间：')
        sheet.write_merge(rows_every_desk*i + 1, rows_every_desk*i + 1, 6, 13, game.config.get_time())
        sheet.write_merge(rows_every_desk*i + 1, rows_every_desk*i + 1, 14, 15, '桌号')
        sheet.write_merge(rows_every_desk*i + 1, rows_every_desk*i + 1, 16, 18, '第%d桌' % desk.get_did())
        #第三行
        sheet.write(rows_every_desk*i + 2, 0, '赛号', border_style)
        sheet.write(rows_every_desk*i + 2, 1, '姓名', border_style)
        sheet.write(rows_every_desk*i + 2, 2, '单位', border_style)
        for num in range(16):
            sheet.write(rows_every_desk*i + 2, num + 3, str(num +1),  border_style)
        sheet.write(rows_every_desk*i + 2, 19, '级差', border_style)
        #第四-七行
        for j, team in enumerate(desk.get_teams()):
                sheet.write_merge(rows_every_desk*i + j*2 + 3, rows_every_desk*i + j*2 + 4,  0, 0, team.get_no(), border_style)
                sheet.write_merge(rows_every_desk*i  + j*2 + 3, rows_every_desk*i + j*2 + 4, 1, 1, team.get_p1()+'/'+team.get_p2(), border_style)
                sheet.write_merge(rows_every_desk*i  + j*2 + 3, rows_every_desk*i + j*2 + 4, 2, 2, team.get_cname(), border_style)
                for x in range(3, 20):
                    sheet.write(rows_every_desk*i + j*2 + 3, x, '', border_style)
                    sheet.write(rows_every_desk*i + j*2 + 4, x, '', border_style)
        #第八行
        sheet.write_merge(rows_every_desk*i + 7, rows_every_desk*i + 7,  0, 1, '胜方签字：')
        sheet.write_merge(rows_every_desk*i + 7, rows_every_desk*i + 7,  6, 8, '负方签字：')
        sheet.write_merge(rows_every_desk*i + 7, rows_every_desk*i + 7,  9, 11, '')
        sheet.write_merge(rows_every_desk*i + 7, rows_every_desk*i + 7, 12, 16,  '裁判员：')
        sheet.write_merge(rows_every_desk*i + 7, rows_every_desk*i + 7, 17,  18,  '胜方画圈')
        #第九行
        sheet.write_merge(rows_every_desk*i + 8,  rows_every_desk*i + 8, 0,  1, '违例警告说明：')

    wbk.save(filename)
    return filename
