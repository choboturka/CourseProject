__author__ = 'Vlad'
import os
import xlrd
import csv
import pyautogui
#region constants
PATH = [r'E:\ZNO\ZNO2010',
        r'E:\ZNO\ZNO2011',
        r'E:\ZNO\ZNO2012',
        r'E:\ZNO\ZNO2013',
        r'E:\ZNO\ZNO2014']

test_path = ['E:\\ZNO\\test']

Y = 80
X11 = [400, 515, 600, 655, 700, 745, 781, 810, 990, 1080, 1170, 1260]
X12 = [320,460,540,600,640,690,750,830,930,1030,1110,1200,1300]
X13 = [250,380,460,530,570,620,680,760,860,950,1040,1130,1220,1300]

X_UKR, Y_UKR = 50,60
X_EXPORT, Y_EXPORT = 40, 40
X_END, Y_END = 70,710

test = [885]
NODES = 800 #800#800, 781, 787
PAUSE = 1.8
#endregion

def convert_all(p):
    for path in p:
        for filename in os.listdir(path):
            if '.xls' in filename: #and ',' in filename:
                csv_from_excel(path + '\\' + filename)

def csv_from_excel(name):
    wb = xlrd.open_workbook(name)
    sh = wb.sheet_by_index(0)
    your_csv_file = open(name[:-4] + '.csv', 'w', newline='')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_NONNUMERIC, quotechar='|')
    print(name)
    for rownum in range(sh.nrows): #  2,sh.rows):
        print(rownum)
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

def mine_exe(list):
    pyautogui.moveTo(40,40,pause=5)
    go_down = True
    for X in list:
        pyautogui.moveTo(X,Y)
        pyautogui.click(X,Y,button='left')
        if go_down:
            pyautogui.click(X_UKR,Y_UKR,button='left')
            for i in range(NODES):
                pyautogui.click(X_EXPORT,Y_EXPORT,button='left')
                pyautogui.press('enter')
                pyautogui.press('down', pause=PAUSE)
        else:
            pyautogui.click(X_END,Y_END,button='left')
            for i in range(NODES):
                pyautogui.click(X_EXPORT,Y_EXPORT,button='left')
                pyautogui.press('enter')
                pyautogui.press('up', pause=PAUSE)
        go_down = not go_down

if __name__ == '__main__':
    convert_all(test)