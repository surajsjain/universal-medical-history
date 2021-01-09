import xlwt
from datetime import datetime

'''

queryset_dict = {
    'sheet_1': queryset_1,
    'sheet_2': queryset_2,
    .
    .
    .
}

'''


def queryset_to_excel(queryset_dict, wb_name):
    workbook = xlwt.Workbook()

    sheet_names = list(queryset_dict.keys())

    for sheet_name in sheet_names:
        queryset = queryset_dict[sheet_name]
        sheet = workbook.add_sheet(sheet_name)

        if (len(queryset) != 0):
            write_queryset_to_sheet(queryset, sheet)

    workbook.save(wb_name)


def write_queryset_to_sheet(queryset, sheet):
    header_style = xlwt.easyxf('font:bold on')
    columns = []

    fields = queryset[0]._meta.fields

    i = 0

    for field in fields:
        col_name = field.name

        sheet.write(0, i, col_name, header_style)  # Writing headings
        columns.append(col_name)

        i = i + 1


    i = 1
    for query in queryset:
        skip_first = True
        j = 0
        for value in query.__dict__.values():

            if(type(value) == datetime):
                value = str(value.date()) + ' ' + str(value.time())

            if(skip_first):
                skip_first = False
                continue
            else:
                sheet.write(i, j, value)
                j = j + 1

        i = i +1