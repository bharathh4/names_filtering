from freqest import process_names, get_not_popular_names

def demo_using_file():
    filepath = 'uploads//names.txt'
    params = {'first_name_threshold_denorm': 400,
              'last_name_threshold_denorm': 80000}
    not_popular_names = process_names(filepath, params)
    
    with open(filepath, 'r') as f:
        names_in_file = [line.rstrip() for line in f]
        print 'The names in the input file are ' + ' , '.join(names_in_file)
        
    print 'Not popular names are ' + ' , '.join(not_popular_names)

def demo_using_list():
    names = ['jesse', 'bharath', 'hjesse', 'smith', 'meselch']
    print 'The input names are ' + ' , '.join(names)
    firstname_count_threshold = 400
    lastname_rank_threshold = 30000
    not_popular_names = get_not_popular_names(names, firstname_count_threshold,
                                              lastname_rank_threshold,
                                              write_to_file=False)
    print 'Not popular names are ' + ' , '.join(not_popular_names)
    
if __name__ == '__main__':

    demo_using_file()
    demo_using_list()