import MonthlyExpendituresClass as mec
import matplotlib.pyplot as plt
import FinancialTools as ft
import numpy as np
import cantrips as can
import sys

class Finances:

    def plotAllFinances(self, figsize  = (16, 10) ):
        f, axarr = plt.subplots(2,2, figsize = figsize)
        ax00 = axarr[0,0]
        ax10 = axarr[1,0]
        ax01 = axarr[0,1]
        ax11 = axarr[1,1]
        self.plotFinancesByCategoary(ax = ax00, show = 0, legend = 0)
        self.plotDifferencesByCategory(ax = ax10, show = 0, legend = 0)
        self.plotTotalDifferences(ax = ax01, show = 0, legend = 0)
        bars = self.plotTotalFinances(ax = ax11, show = 0, legend = 0)
        f.legend(bars, ['Starting'] + [self.flags[flag] for flag in self.flags.keys()], bbox_to_anchor=(1, 0.9))
        f.subplots_adjust(right=0.85, wspace = 0.15, hspace = 0.25)
        plt.show()
        plt.tight_layout()
        return 1

    def plotDifferencesByCategory(self, figsize = (15, 5), ax = None, show = 1, legend = 0, fontsize = 10, title = 'Differences between budgeted and spent, by category'):
         xticklabels = self.months_to_include
         xs = range(len(self.months_to_include))
         flags = list(self.flags.keys() )
         if ax == None:
             f, ax = plt.subplots(1,1, figsize = figsize)
         scats = []
         for i in range(len(flags)):
             flag = flags[i]
             diffs_by_category = [month.differences[flag] for month in self.monthly_finances]
             scat = ax.plot(xs, diffs_by_category, marker = 'o', c = self.flag_colors[flag])[0]
             scats = scats + [scat]
         ax.set_xticks(xs)
         ax.set_xticklabels(xticklabels, fontsize = fontsize, rotation = 15)
         ax.set_title(title)
         if legend:
             ax.legend(scats, [self.flags[flag] for flag in self.flags.keys()], ncol = 4, fontsize = fontsize)
         if show:
             plt.show()
         return scats

    def plotTotalDifferences(self, figsize = (15, 5), ax = None, show = 1, legend = 0, fontsize = 10, title = 'Differences between budgeted and spent'):
         xticklabels = self.months_to_include
         xs = range(len(xticklabels))
         flag_keys = list(self.flags.keys())
         if ax == None:
             f, ax = plt.subplots(1,1, figsize = figsize)
         diffs = [ [month.differences[flag] for flag in flag_keys] for month in self.monthly_finances ]
         list_of_colors = [ [self.flag_colors[flag] for flag in flag_keys] for month in self.monthly_finances ]
         bars = can.plotBarGraphStack(xs, diffs, list_of_colors, ax = ax, figsize = (10, 15))

         overall_diffs = [month.overall_diff for month in self.monthly_finances]
         scat = ax.plot(xs, overall_diffs, marker = 'x', c = 'k')[0]
         ax.set_xticks(xs)
         ax.set_xticklabels(xticklabels, fontsize = fontsize, rotation = 15)
         ax.axhline(0.0, c = 'k', linestyle = '--')
         ax.set_title(title)
         #ax.legend(bars, [self.flags[flag] for flag in can.niceReverse(sorted_flags)], ncol = 4)
         if legend:
             ax.legend(bars, [self.flags[flag] for flag in flag_keys], ncol = 4, fontsize = fontsize)
         if show:
             plt.show()
         return bars

    def plotTotalFinances(self, figsize = (15, 5), ax = None, show = 1, total_color = 'k', legend = 0, fontsize = 10, title = 'Total expenditures'):
         xticklabels = ['Starting'] + self.months_to_include
         xs = range(len(xticklabels))
         flag_keys = list(self.flags.keys())
         if ax == None:
             f, ax = plt.subplots(1,1, figsize = figsize)
         totals = [month.overall_total for month in self.monthly_finances]
         integrations = [ 0.0 for i in range(len(totals) + 1) ]
         integrations[0] = self.starting
         for i in range(1, len(integrations)):
             integrations[i] = integrations[i - 1] + totals[i - 1]

         costs = [ [month.totals[flag] for flag in flag_keys] for month in self.monthly_finances ]
         costs = [[integrations[i]] + costs[i] for i in range(len(costs))]
         list_of_colors = [ [total_color] + [self.flag_colors[flag] for flag in flag_keys] for month in self.monthly_finances ]
         bars = can.plotBarGraphStack(xs[1:], costs, list_of_colors, ax = ax, figsize = (10, 15))

         scat = ax.plot(xs, integrations, marker = 'x', c = 'gray', linestyle = '--')[0]
         ax.set_xticks(xs)
         ax.set_xticklabels(xticklabels, fontsize = fontsize, rotation = 15)
         ax.axhline(0.0, c = 'k', linestyle = '--')
         ax.set_title(title)
         if legend:
             ax.legend(bars, ['Starting'] + [self.flags[flag] for flag in flag_keys], ncol = 4, fontsize = fontsize)
         if show:
             plt.show()
         return bars


    def plotFinancesByCategoary(self, figsize = (15, 5), ax = None, show = 1, legend = 1, title = 'Total expenditues, by category'):
         xticklabels = self.months_to_include
         xs = range(len(self.months_to_include))
         scats = []
         flags = list(self.flags.keys() )
         if ax == None:
             f, ax = plt.subplots(1,1, figsize = figsize)
         for i in range(len(flags)):
             flag = flags[i]
             totals_by_category = [month.totals[flag] for month in self.monthly_finances]
             scat = ax.plot(xs, totals_by_category, marker = 'o', c = self.flag_colors[flag])[0]
             scats = scats + [scat]
         ax.set_xticks(xs)
         ax.set_xticklabels(xticklabels, rotation = 15)
         ax.set_title(title)
         if legend:
             ax.legend(scats, [self.flags[flag] for flag in self.flags.keys()], ncol = 4, fontsize = 10)
         if show:
             plt.show()
         return scats

    def __init__(self, months_to_include,
                 starting = 5480.48,
                 data_dir = '/Users/sashabrownsberger/Documents/Finances/MonthlyFinances/',
                 accounts_file = 'AccountAbbreviations.csv', flags_file = 'FlagAbbreviations.csv',):
        self.starting = starting
        self.months_to_include = months_to_include
        self.monthly_finances = [mec.MonthlyExpenditures(month) for month in months_to_include]
        self.accounts, self.account_colors = ft.readInAbbreviationFile(data_dir, accounts_file)
        self.flags, self.flag_colors = ft.readInAbbreviationFile(data_dir, flags_file)
        [month.sumExpenditures() for month in self.monthly_finances]
        [month.calculateDifferences() for month in self.monthly_finances]
        [month.sumDifferences() for month in self.monthly_finances]

if __name__ == "__main__":
    # python FinancesClass.py [November2022,December2022,January2023,February2023,March2023,April2023,May2023,June2023,July2023,August2023,September2023,October2023,Novermber2023,December2023,January2024]
    args = sys.argv[1:]
    months = args[0]
    months = can.recursiveStrToListOfLists(months)
    finances = Finances(months)
    finances.plotAllFinances()
