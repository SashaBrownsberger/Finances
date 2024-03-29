import numpy as np
import cantrips as can

class DescriptionToFinanceCategoryClass:

    def getCategoriesOfDescriptions(self, descriptions, update_descriptions = 1):


    def readInDescriptionsToAbbreviationsFile(self, file_path, delimiter = ' : '):
        data = can.readInColumnsToList(file_path, n_ignore = 1, delimiter = delimiter)
        description = data[0]
        category = data[1]
        n_descriptions = len(description)
        description_to_category_dir = dict([(description[i], category[i]) for i in range(n_descriptions)])

        return description_to_category_dir

    def readInAbbreviationsFile(self, file_path, delimiter = ','):
        data = can.readInColumnsToList(file_path, n_ignore = 1, delimiter = delimiter)
        abbreviation = data[0]
        category = data[1]
        plot_color = data[2]
        return [abbreviation, category, plot_color]

    def __init__(self, flag_abbrev_file = 'FlagAbbreviations.csv', description_to_category_dir = 'DescriptionToSpendingCategoryDict.txt', reference_files_dir = 'ref/'):
        abbreviation, category, plot_color = self.readInAbbreviationsFile(reference_files_dir + flag_abbrev_file)
        n_categories = len(category)
        self.abbrev_to_plot_color_dict = dict([(abbreviation[i], plot_color[i]) for i in range(n_categories)])
        self.abbrev_to_category_dict = dict([(abbreviation[i], category[i]) for i in range(n_categories)])
        self.category_to_abbrev_dict = dict([(category[i], abbreviation[i]) for i in range(n_categories)])
        self.description_to_category_dict = self.readInDescriptionsToAbbreviationsFile(reference_files_dir + description_to_category_dir)
