def getFinancialStreamIDsFromShorthand(shorthand):
    capital_one_cc_shorthands = ['capitalonecreditcard', 'capitalonecc', 'c1credictcard', 'c1cc']
    amex_cc_sasha_shorthands = ['americanexpresscreditcardsasha', 'americanexpressccsasha', 'amexcredictcardsasha', 'amexcardsasha','amexccsasha', 'amexsasha',
                                 'americanexpresscreditcards', 'americanexpressccs', 'amexcredictcards', 'amexcards','amexccs', 'amexs',
                                 'americanexpresscreditcard_sasha', 'americanexpresscc_sasha', 'amexcredictcard_sasha', 'amexcard_sasha','amexcc_sasha', 'amex_sasha',
                                 'americanexpresscreditcard_s', 'americanexpresscc_s', 'amexcredictcard_s', 'amexcard_s','amexcc_s',  'amex_s',]
    amex_cc_masha_shorthands = ['americanexpresscreditcardmasha', 'americanexpressccmasha', 'amexcredictcardmasha', 'amexcardmasha','amexccmasha', 'amexmasha',
                                'americanexpresscreditcardm', 'americanexpressccm', 'amexcredictcardm', 'amexcardm','amexccm', 'amexm',
                                'americanexpresscreditcard_masha', 'americanexpresscc_masha', 'amexcredictcard_masha', 'amexcard_masha','amexcc_masha', 'amex_masha',
                                'americanexpresscreditcard_m', 'americanexpresscc_m', 'amexcredictcard_m', 'amexcard_m','amexcc_m', 'amex_m']
    chase_reserve_cc_shorthands = ['chasereservecreditcard', 'chasereservecc', 'crcredictcard', 'crcc','chasecreditcard', 'chasecc', 'ccredictcard', 'ccc']
    capital_one_checking_shorthands = ['capitalonechecking', 'capitalonech', 'c1checking', 'c1ch','c1check',]
    capital_one_saving_shorthands = ['capitalonesaving', 'capitalones', 'c1saving', 'c1s', 'c1save']

    print (shorthand.lower())
    if shorthand.lower() in capital_one_cc_shorthands:
        return 'CapitalOneCC'
    if shorthand.lower() in amex_cc_sasha_shorthands:
        return 'AmExCC_Sasha'
    if shorthand.lower() in amex_cc_masha_shorthands:
        return 'AmExCC_Masha'
    if shorthand.lower() in chase_reserve_cc_shorthands:
        return 'ChaseReserve'
    if shorthand.lower() in capital_one_checking_shorthands:
        return 'CapitalOneChecking'
    if shorthand.lower() in capital_one_saving_shorthands:
        return 'CapitalOneSaving'
