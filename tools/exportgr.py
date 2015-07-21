# -*- coding: utf-8 -*-
from Tkinter import * 
import tkFileDialog
import xlwt

def export_group_rank(game):  
    filename = tkFileDialog.asksaveasfilename(initialdir = './', defaultextension='.xls',  initialfile='团体排名')
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('团体排名')
    header = ['排名', '单位编号', '单位名称', '总大分', '总小分', '总级差']
    for index, item in enumerate(header):
        sheet.write(0, index, header[index])
    companys = game.company_rank()
    for index, item in enumerate(companys):
        sheet.write(index+1, 0, index+1)
        sheet.write(index+1, 1, item.get_scname())
        sheet.write(index+1, 2, item.get_cname())
        sheet.write(index+1, 3, item.get_total_score())
        sheet.write(index+1, 4, item.get_total_sscore())
        sheet.write(index+1, 5, item.get_total_diff())

    wbk.save(filename)
    return filename