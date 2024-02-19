import cantrips as can


def readInAbbreviationFile(dir, file_name):
   cols = can.readInColumnsToList(file_name, file_dir = dir, n_ignore = 0, delimiter =',')
   abbreviations = cols[0]
   meanings = cols[1]
   colors = cols[2]
   meaning_dict = {}
   color_dict = {}
   n_elems = len(abbreviations)
   for i in range(n_elems):
       meaning_dict[abbreviations[i]] = meanings[i]
       color_dict[abbreviations[i]] = colors[i]
   return meaning_dict, color_dict
