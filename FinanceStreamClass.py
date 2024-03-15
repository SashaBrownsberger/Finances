import numpy as np
import cantrips as can
import os
import datetime
import matplotlib.pyplot as plt
import scipy
import ImportDownloadedCSVFile as icsv
import FinancialShorthandToID as fsh

class FinanceStream:

    def getSpendingInterpolator(self, n_days_avg = 7, description_strings_to_ignore = ['payment', 'pymt',]):
        data_stream = self.data_stream
        indeces_to_ignore = [i for i in range(len(data_stream[0])) if np.any([str_to_ignore in data_stream[1][i].lower() for str_to_ignore in description_strings_to_ignore]) ]
        spending_indeces = [i for i in range(len(data_stream[0])) if (int(data_stream[4][i]) == 1 and not(i in indeces_to_ignore))]
        spending_dates = [data_stream[0][i] for i in spending_indeces]
        spending = [data_stream[3][i] for i in spending_indeces]
        spending_dates, spending = can.safeSortOneListByAnother(spending_dates, [spending_dates, spending])
        spending_delta_days = [(datetime.datetime.strptime(str(date), self.date_format_string) - self.start_date).days  for date in spending_dates]
        min_spending_delta_days, max_spending_delta_days = [min(spending_delta_days), max(spending_delta_days)]
        binned_spending_windows = ( can.niceReverse([[-(i + 1) * n_days_avg, -i * n_days_avg] for i in range(max(0, int(np.floor(-max_spending_delta_days/n_days_avg))), int(max(0, np.ceil(-min_spending_delta_days/n_days_avg)))) ])
        + [[i * n_days_avg, (i + 1) * n_days_avg] for i in range(max(0, int(np.floor(min_spending_delta_days/n_days_avg))), int(max(0, np.ceil(max_spending_delta_days/n_days_avg)))) ] )
        binned_spending_windows[0] = [spending_delta_days[0], binned_spending_windows[0][1]]
        binned_spending_windows[-1] = [binned_spending_windows[-1][0], spending_delta_days[-1]]
        spending_window_centers = [sum(window) / 2 for window in binned_spending_windows]
        n_windows = len(binned_spending_windows)
        binned_spending = [0.0 for i in range(n_windows)]
        #balances = [data_stream[3][i] for i in range(len(data_stream[0])) if int(data_stream[4][i]) == 0]
        current_window_index = 0
        for i in range(len(spending_dates)) :
            spending_on_date = spending [i]
            spending_date = spending_delta_days[i]
            finding_bin = 1
            while(finding_bin):
                if current_window_index >= len(binned_spending_windows):
                    binned_spending[-1] = binned_spending[-1] + spending_on_date
                    finding_bin = 0
                else:
                    current_window = binned_spending_windows[current_window_index]
                    if spending_date >= current_window[0] and spending_date < current_window[1]:
                        finding_bin = 0
                        binned_spending[current_window_index] = binned_spending[current_window_index] + spending_on_date
                    else:
                        current_window_index = current_window_index + 1
        binned_spending_per_day = [binned_spending[i] / (binned_spending_windows[i][1] - binned_spending_windows[i][0]) for i in range(len(binned_spending))]
        spending_interpolator = scipy.interpolate.interp1d(spending_window_centers, binned_spending_per_day, fill_value = (0,0), bounds_error = False)
        return [[spending_window_centers, binned_spending_per_day], spending_interpolator]

    def getBalanceInterpolator(self):
        data_stream = self.data_stream
        balance_dates = [data_stream[0][i] for i in range(len(data_stream[0])) if int(data_stream[4][i]) == 0]
        balance_delta_days = [(datetime.datetime.strptime(str(date), self.date_format_string) - self.start_date).days  for date in balance_dates]
        balances = [data_stream[3][i] for i in range(len(data_stream[0])) if int(data_stream[4][i]) == 0]
        if len(balances) < 2:
            print ('We have less than two balance entries, and so we cannot interpolate balances over time')
            return 0
        #plt.scatter(balance_delta_days, balances)
        #plt.xlabel(r'$\Delta$ days')
        #plt.ylabel('Balance ($)')
        #plt.show()
        balance_interpolator = scipy.interpolate.interp1d(balance_delta_days, balances, fill_value = (0,0), bounds_error = False)
        return [[balance_delta_days, balances], balance_interpolator]

    def saveStreamFile(self, header = 'Default', delimiter = 'Default'):
        if header in ['Default', 'default']:
            header = self.file_header
        if delimiter in ['Default', 'default']:
            delimiter = self.delimiter
        columns = self.data_stream
        can.saveListsToColumns(columns, self.file_path, '', sep = delimiter, append = False, header = header, type_casts = [int, str, str, float, int])
        return 1


    def loadStreamFile(self, delimiter = 'Default'):
        if delimiter in ['Default', 'default']:
            delimiter = self.delimiter
        if not(os.path.exists(self.file_path)):
            self.data_stream = [[], [], [], [], []]
            self.saveStreamFile( delimiter = delimiter )
        data = can.readInColumnsToList(self.file_path, file_dir = '', n_ignore = 1, n_ignore_end = 0, delimiter = delimiter, verbose = 0, remove_redundant_delimiter = 0)
        if len(data) > 0:
            dates = data[0]
            dates = [int(date) for date in dates]
            balances = data[3]
            balances = [float(balance) for balance in balances]
            descriptions = data[1]
            categories = data[2]
            adjustment_flags = data[4]
        else:
            dates, descriptions, categories, balances, adjustment_flags = [[], [] ,[], [], []]
        return [dates, descriptions, categories, balances, adjustment_flags]

    #def updateDataStream(self):
    #    updated = ( self.updateDataStreamByHand() or self.updateDataStreamFromFile() )
    #    return updated

    def updateDataStreamByHand(self):
        today = datetime.date.today()
        today_str = today.strftime(self.date_format_string)
        date_not_updated = 1
        while date_not_updated:
            date_input = can.getUserInputWithDefault('What is the date for this updated data stream formatted YYYYMMDD? (Default: ' + today_str + '): ', today_str)
            if len(date_input) == 8 and date_input.isdigit():
                date_input = int(date_input)
                if date_input in self.data_stream[0]:
                    add_same_day = can.getUserInputWithDefault('The date ' + str(date_input) + ' already has an entry in this finance stream.  Do you want to add another? (Default: no): ', 'no')
                    if add_same_day.lower() in ['y', 'yes']:
                        date_not_updated = 0
                else:
                    date_not_updated = 0
            else:
                print ('The value entered here must be either an eight digit date string formatted as YYYYMMDD.   Try entering again? ')
        description_str = can.getUserInputWithDefault("What is the description of this line (e.g. Balance, Payment, etc)? (Default: ''): " , '')
        category_str = can.getUserInputWithDefault("What is the category description of this line (e.g. Balance, Food, Games, etc)? (Default: ''): " , '')
        balance_not_updated = 1
        while balance_not_updated:
            balance_str = can.getUserInputWithDefault('What is the balance or balance change (remember that credit card charges and balances should be entered as NEGATIVE)? (Default: 0): ' , '0')
            balance_not_updated = 0
            try:
                balance = float(balance_str)
            except ValueError:
                balance_not_updated = 1
                print ('I could not print the entered string: ' + balance_str + ' to a float.  Try entering again?')
        balance_not_flagged = 1
        while balance_not_flagged:
            balance_or_change = can.getUserInputWithDefault('Is the value you provided a balance (then enter 0) or a change to a balance (then enter 1)? (Default: 0): '  , '0')
            if balance_or_change in ['0','1']:
                balance_flag = int(balance_or_change)
                balance_not_flagged = 0
            else:
                print ('The value entered here must be either 0 or 1, each single-character strings.   Try entering again? ')
        #self.data_stream = [self.data_stream[0] + [date_input], self.data_stream[1] + [balance], self.data_stream[2] + [balance_flag]]

        self.data_stream = [self.data_stream[0] + [date_input], self.data_stream[1] + [description_str], self.data_stream[2] + [category_str], self.data_stream[3] + [balance], self.data_stream[4] + [balance_flag]]
        self.data_stream = can.safeSortOneListByAnother(self.data_stream[0], self.data_stream)
        return 1

    def updateDataStreamFromFile(self, compiled_data_suffix = '_COMPILED.csv', data_dir = 'Data/', default = 'NewData.csv'):
        csv_file = can.getUserInputWithDefault('Enter the name of the data file to be added into the total data for stream ' + self.stream_name + ' (default: ' + default + '): ', default)
        success = icsv.addFileToStreamHistory(csv_file, self.stream_name, compiled_data_suffix = compiled_data_suffix, data_dir = data_dir, delimiter = self.delimiter)
        self.data_stream = self.loadStreamFile()
        self.data_stream = can.safeSortOneListByAnother(self.data_stream[0], self.data_stream)
        return success

    def __init__(self, stream_name, data_dir,
                update_on_start = 1, delimiter = ', ', stream_file_header = ['Date (YYYYMMDD), Description, Category, Value($), Balance (0) or Adjustment (1)'], date_format_string = '%Y%m%d', start_date_str = '20221101',
                raw_source_suffix = '_RAW.csv', compiled_data_suffix = '_COMPILED.csv', temp_file_name = 'TEMP.csv'):
        self.delimiter = delimiter
        self.file_header = stream_file_header
        print ('stream_name = ' + str(stream_name))
        self.stream_name = fsh.getFinancialStreamIDsFromShorthand(stream_name)
        print ('self.stream_name = ' + str(self.stream_name))
        self.file_path = data_dir + self.stream_name + compiled_data_suffix
        self.date_format_string = date_format_string
        self.start_date_str = start_date_str
        self.start_date = datetime.datetime.strptime(str(start_date_str), self.date_format_string)
        self.data_stream = self.loadStreamFile(delimiter = delimiter )
        if update_on_start:
            update_done = self.updateDataStreamFile()
        else:
            update_done = 0

        #self.balance_interpolator = self.getBalanceInterpolator( )
        #self.spending_interpolator = self.getSpendingInterpolator( )
