import numpy as np
import matplotlib.pyplot as plt
import os
import cantrips as can
import FinancialTools as ft

class MonthlyExpenditures:

    def calculateDifferences(self):
        if len(self.totals) == 0:
            self.sumExpenditures(print = 0)
        flags = self.flags
        differences = {}
        for flag in self.flags:
            actual = self.totals[flag]
            expected = self.expected[flag]
            differences[flag] = actual - expected
        self.differences = differences
        return 1

    def printTotals(self):
        print ('Here are our totals for ' + self.name + ': ')
        for flag in self.flags.keys():
            print (self.flags[flag] + ' => ' + str(round(self.totals[flag], 2)))
        return 1

    def sumDifferences(self, pnt = 1):
        n_expenditures = len(self.expenditures[self.keys[0]])
        overall_total = 0
        self.overall_diff = sum([self.differences[flag] for flag in self.expected.keys()])
        if pnt:
            self.printTotals()
        #print (' ')
        return 1

    def sumExpenditures(self, print = 1):
        n_expenditures = len(self.expenditures[self.keys[0]])
        overall_total = 0
        for flag in self.flags.keys():
            total = sum([self.expenditures[self.keys[1]][i] for i in range(n_expenditures) if self.expenditures[self.keys[2]][i] == flag])
            self.totals[flag] = total
            overall_total = overall_total + total
        self.overall_total = overall_total
        if print:
            self.printTotals()
        #print (' ')
        return 1

    def saveExpenditures(self, data_dir = None, file_name = None, append = True, header = None):
        if file_name == None:
            file_name = self.file_name
        if data_dir == None:
            data_dir = self.data_dir
        if header == None:
            header = ','.join(self.header)
        cols = [self.expenditures[key] for key in self.keys]
        can.saveListsToColumns(cols, file_name, data_dir, sep = ',', append = append)
        print ('Expenditures saved to: ' + data_dir + file_name)
        return 1

    def readInExpectations(self, data_dir = None, file_name = None):
        if file_name == None:
            file_name = self.expectations_file_name
        if data_dir == None:
            data_dir = self.data_dir
        expected = {}
        for flag in self.flags:
            expected[flag] = 0.0
        if  os.path.isfile(data_dir + file_name):
            print ("Let's read in the expected expenditures from: " + data_dir + file_name)
            cols = can.readInColumnsToList(file_name, file_dir = data_dir, n_ignore = self.n_header_lines, verbose = 0, delimiter = ',')
            if len(cols) != 2:
                #if data is not properly formatted, this block will catch it.
                for i in range(len(cols)):
                    row = cols[i]
                    if len(row) != 2:
                        print ('Row ' + str(i) + ' is not properly formatted: ')
                        print (row)
            else:
                if len(cols) > 0:
                    for i in range(len(cols[1])):
                        try:
                            cols[1][i] = float(cols[1][i])
                        except ValueError:
                            print ('Following value at row ' + str(i) + ' could not be converted to a float: ' + cols[1][i])
                        cols[1][i] = float(cols[1][i])
                    cols[1] = [float(val) for val in cols[1]]
                    for i in range(len(cols[0])):
                        category = cols[0][i]
                        if category in self.exp_categories:
                            flag = [ flag for flag in self.flags if self.flags[flag] == category ][0]
                            expected[flag] = cols[1][i]
                        else:
                            print ('Expenditure category ' + category + ' in expected expenditues file not recognized.  Check spelling, and maybe update known expenditues category at: ' + self.flags_file)
                            expected[category] = cols[1][i]

                else:
                    for i in range(len(self.flags)):
                        expected[self.keys[i]] = []

            print ('Expected expenditures read in from file: ' + data_dir + file_name)
        else:
            print ('Could not find expected expenditures: ' + data_dir + file_name)
        return expected

    def readInExpenditures(self, data_dir = None, file_name = None, base_on_expected = 1):
        if file_name == None:
            file_name = self.file_name
        if data_dir == None:
            data_dir = self.data_dir
        if  os.path.isfile(data_dir + file_name):
            print ('Reading in expenditures from file: ')
            print (data_dir + file_name)
            cols = can.readInColumnsToList(file_name, file_dir = data_dir, n_ignore = self.n_header_lines, verbose = 0, delimiter = ',')
            if len(cols) != 4:
                print ('len(cols) = ' + str(len(cols)))
                #if data is not properly formatted, this block should catch it.
                for  i in range(len(cols)):
                    row = cols[i]
                    if len(row) != 4:
                        print ('Row ' + str(i) + ' is not properly formatted: ')
                        print (row)
                for i in range(len(self.keys)):
                    self.expenditures[self.keys[i]] = []
            else:
                if len(cols) > 0:
                    for i in range(len(cols[1])):
                        try:
                            cols[1][i] = float(cols[1][i])
                        except ValueError:
                            print ('Following value at row ' + str(i) + ' could not be converted to a float: ' + cols[1][i])
                        cols[1][i] = float(cols[1][i])
                    cols[1] = [float(val) for val in cols[1]]
                    for i in range(len(self.keys)):
                        self.expenditures[self.keys[i]] = cols[i]
                else:
                    for i in range(len(self.keys)):
                        self.expenditures[self.keys[i]] = []

            print ('Expenditures read in from file: ' + data_dir + file_name)

        elif base_on_expected:
            print ('Could not find expenditures file: ' + data_dir + file_name)
            print ('Reading in data from expectations file. ')
            expectations = self.readInExpectations()
            expectation_keys = list(expectations.keys())
            n_expenditures = len(expectation_keys)
            self.expenditures = { 'Days':['1' for i in range(n_expenditures)],
                                  'Values':[expectations[key] for key in expectation_keys],
                                  'Flags':expectation_keys,
                                  'Account':['EXPECT' for key in expectation_keys]  }
        else:
            print ('Expenditures file: ' + data_dir + file_name + ' does not appear to exist yet. Making empty expenditures dictionary....')
            for i in range(len(self.keys)):
                self.expenditures[self.keys[i]] = []
            can.saveListsToColumns([[elem] for elem in self.header], file_name, data_dir, sep = ',' )
        return 1

    def addInExpenditures(self, ):
        print ("Let's start reading in expenditures: ")
        prev_date = 'NONE ENTERED'
        prev_val = -999
        prev_flag = 'NO FLAG'
        prev_account = 'NO ACCOUNT'
        new_dates = []
        new_vals = []
        new_flags = []
        new_accounts = []
        more_to_add = 1
        while (more_to_add):
            date_str = 'DUMMY'
            while date_str.lower() != 'done' and len(date_str) != 8:
                date_str = input('Enter the expenditure date as YYYYMMDD (Default: ' + prev_date + '; enter DONE if done entering transactions): ')
                if len(date_str) == 0:
                    date_str = prev_date
                if date_str.lower() != 'done' and len(date_str) != 8:
                    print ('You must enter the date of the expenditure as a string in the format: YYYYMMDD.  Try again please :)')
            if date_str.lower() != 'done':
                valid_value = 0
                while not(valid_value):
                    val_str = input('Enter the expenditure amount as a number (Default: ' + str(prev_val) + '): ')
                    if len(val_str) == 0:
                        val_str = str(prev_val)
                    try:
                        val = float(val_str)
                        valid_value = 1
                    except ValueError:
                        print ("Entered value could not be converted to a float.  Please try again :)" )
                valid_flag = 0
                while not(valid_flag):
                    flag_str = input('Enter the flag for this expenditure (Default: ' + prev_flag + '; enter ? to see a list of valid flags): ')
                    if len(flag_str) == 0:
                        flag_str = prev_flag
                    if flag_str.upper() in self.flags.keys() :
                        flag = flag_str
                        valid_flag = 1
                    elif flag_str == '?':
                        self.printExpenditureFlags()
                    else:
                        print ("Entered value was not in list of valid flags.  Please try again :)" )
                valid_account = 0
                while not(valid_account):
                    account_str = input('Enter the account for this expenditure (Default: ' + prev_account + '; enter ? to see a list of valid accounts): ')
                    if len(account_str) == 0:
                        account_str = prev_account
                    if account_str.upper() in self.accounts.keys() :
                        account = account_str
                        valid_account = 1
                    elif account_str == '?':
                        self.printExpenditureAccounts()
                    else:
                        print ("Entered value was not in list of valid accounts.  Please try again :)" )
                new_dates = new_dates + [date_str]
                new_vals = new_vals + [val]
                new_flags = new_flags + [flag_str]
                new_accounts = new_accounts + [account_str]
                print ('Added following expenditure: ')
                print (new_dates[-1] + ', ' + str(new_vals[-1]) + ', ' + new_flags[-1] + ', ' + new_accounts[-1])
                prev_date = date_str
                prev_val = val
                prev_flag = flag_str
                prev_account = account_str
            else:
                more_to_add = 0
        expend_keys = self.keys
        new_data = [new_dates, new_vals, new_flags, new_accounts]
        for i in range(len(expend_keys)):
            self.expenditures[expend_keys[i]] = self.expenditures[expend_keys[i]] + new_data[i]

        return 1

    def printExpenditureAccounts(self):
        print ('Here are the account keys, and what they correspond to: ')
        for key in self.accounts.keys():
            print (key + ' => ' + self.accounts[key])
        return 1

    def printExpenditureFlags(self):
        print ('Here are the expenditure flags, and what they correspond to: ')
        for key in self.flags.keys():
            print (key + ' => ' + self.flags[key])
        return 1

    def readInAbbreviationFile(self, dir, file_name):
       cols = can.readInColumnsToList(file_name, file_dir = dir, n_ignore = 0, delimiter =',')
       abbreviations = cols[0]
       meanings = cols[1]
       print ('abbreviations = ' + str(abbreviations))
       print ('meanings = ' + str(meanings))
       dict = {}
       n_elems = len(abbreviations)
       for i in range(n_elems):
           dict[abbreviations[i]] = meanings[i]
       return dict

    def __init__(self, name, specified_file_name = None, expectations_file_name = None,
                file_name_prefix = '', file_name_suffix = '_expenditures.csv', expected_file_name_suffix = '_expectations.csv',
                data_dir = '/Users/sashabrownsberger/Documents/Finances/MonthlyFinances/',
                n_header_lines = 1, header = ['Days', 'Values', 'Flags', 'Account'],
                accounts_file = 'AccountAbbreviations.csv', flags_file = 'FlagAbbreviations.csv',
                ):

        print ('Name = ' + str(name))
        self.name = name
        self.keys = header
        self.header = header
        if specified_file_name == None:
            self.file_name = file_name_prefix + self.name + file_name_suffix
        else:
            self.file_name = specified_file_name
        if expectations_file_name == None:
            self.expectations_file_name = file_name_prefix + self.name + expected_file_name_suffix
        else:
            self.expectations_file_name = expectations_file_name
        self.data_dir = data_dir
        self.expenditures = {}
        self.expected = {}
        self.n_header_lines = n_header_lines
        self.accounts, self.account_colors = ft.readInAbbreviationFile(data_dir, accounts_file)
        self.flags, self.flag_colors = ft.readInAbbreviationFile(data_dir, flags_file)
        print ('self.flags = ' + str(self.flags))
        self.accounts_file, self.flags_file = [accounts_file, flags_file]
        self.exp_categories = [ self.flags[flag] for flag in self.flags.keys() ]
        self.readInExpenditures()
        self.expected = self.readInExpectations()
        print(self.expected)
        keys = header

        self.totals = {}
        self.overall_total = 0.0
        self.overall_diff = 0.0
