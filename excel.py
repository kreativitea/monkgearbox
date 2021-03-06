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


def write_data(filename, sheetname, data):
    ''' Opens the workbook, then the worksheet, then writes the data.'''
    try:
        workbook = excel.Workbooks.Open(filename)
    except Exception as e:
        print "Unable to instantiate workbook!"
        print repr(e)
        raise
    if not workbook:
        print "Unable to instantiate workbook!"
        raise IOError("Workbook not found.")

    try:
        sheet = get_sheet(sheetname)
    except Exception as e:
        print "Unable to instantiate worksheet!"
        print repr(e)
        raise
    if not sheet:
        print "Unable to instantiate worksheet!"
        raise IOError("Worksheet not found")

    for k, d in sorted(data.items()):
        # if there's no cell, there's no data to write
        if not d.cell:
            print ('{}: skipping value {}, no cell'
                   ''.format(ljust(k, 40, '.'), d.value))

        # otherwise, write something
        else:
            pass
            # if there's no value, reset the cell to zero
            if not d.value:
                print ('{}: writing to cell : {} : no value'
                       ''.format(ljust(k, 40, '.'), d.cell))
            # if there is, write the value to the cell
            else:
                print ('{}: writing to cell : {} : value {} '
                       ''.format(ljust(k, 40, '.'), d.cell, d.value))

            # excel com bound method
            sheet.Range(d.cell).Value = d.value

    excel.Visible = True


def get_sheet(sheet):
    ''' Given the name of a sheet, returns the sheet object. '''
    # for each sheet in the workbook,
    for s in range(1, excel.Sheets.Count + 1):
        # if the worksheet name matches the variable sheet,
        if excel.Sheets(s).Name == sheet:
            # return the sheet.
            return excel.Sheets(s)


def select_excel():
    excel_extensions = ('xlsx', 'xls', 'xlsm')
    try:
        # for each file in the directory
        # if the extension is of an excel type
        # and is not an office temporary workbook
        excel_sheets = [f for f in os.listdir(os.getcwd())
                        if f.endswith(excel_extensions)
                        and not f.startswith('~$')]

        # if there's only one sheet, use it.
        if len(excel_sheets) == 1:
            return os.path.join(os.getcwd(), excel_sheets[0])

        # if there's more than one, prompt the user to select one
        elif len(excel_sheets) > 1:
            print "Please select a toolbox sheet:"
            for i, v in enumerate(excel_sheets, 1):
                print '{}: {}'.format(i, v)

            while True:
                selection = raw_input('>>> ')
                try:
                    sheet = excel_sheets[int(selection)-1]
                    print 'attempting to load: {}'.format(sheet)
                    return os.path.join(os.getcwd(), sheet)
                except:
                    print "I'm sorry, that's not a valid selection."
    except IOError:
        raise IOError("Workbook not found")
    except Exception as e:
        print "Unable to instantiate workbook!"
        print "Exception raised: {}".format(repr(e))
