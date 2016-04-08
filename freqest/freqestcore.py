from dbhelper import get_firstname_count, get_lastname_percentage_rank


def get_not_popular_firstnames(names, firstname_count_threshold):
    # fetch first names frequency from first names database
    dbfilename = 'freqest//db//firstnames.sqlite'
    name_counts = [(name, get_firstname_count(dbfilename, name)) for name in names]

    not_popular_firstnames = []
    # if the count of name is less than firstname_count_threshold, add it to a
    # list
    for name, count in name_counts:
        if count < firstname_count_threshold:
            #print '%s : %d' % (name, count)
            not_popular_firstnames.append(name)
    return not_popular_firstnames


def get_not_popular_lastnames(names, lastname_rank_threshold):
    not_popular_lastnames = []
    # Check in last name db
    # if name is not in the last names db , add it to a list. If available and
    # has rank above last_name_rank_threshold, add it to a list.
    dbfilename = 'freqest//db//lastnames.sqlite'
    for name in names:
        result = get_lastname_percentage_rank(dbfilename, name)  # search in last name db
        if result is not None:
            percentage, rank = result
            #print 'Name: %s percentage: %s  rank: %s' % (name, percentage, rank)
            if int(rank) > lastname_rank_threshold:
                not_popular_lastnames.append(name)
            else:
                pass
        else:
            not_popular_lastnames.append(name)
    return not_popular_lastnames


def get_not_popular_names(names, firstname_count_threshold, lastname_rank_threshold, write_to_file=False):
    '''
    Filters through the first name database. The filtered list is passed 
    through last names db. The motivation is: Names deemed less frequent in 
    first names db are not necessarily less frequent. This tends to happen when 
    some very popular last names are used as first names. So search the names 
    deemed less frequent in first names db in the last name db as well.

    Another perspectives -- we are passing any name, whether first or last
    to get_not_popular_firstnames. last names are bound to be returned back.
    '''
    not_popular_names = get_not_popular_firstnames(names, firstname_count_threshold)
    # not_popular_names is a mix of not popular first names and probably
    # all last names
    not_popular_names = get_not_popular_lastnames(not_popular_names, lastname_rank_threshold)
    # Now --- not_popular_names is a mix of not popular first names and not
    # popular last names
    if write_to_file:
        with open('difficult_names.txt', 'w') as f:
            for name in sorted(not_popular_names):
                f.write(name + '\n')

    return not_popular_names


def process_names(filepath, params):

    first_name_count_threshold = params['first_name_threshold_denorm']
    last_name_rank_threshold = params['last_name_threshold_denorm']
    

    # assumes single name per line
    with open(filepath, 'r') as f:
        all_names = [line.rstrip() for line in f]

        return get_not_popular_names(all_names,
                                     first_name_count_threshold,
                                     last_name_rank_threshold,
                                     write_to_file=False)

if __name__ == '__main__':
    '''Play with this. Change firstname_count_threshold, lastname_rank_threshold
    In our trysts firstname_count_threshold of 400 and lastname_rank_threshold
    of 30000 seemed good. All names below the count of 400 are deemed not 
    popular and all names above rank of 30000 are deemed not popular'''

    not_popular_names = get_not_popular_names(names, firstname_count_threshold,
                                              lastname_rank_threshold,
                                              write_to_file=False)
