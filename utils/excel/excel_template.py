# -*- coding: utf-8 -*-
"""
excel_template.py
~~~~~~~~~~~~~~~~~

Utility module for exporting a dictionary of dataframes to excel tables, with each dataframe saved to a separate tab in the workbook. 


@Author: Jeff Maxey
"""

from __future__ import print_function

import pandas as pd
from datetime import date, time
from collections import OrderedDict

from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.worksheet import convert_cell_args
from typing import Optional
from xlsxwriter.worksheet import (
    Worksheet, cell_number_tuple, cell_string_tuple)

xlApp = win32com.client.Dispatch('Excel.Application') 
xlApp.Visible = True

def excel_string_width(str):
    """
    Calculate the length of the string in Excel character units. This is only
    an example and won't give accurate results. It will need to be replaced
    by something more rigorous.

    """
    string_width = len(str)

    if string_width == 0:
        return 0
    else:
        return string_width * 1.1

class xlSheet(Worksheet):
    """
    Subclass of the XlsxWriter Worksheet class to override the default
    write_string() method.

    """

    @convert_cell_args
    def write_string(self, row, col, string, cell_format=None):
        # Overridden write_string() method to store the maximum string width
        # seen in each column.

        # Check that row and col are valid and store max and min values.
        if self._check_dimensions(row, col):
            return -1

        # Set the min width for the cell. In some cases this might be the
        # default width of 8.43. In this case we use 0 and adjust for all
        # string widths.
        min_width = 0

        # Check if it the string is the largest we have seen for this column.
        string_width = excel_string_width(string)
        if string_width > min_width:
            max_width = self.max_column_widths.get(col, min_width)
            if string_width > max_width:
                self.max_column_widths[col] = string_width

        # Now call the parent version of write_string() as usual.
        return super(xlSheet, self).write_string(row, col, string,
                                                     cell_format)


class xlBook(Workbook):
    """
    Subclass of the XlsxWriter Workbook class to override the default
    Worksheet class with our custom class.

    """

    def add_worksheet(self, name=None):
        # Overwrite add_worksheet() to create a xlSheet object.
        # Also add an Worksheet attribute to store the column widths.
        worksheet = super(xlBook, self).add_worksheet(name, xlSheet)
        worksheet.max_column_widths = {}
        
        return worksheet

    def format_worksheet(self, name=None, lock_cells=False, hide_formulas=False, hide_gridlines=False):
        worksheet = super(xlBook, self).get_worksheet_by_name(name)

        # set worksheet tab color
        worksheet.set_tab_color('#808080')

        # set worksheet gridline property
        if hide_gridlines is True:
            worksheet.hide_gridlines(True)
        else:
            worksheet.hide_gridlines(False)

        # enable worksheet protection
        worksheet.protect(True)

        # define cell formats
        cell_format.set_font_name('Arial')
        cell_format.set_font_size(10)
        cell_format.set_font_color('black')
        cell_format.set_text_wrap(False)
        cell_format.set_bold(False)
        cell_format.set_align('left')
        cell_format.set_valign('top')
        
        if lock_cells is True:            
            cell_format.set_locked(True)
        else:
            cell_format.set_locked(False)

        if hide_formulas is True:
            cell_format.set_hidden(True)
        else:
            cell_format.set_hidden(False)

    def close(self):
        # We apply the stored column widths for each worksheet when we close
        # the workbook. This will override any other set_column() values that
        # may have been applied. This could be handled in the application code
        # below, instead.
        for worksheet in self.worksheets():
            for column, width in worksheet.max_column_widths.items():
                worksheet.set_column(column, column, width)
                
        return super(xlBook, self).close()

class objdict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

class xlObject(object):
    def __init__(self, *args, **kwargs):  
        self._attrs = OrderedDict(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(first, self).__setattr__(name, value)
        self._attrs[name] = value


        def get_column_width(worksheet: Worksheet, column: int) -> Optional[int]:
    """Get the max column width in a `Worksheet` column."""
    strings = getattr(worksheet, '_ts_all_strings', None)
    if strings is None:
        strings = worksheet._ts_all_strings = sorted(
            worksheet.str_table.string_table,
            key=worksheet.str_table.string_table.__getitem__)
    lengths = set()
    for row_id, colums_dict in worksheet.table.items():  # type: int, dict
        data = colums_dict.get(column)
        if not data:
            continue
        if type(data) is cell_string_tuple:
            iter_length = len(strings[data.string])
            if not iter_length:
                continue
            lengths.add(iter_length)
            continue
        if type(data) is cell_number_tuple:
            iter_length = len(str(data.number))
            if not iter_length:
                continue
            lengths.add(iter_length)
    if not lengths:
        return None
    return max(lengths)


def set_column_autowidth(worksheet: Worksheet, column: int):
    """
    Set the width automatically on a column in the `Worksheet`.
    """
    maxwidth = get_column_width(worksheet=worksheet, column=column)
    if maxwidth is None:
        return
    worksheet.set_column(first_col=column, last_col=column, width=maxwidth)


class xlTemplate(xlObject):
    def __init__(self, file_path='template.xlsx', 
                 title='Excel Template File.', subject='Input/Output/Analysis', 
                 author='Jeff A. Maxey', company=None, category=None, 
                 keywords=None, comments=None):        
        self.file_path = file_path
        self.title = title
        self.subject = subject
        self.author = author
        self.company = company 
        self.cateogry = category
        self.keywords = keywords
        self.comments = comments

        self.initialize_template()
        workbook.close()
        
    def initialize_template(self):
        self.create_wb()
        self.create_ws_about()
        # self.create_ws_toc()
        workbook.close()
              
    def create_wb(self):
        # create a new workbook
        self.workbook = workbook = Workbook(filename=self.name)     
        
        # set workbook properties        
        workbook.set_properties({
            'title': self.title,
            'subject': self.subject,
            'author': self.author,
            'company': self.company,
            'category': self.category,
            'keywords': self.keywords,
            'comments': self.comments
            })

        # define a header format
        header_format = workbook.add_format({
			'font_name': 'Arial',
			'font_size': 10,	
			'bold': True,
			'text_wrap': True,
			'valign': 'top',
			'align': 'left',
			'locked': True,
			'hidden': True
            })

        # define a cell format
        cell_format = workbook.add_format({
            	'font_name': 'Arial',
			'font_size': 10,	
			'bold': False,
			'text_wrap': False,
			'valign': 'top',
			'align': 'left',
			'locked': True,
			'hidden': True
            })
        

    def create_ws_about(self):
        ws = self.workbook.add_worksheet(name='About')
        ws.set_tab_color('black')
        
        row = 0
        for k, v in self._attrs.items():
            ws.write(row, 0, k+":", header_format)
            ws.write(row, 1, v, cell_format)
            row += 1
        for idx in range(0, 1):
            set_column_autowidth(worksheet=ws, column=idx)
            set_column_autowidth(worksheet=ws, column=idx)

        
    def create_ws_toc(self):
        ws = self.workbook.add_worksheet('Table of Contents')
        ws.set_tab_color('black')
        

template = xlTemplate()

def create_xl_template():
    workbook = Workbook('template.xlsx')
    

def write_dfs_to_xl_tables(xl_file, dfs):
    
	writer = pd.ExcelWriter(xl_file, engine='xlsxwriter')

    for df_name, df in dfs.items():
        # loop through `dict` of dataframes
        # write dataframe to excel sheet; disable index column
        df.to_excel(writer, sheet_name=df_name, index=False)
		# get xlsxwriter workbook and worksheet objects
		workbook = writer.book 
		worksheet = writer.sheets[df_name] 
		
        # enable worksheet protection
		worksheet.protect()
        
        #worksheet.set_tab_color('#808080')
        
        worksheet.hide_gridlines()
        worksheet.freeze_panes(1, 1)
        
		# add a header format
		header_format = workbook.add_format({
			'font_name': 'Arial',
			'font_size': 10	
			'bold': True,
			'text_wrap': True,
			'valign': 'top',
			'align': 'left',
			'locked': True
			'hidden': True
		})
        
     	# add a cell format 
		locked = workbook.add_format()
		locked.set_locked(True)
		unlocked = workbook.add_format()
		unlocked.set_locked(False)	
		hidden = workbook.add_format()
		hidden.set_hidden(True)
		unhidden = workbook.add_format()
		unhidden.set_hidden(False)
		
		# define table name

		table_name = 'tbl_'+df_name
        
        # create list of dicts for header names; columns property accepts {'header': value} as header name
		field_names = [{'header': field_name} for field_name in df.columns]

		# add table with coordinates: first row, first col, last row, last col; 
		# header names or formatting can be inserted into dict 
		worksheet.add_table(0, 0, df.shape[0], df.shape[1]-1, {'name'=table_name, 'columns': field_names, 'autofilter': False, 'style': 'Table Style Medium 20'})

		# Write the column headers with the defined format.
		for idx, value in enumerate(df.columns.values):
			worksheet.write(0, idx + 1, value, header_format)
		
		
		for idx, col in enumerate(df):  # loop through all columns
			series = df[col]
			max_len = max((
				series.astype(str).map(len).max(),  # len of largest item
				len(str(series.name))  # len of column name/header
				)) + 1  # pad with an additional space character
			worksheet.set_column(idx, idx, max_len)  # set column width
		

		
		
	# save writer object and created Excel file with data from DataFrame     
	writer.save()
