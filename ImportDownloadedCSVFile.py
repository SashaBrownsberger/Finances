import cantrips as can
import numpy as np

def identifyColumnsToSave(given_col_categories, cols_to_save ):
    given_col_categories = [col.lower() for col in given_col_categories]
    cols_to_save = [col.lower() for col in cols_to_save]
    col_indeces_to_save = [given_col_categories.index(col) for col in can.intersection(cols_to_save, given_col_categories)]
    return col_indeces_to_save

def parseRawData(csv_file, cols_to_read_in, delimiter, replace_delimiter, lines_to_skip = [] ):
    data = can.readInFileLineByLine(csv_file, n_ignore = 0)
    header = data[0].split(delimiter)
    data = data[1:]
    data = [line.split(delimiter) for line in data]
    print ('len(data) = ' + str(len(data)) )
    end_line = len(data)
    expected_n_elems = len(header)
    for i in can.niceReverse(list(range(0, len(data)))):
        line = data[i]
        if not(i in lines_to_skip):
            print ('i = ' + str(i))
            print ('len(line) = ' + str(len(line)))
            print ('expected_n_elems = ' + str(expected_n_elems))
            print ('line = ' )
            print (line )
        if len(line) > expected_n_elems and not(i in lines_to_skip):
            print ('I found that line ' + str(i + 1) + ' appears to have ' + str(len(line) - expected_n_elems) + ' more elements than expected.  Should I merge any of elements from this line: ')
            print (line)
            still_merging = 1
            while(still_merging):
                do_merger = can.getUserInputWithDefault('1, y, or yes for do/continue merger.  Anything else for move on (default: 0): ', '0')
                if do_merger.lower() in ['1', 'y', 'yes']:
                    still_merging = 1
                    elems_to_merge = input('Which elements should I merge, type as #/#? ')
                    elems_to_merge = elems_to_merge.split('/')
                    if (len(elems_to_merge) == 2 and elems_to_merge[0].isdigit() and elems_to_merge[1].isdigit()):
                        elems_to_merge = [int(elems_to_merge[0]), int(elems_to_merge[1])]
                        if (elems_to_merge[0] < len(line) and elems_to_merge[0] >= 0 and elems_to_merge[1] < len(line) and elems_to_merge[1] >= 0):
                            line = line[0:elems_to_merge[0]] + [line[elems_to_merge[0]] + replace_delimiter + line[elems_to_merge[1]]] + line[elems_to_merge[1]+1:]
                            print ('Line is now: ')
                            print (line)
                        else:
                            print ('The line is ' + str(line) + ' elems long.  Your input of '+ str(elems_to_merge) + ' are invalid indexes cannot be used as a valid index (format #/#).  Try again? ')
                    else:
                        print ('Your input of '+ str(elems_to_merge) + ' cannot be used as a valid set of indexes (format #/#).  Try again? ')
                else:
                    still_merging = 0
        data[i] = line
        if len(data[i]) <= max(cols_to_read_in):
            end_line = i
    print ('end_line = '+ str(end_line))
    data = data[:end_line]
    print ('len(data) = ' + str(len(data)))
    print ('len(lines_to_skip) = ' + str(len(lines_to_skip)))
    for i in can.niceReverse(sorted(lines_to_skip)):
        print ('i = ' + str(i))
        data = can.removeListElement(data, i)
    print ('len(data) = ' + str(len(data)))
    return data

def importCapitalOneCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = [], date_sep_delim = '-', delimiter = ',', replace_delimiter = ' ', date_col = 0, description_col = 3, cat_col = 4, in_amount_col = 6, out_amount_col = 5 ):
    #col_indeces_to_save = identifyColumnsToSave(given_col_categories, cols_to_save)
    #Lines with more elements should be checked for interfering commas
    data = parseRawData(csv_file, [date_col, description_col, cat_col, in_amount_col, out_amount_col], delimiter, replace_delimiter, lines_to_skip = lines_to_skip)
    print ('data = ' + str(data))
    dates = [line[date_col].split(date_sep_delim) for line in data]
    dates = [int(date[0] + date[1] + date[2]) for date in dates]
    descriptions = [line[description_col] for line in data]
    categories = [line[cat_col] for line in data]
    amount_col = [float('0' + line[in_amount_col]) - float('0' + line[out_amount_col]) for line in data]
    transaction_flag_col = [1 for i in range(len(amount_col))]
    data_to_save = [dates, descriptions, categories, amount_col, transaction_flag_col]
    print ('Done parsing data.')

    return data_to_save

def importAmExCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = [], date_sep_delim = '/', delimiter = ',', replace_delimiter = ' ', date_col = 0, description_col = 1, amount_col = 2):
    data = parseRawData(csv_file, [date_col, description_col, amount_col], delimiter, replace_delimiter, lines_to_skip = lines_to_skip)
    dates = [line[date_col].split(date_sep_delim) for line in data]
    print ('dates = ')
    print (dates)
    dates = [int(date[2] + date[0] + date[1]) for date in dates]
    descriptions = [line[description_col] for line in data]
    categories = ['' for line in data]
    #We want to define negative as spending.  AmEx Does the opposite by default
    # so we add a - sign here.
    amount_col = [-float(line[amount_col]) for line in data]
    transaction_flag_col = [1 for i in range(len(amount_col))]
    data_to_save = [dates, descriptions, categories, amount_col, transaction_flag_col]
    print ('Done parsing data.')
    return data_to_save

def importChaseCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = [], date_sep_delim = '/', delimiter = ',', replace_delimiter = ' ', t_date_col = 0, p_date_col = 1, description_col = 2, cat_col = 3, in_or_out_col = 4, amount_col = 5, memo_col = 6 ):
    #col_indeces_to_save = identifyColumnsToSave(given_col_categories, cols_to_save) Transaction Date,Post Date,Description,Category,Type,Amount,Memo
    #Lines with more elements should be checked for interfering commas
    data = parseRawData(csv_file, [t_date_col, p_date_col, description_col, cat_col, in_or_out_col, amount_col, memo_col], delimiter, replace_delimiter, lines_to_skip = lines_to_skip)
    dates = [(line[t_date_col]).split(date_sep_delim) for line in data]
    dates = [int(date[2] + date[0] + date[1]) for date in dates]
    descriptions = [line[description_col] for line in data]
    categories = [line[cat_col] for line in data]
    amount_col = [float(line[amount_col]) for line in data]
    transaction_flag_col = [1 for i in range(len(amount_col))]
    data_to_save = [dates, descriptions, categories, amount_col, transaction_flag_col]
    print ('Done parsing data.')
    return data_to_save

def importCapitalOneAccount(csv_file, description_to_category_dir, lines_to_skip = [], date_sep_delim = '/', delimiter = ',', replace_delimiter = ' ', account_num_col= 0, date_col = 1, description_col = 4, cat_col = 3, quantity_col = 2, out_amount_col = 5 ):
    #col_indeces_to_save = identifyColumnsToSave(given_col_categories, cols_to_save)
    #Lines with more elements should be checked for interfering commas
    data = parseRawData(csv_file, [account_num_col, date_col, description_col, cat_col, quantity_col, out_amount_col], delimiter, replace_delimiter, lines_to_skip = lines_to_skip)
    print ('data = ' + str(data))
    dates = [line[date_col].split(date_sep_delim) for line in data]
    dates = [int('20' + date[2] + date[0] + date[1]) for date in dates]
    descriptions = [line[description_col] for line in data]
    categories = [line[cat_col] for line in data]
    quantities = [float(line[quantity_col]) for line in data]
    balances = [float(line[out_amount_col]) for line in data]
    #Now add add a separate line, once for the transaction and once for the balance
    dates = can.flattenListOfLists([[dates[i], dates[i]] for i in range(len(dates))])
    descriptions = can.flattenListOfLists([[descriptions[i], descriptions[i]] for i in range(len(descriptions))])
    categories = can.flattenListOfLists([[categories[i], categories[i]] for i in range(len(categories))])
    transaction_flag_col = can.flattenListOfLists([[1, 0] for i in range(len(quantities))])
    quantities = can.flattenListOfLists([[quantities[i], balances[i]] for i in range(len(quantities))])
    data_to_save = [dates, descriptions, categories, quantities, transaction_flag_col]
    print ('Done parsing data.')

    return data_to_save

def readInDescriptionToCategoryDir():
    return 0

def importRawCSVFile(csv_file, source, lines_to_skip = []): #, cols_to_save = ['Transaction date', 'Amount', 'Description', 'Category']):
    #if 'Category' in cols_to_save:
    #    description_to_category_dir = readInDescriptionToCategoryDir()
    #else:
    #    description_to_category_dir = None
    description_to_category_dir = readInDescriptionToCategoryDir()
    if source.lower() in ['capitalonecreditcard', 'capitalonecc', 'c1credictcard', 'c1cc']:
        data = importCapitalOneCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = lines_to_skip)
    elif source.lower() in ['americanexpresscreditcard', 'americanexpressecc', 'amexcredictcard', 'amexcc', 'americanexpresscreditcard_sasha', 'americanexpressecc_sasha', 'amexcredictcard_sasha', 'amexcc_sasha', 'americanexpresscreditcard_masha', 'americanexpressecc_masha', 'amexcredictcard_masha', 'amexcc_masha']:
        data = importAmExCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = lines_to_skip)
    elif source.lower() in ['chasereserve','chasereservecreditcard', 'chasereservecc', 'crcredictcard', 'crcc','chasecreditcard', 'chasecc', 'ccredictcard', 'ccc']:
        data = importChaseCreditCardCSVFile(csv_file, description_to_category_dir, lines_to_skip = lines_to_skip)
    elif source.lower() in ['capitalonechecking', 'capitalonech', 'c1checking', 'c1ch','capitalonesaving', 'capitalones', 'c1saving', 'c1s']:
        data = importCapitalOneAccount(csv_file, description_to_category_dir, lines_to_skip = lines_to_skip)
    else:
        print ('I could not find finance stream: ' + str(source) + ' in my knowledge of streams. Check spelling, or add to the ImportDownloadedCSVFile.py python script? ')
        return 0
    return data

def identifyAlreadyRecordedLines(new_lines, existing_lines):
    already_recorded_indeces = []
    for i in range(len(new_lines)):
        line = new_lines[i]
        if line in existing_lines:
            already_recorded_indeces = already_recorded_indeces + [i]
    already_recorded_indeces = np.unique(already_recorded_indeces)
    return already_recorded_indeces

def addFileToStreamHistory(csv_file, source, raw_source_suffix = '_RAW.csv', compiled_data_suffix = '_COMPILED.csv', data_dir = 'Data/', delimiter = ', '):
    raw_file = data_dir + source + raw_source_suffix
    compiled_file = data_dir + source + compiled_data_suffix
    raw_lines = can.readInFileLineByLine(data_dir + csv_file, n_ignore = 1) #Must have a header to ignore
    existing_raw_lines = can.readInFileLineByLine(raw_file, n_ignore = 1)
    already_located_indeces = identifyAlreadyRecordedLines(raw_lines, existing_raw_lines)
    print ('already_located_indeces = ')
    print (already_located_indeces)
    print ('[len(raw_lines), len(already_located_indeces)] = ' + str([len(raw_lines), len(already_located_indeces)]))
    #Now we need to save the not already imported data to another (temporary) csv file, which is the one for which we'll generate data
    new_raw_lines = [raw_lines[i] for i in range(len(raw_lines)) if not(i in already_located_indeces)]
    print ('new_raw_lines = ')
    print (new_raw_lines)
    data = importRawCSVFile(data_dir + csv_file, source, lines_to_skip = already_located_indeces)
    #data = data + [[1 for row in range(len(data[0]))]]
    previous_data = can.readInColumnsToList(compiled_file, n_ignore = 0, delimiter = delimiter, remove_redundant_delimiter = 0)
    header = delimiter.join([col[0] for col in previous_data])
    previous_data = [col[1:] for col in previous_data]
    print ('data = ')
    print (data)
    print ('previous_data = ')
    print(previous_data)
    print('header = ')
    print(header )
    if len(data) == 0:
        combined_data = previous_data
    elif len(previous_data) == 0:
        combined_data = data
    else:
        combined_data = [previous_data[i] + data[i] for i in range(len(data))]
    print ('compiled_file = ' + str(compiled_file))
    combined_data = can.safeSortOneListByAnother([int(date) for date in combined_data[0]], combined_data)
    print ('combined_data = ' )
    print(combined_data )
    can.saveListsToColumns(combined_data, compiled_file, '', sep = delimiter, header = header )

    #Add the now read-in lines (wait until we have successfully updated all the other data)
    with open(raw_file, 'a') as raw_file_obj:
        for line in new_raw_lines:
            raw_file_obj.write(line + '\n')

    return 1
