''' This file contains all the functions that directly manipulate excel. '''
import os
from string import ljust

# import com libraries
import win32com.client
try:
    if win32com.client.gencache.is_readonly is True:
        win32com.client.gencache.is_readonly = False
        win32com.client.gencache.Rebuild()
    excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
except Exception as e:
    print 'Unable to instantiate Excel.Application COM interface!'
    print repr(e)
    raise


def write_data(toolbox, data):
    ''' Opens the workbook, then the worksheet, then writes the data.'''
    try:
        workbook = excel.Workbooks.Open(toolbox)
    except Exception as e:
        print "Unable to instantiate workbook!"
        print repr(e)
        raise
    if not workbook:
        print "Unable to instantiate workbook!"
        raise IOError("Workbook not found.")

    try:
        sheet = get_sheet('Inputs')
    except Exception as e:
        print "Unable to instantiate worksheet!"
        print repr(e)
        raise
    if not sheet:
        print "Unable to instantiate worksheet!"
        raise IOError("Worksheet not found")

    for k, d in data.items():
        if d.cell:
            print ('{}: writing value {} to cell {}'
                   ''.format(ljust(k, 30), d.value, d.cell))
            sheet.Range(d.cell).Value = d.value
        else:
            print ('{}: skipping value {}, no cell'
                   ''.format(ljust(k, 30), d.value))
    excel.Visible = True


def get_sheet(sheet):
    for s in range(1, excel.Sheets.Count + 1):
        if excel.Sheets(s).Name == sheet:
            return excel.Sheets(s)


def select_excel():
    try:
        excel_sheets = [f for f in os.listdir(os.getcwd())
                        if f.endswith('xlsx')]

        if len(excel_sheets) == 1:
            return excel_sheets[0]

        else:
            print "Please select a toolbox sheet:"
            for i, v in enumerate(excel_sheets, 1):
                print '{}: {}'.format(i, v)

            while True:
                selection = raw_input('>>> ')
                try:
                    sheet = excel_sheets[int(selection)-1]
                    print 'attempting to load: {}'.format(sheet)
                    return sheet
                except:
                    print "I'm sorry, that's not a valid selection."

    except:
        print "Unable to instantiate workbook!"
        raise IOError("Workbook not found.")
