import FinanceStreamClass as fsc
import numpy as np
import matplotlib.pyplot as plt
import datetime
import cantrips as can
import ImportDownloadedCSVFile as icsv

def getDetailedInstructions(stream_name):
    instructions_dir = {
        "CapitalOneCC":
         "If you want to update a balance, just note the number displayed on the card account. If you want to update the monthly expenditures, open up the corresponding statement and find the list of credits for the month and enter them as negative value transactions when the time comes.  Enter the statement balance as a balance (a sample statement image will be added to the GitHub)."
        ,"AmericanExpressCCSasha":
        "If you want to update a balance, just note the number displayed on the card account. If you want to update the monthly expenditures, open up the corresponding statement, find 'Payments/Credits' entry, and enter that as a negative transactions when the time comes.  Enter the 'New Balance' as a balance (a sample statement image will be added to the GitHub)."
        , "ChaseReserveCC":
        "If you want to update a balance, just note the number displayed on the card account. If you want to update the monthly expenditures, open up the corresponding statement, find 'Payments/Credits' entry, and enter that as a negative transactions when the time comes.  Enter the 'New Balance' as a balance (a sample statement image will be added to the GitHub)."
    }
    return instructions_dir[stream_name]

def doStreamUpdate(stream, stream_name, detailed_instructions = 1):
     if detailed_instructions:
         instructions = getDetailedInstructions(stream_name)
         print (instructions)
     still_updating = 1
     updating_prompt = 'Do you want to update (or continue updating) stream ' + stream_name + ' by hand (1, y, or yes for "yes", anything else for no; default: n)?'
     while still_updating:
         user_continue = can.getUserInputWithDefault(updating_prompt, 'n')
         if user_continue.lower() in ['1','y','yes']:
             stream.updateDataStreamByHand()
             stream.saveStreamFile()
         else:
             still_updating = 0
     updating_prompt = 'Do you want to update (or continue updating) stream ' + stream_name + ' from a file (1, y, or yes for "yes", anything else for no; default: n)?'
     still_updating = 1
     while still_updating:
         user_continue = can.getUserInputWithDefault(updating_prompt, 'n')
         if user_continue.lower() in ['1','y','yes']:
             stream.updateDataStreamFromFile()
             stream.saveStreamFile()
         else:
             still_updating = 0
     return 1

def plotBalances(streams, stream_names, start_date_str, end_date_str, N_days_per_point, date_format_string, plot_color_dict, avg_period = 30, ax = None, show_fig = 1, save_fig = 1):
    if ax == None:
         f, ax = plt.subplots(1,1)
    balances = [stream.getBalanceInterpolator() for stream in streams]
    balance_measured_points = [balance[0] for balance in balances]
    balance_interpolators = [balance[1] for balance in balances]
    start_date = datetime.datetime.strptime(str(start_date_str), date_format_string)
    end_date = datetime.datetime.strptime(str(end_date_str), date_format_string)
    N_days_start_to_end = (end_date - start_date).days
    days_to_plot_balances = np.arange(0, N_days_start_to_end, N_days_per_point)
    total_balances = np.array([0 for day in days_to_plot_balances])
    scats = [0 for i in range(len(streams))]
    for i in range(len(streams)):
        stream_name = stream_names[i]
        scat = ax.scatter(balance_measured_points[i][0], -np.array(balance_measured_points[i][1]), c = plot_color_dict[stream_name])
        scats[i] = scat
        interped_balance = balance_interpolators[i] (days_to_plot_balances)
        total_balances = total_balances - interped_balance
    total_plot = ax.plot(days_to_plot_balances, total_balances, marker = 'x', c = plot_color_dict['Total'])[0]
    ax.set_xlabel(r'$\Delta$ days')
    ax.set_ylabel('Balance carried on date')
    ax.legend(scats + [total_plot], stream_names + ['Total (interpolated)'])
    if save_fig:
         plt.savefig('plots/TotalSpending_Made' + datetime.date.today().strftime('%Y%m%d') + '.pdf')
    if show_fig:
         plt.show()
    return 1

def plotSpending(streams, stream_names, start_date_str, end_date_str, N_days_per_point, date_format_string, plot_color_dict, avg_period = 30, ax = None, show_fig = 1, save_fig = 1):
    if ax == None:
        f, ax = plt.subplots(1,1)
    spending_amounts = [stream.getSpendingInterpolator(N_days_per_point) for stream in streams]
    spending_measured_points = [spending_amount[0] for spending_amount in spending_amounts]
    spending_amount_interpolators = [spending_amount[1] for spending_amount in spending_amounts]
    start_date = datetime.datetime.strptime(str(start_date_str), date_format_string)
    end_date = datetime.datetime.strptime(str(end_date_str), date_format_string)
    N_days_start_to_end = (end_date - start_date).days
    days_to_plot_spending = np.arange(0, N_days_start_to_end, N_days_per_point)
    total_spending_per_day = np.array([0 for day in days_to_plot_spending])
    scats = [0 for i in range(len(streams))]
    for i in range(len(streams)):
        stream_name = stream_names[i]
        scat = ax.scatter(spending_measured_points[i][0], -np.array(spending_measured_points[i][1]) * N_days_per_point, c = plot_color_dict[stream_name])
        scats[i] = scat
        interped_spending = spending_amount_interpolators[i] (days_to_plot_spending)
        total_spending_per_day = total_spending_per_day + interped_spending
    total_spending = -np.array(total_spending_per_day) * N_days_per_point
    total_plot = ax.plot(days_to_plot_spending, total_spending, marker = 'x', c = plot_color_dict['Total'])[0]
    avg_spending = [sum(total_spending[abs(days_to_plot_spending - days_to_plot_spending[j]) <= avg_period / 2]) / len(total_spending[abs(days_to_plot_spending - days_to_plot_spending[j]) <= avg_period /2])
                    for j in range(len(days_to_plot_spending))]
    total_avg_plot = ax.plot(days_to_plot_spending, avg_spending, marker = 'x', c = plot_color_dict['Total (AVG)'])[0]
    ax.set_xlabel(r'$\Delta$ days')
    ax.set_ylabel('Spending rate over ' + str(N_days_per_point) + ' day interval')
    ax.legend(scats + [total_plot, total_avg_plot ], stream_names + ['Total (Interpolated)', 'Total (' + str(avg_period) + 'D AVG; interpolated)'] )
    if save_fig:
         plt.savefig('plots/TotalSpending_Made' + datetime.date.today().strftime('%Y%m%d') + '.pdf')
    if show_fig:
         plt.show()
    return 1


if __name__ =="__main__":
    spending_stream_data_folder = "Data/"
    start_date_str = '20221101'
    end_date_str = 'Today'
    date_format_string = '%Y%m%d'
    figsize = (12, 8)
    if end_date_str.lower() in ['today', 'now']:
        today = datetime.date.today()
        end_date_str = today.strftime(date_format_string)

    #Add new data from files
    #c1cc_to_add =
    #amexcc_to_add =
    #crcc_to_add =
    #icsv.addFileToStreamHistory(c1cc_to_add, 'c1cc', raw_source_suffix = '_RAW.csv', compiled_data_suffix = '_COMPILED.csv', data_dir = 'Data/', temp_file_name = 'TEMP.csv', delimiter = ', ')
    #icsv.addFileToStreamHistory(amexcc_to_add, 'amexcc', raw_source_suffix = '_RAW.csv', compiled_data_suffix = '_COMPILED.csv', data_dir = 'Data/', temp_file_name = 'TEMP.csv', delimiter = ', ')
    #icsv.addFileToStreamHistory(crcccc_to_add, 'crcc', raw_source_suffix = '_RAW.csv', compiled_data_suffix = '_COMPILED.csv', data_dir = 'Data/', temp_file_name = 'TEMP.csv', delimiter = ', ')

    N_days_per_point = 7
    spending_stream_names = ['CapitalOneCC', 'AmericanExpressCCSasha', 'ChaseReserveCC',
#                              'AmericanExpressMasha', 'ChaseMasha'
                               ]
    plot_color_dict = {'CapitalOneCC':'red', 'AmericanExpressCCSasha':'silver', 'ChaseReserveCC':'DarkBlue','Total':'k', 'Total (AVG)':'brown'}
    saving_stream_names =  ['c1cc', 'amexs', 'crcc']
    spending_streams = [fsc.FinanceStream(stream_file, spending_stream_data_folder, start_date_str = start_date_str, update_on_start = 0, date_format_string = date_format_string) for stream_file in spending_stream_names]

    for i in range(len(spending_streams)):
        stream = spending_streams[i]
        stream_name = spending_stream_names[i]
        doStreamUpdate(stream, stream_name)
    f, axarr = plt.subplots(2,1, figsize = figsize)
    plotSpending(spending_streams, spending_stream_names, start_date_str, end_date_str, N_days_per_point, date_format_string, plot_color_dict, ax = axarr[0], show_fig = 0, save_fig = 0 )
    plotBalances(spending_streams, spending_stream_names, start_date_str, end_date_str, N_days_per_point, date_format_string, plot_color_dict, ax = axarr[1], show_fig = 0, save_fig = 0 )
    plt.savefig('plots/TotalSpendingAndBalances_Updated' + datetime.date.today().strftime('%Y%m%d') + '.pdf')
    plt.show()
    print ('I have updated the data streams, saved the streams, and saved the plots. ')
