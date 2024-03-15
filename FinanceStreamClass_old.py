import numpy as np
import cantrips as can
import os
import datetime
import matplotlib.pyplot as plt
import scipy

class FinanceStream:

    def getSpendingInterpolator(self):
        data_stream = self.data_stream
        balance_dates = [data_stream[0][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 0]
        balance_delta_days = [(datetime.datetime.strptime(str(date), self.date_format_string) - self.start_date).days  for date in balance_dates]
        window_widths = [balance_delta_days[i] - balance_delta_days[i-1] for i in range(1, len(balance_delta_days) ) ]
        window_centers = [(balance_delta_days[i] + balance_delta_days[i-1]) / 2 for i in range(1, len(balance_delta_days) ) ]
        adjustment_dates = [data_stream[0][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 1]
        adjustment_delta_days = [(datetime.datetime.strptime(str(date), self.date_format_string) - self.start_date).days  for date in adjustment_dates]
        balances = [data_stream[1][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 0]
        adjustments = [data_stream[1][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 1]
        if len(balances) < 3:
            print ('We have less than three balance entries, and so we cannot interpolate spending over time')
            return 0
        balance_changes = [balances[i] - balances[i-1] for i in range(1, len(balances) ) ]
        adjustments_in_windows = [sum([adjustments[j] for j in range(len(adjustments)) if adjustment_delta_days[j] > balance_delta_days[i-1] and adjustment_delta_days[j] <= balance_delta_days[i] ])
                                        for i in range(1, len(balances) ) ]
        spending_in_windows = [balance_changes[i] - adjustments_in_windows[i] for i in range(len(balance_changes))]
        spending_rates = [spending_in_windows[i] / window_widths[i] * 30 for i in range(len(spending_in_windows))]
        #plt.scatter(window_centers, spending_rates , c = 'g')
        #plt.xlabel(r'$\Delta$ days')
        #plt.ylabel('Spending rate ($ / 30 days)')
        #plt.show()
        spending_interpolator = scipy.interpolate.interp1d(window_centers, spending_rates, fill_value = (0,0), bounds_error = False)
        return [[window_centers, spending_rates], spending_interpolator]

    def getBalanceInterpolator(self):
        data_stream = self.data_stream
        balance_dates = [data_stream[0][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 0]
        balance_delta_days = [(datetime.datetime.strptime(str(date), self.date_format_string) - self.start_date).days  for date in balance_dates]
        balances = [data_stream[1][i] for i in range(len(data_stream[0])) if data_stream[2][i] == 0]
        if len(balances) < 2:
            print ('We have less than two balance entries, and so we cannot interpolate balances over time')
            return 0
        #plt.scatter(balance_delta_days, balances)
        #plt.xlabel(r'$\Delta$ days')
        #plt.ylabel('Balance ($)')
        #plt.show()
        balance_interpolator = scipy.interpolate.interp1d(balance_delta_days, balances, fill_value = (0,0), bounds_error = False)
        return balance_interpolator

    def saveStreamFile(self, header = 'Default', delimiter = 'Default'):
        if header in ['Default', 'default']:
            header = self.file_header
        if delimiter in ['Default', 'default']:
            delimiter = self.delimiter
        columns = self.data_stream
        can.saveListsToColumns(columns, self.file_path, '', sep = delimiter, append = False, header = header, type_casts = [int, float, int])
        return 1


    def loadStreamFile(self, delimiter = 'Default'):
        if delimiter in ['Default', 'default']:
            delimiter = self.delimiter
        if not(os.path.exists(self.file_path)):
            self.data_stream = [[], [], []]
            self.saveStreamFile( delimiter = delimiter )
        data = can.readInColumnsToList(self.file_path, file_dir = '', n_ignore = 1, n_ignore_end = 0, delimiter = delimiter, verbose = 0)
        if len(data) > 0:
            dates = data[0]
            dates = [int(date) for date in dates]
            balances = data[1]
            balances = [float(balance) for balance in balances]
            adjustment_flags = data[2]
            adjustment_flags = [int(flag) for flag in adjustment_flags]
        else:
            dates, balances, adjustment_flags = [[], [] ,[] ]
        return [dates, balances, adjustment_flags]

    def updateDataStream(self):
        input = str(can.getUserInputWithDefault('Do you want to update the finance stream: ' + self.stream_name + '? (Default: no): ', 'no'))
        if input.lower() in ['yes', 'y']:
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

            balance_not_updated = 1
            while balance_not_updated:
                balance_str = can.getUserInputWithDefault('What is the balance or balance change? (Default: 0): ' , '0')
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
            self.data_stream = [self.data_stream[0] + [date_input], self.data_stream[1] + [balance], self.data_stream[2] + [balance_flag]]
            self.data_stream = can.safeSortOneListByAnother(self.data_stream[0], self.data_stream)
            return 1
        else:
            print('Not updating finance stream: ' + self.stream_name)
            return 0


    def __init__(self, stream_name, data_dir,
                update_on_start = 1, file_suffix = '.txt', delimiter = ',', stream_file_header = ['Date (YYYYMMDD), Value($), Balance (0) or Transaction(1)'], date_format_string = '%Y%m%d', start_date_str = '20221101'):
        self.delimiter = delimiter
        self.file_header = stream_file_header
        self.file_path = data_dir + stream_name + file_suffix
        self.stream_name = stream_name
        self.date_format_string = date_format_string
        self.start_date_str = start_date_str
        self.start_date = datetime.datetime.strptime(str(start_date_str), self.date_format_string)
        self.data_stream = self.loadStreamFile(delimiter = delimiter )
        if update_on_start:
            update_done = self.updateDataStream()
        else:
            update_done = 0
        if update_done:
            self.saveStreamFile(delimiter = delimiter )
        self.balance_interpolator = self.getBalanceInterpolator( )
        self.spending_interpolator = self.getSpendingInterpolator( )
