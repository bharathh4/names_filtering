import sqlite3

def get_firstname_count(dbfilename, name):
    conn = sqlite3.connect(dbfilename)
    c = conn.cursor()
    rows = c.execute("SELECT * from NationalNames where Name = '%s'" % (name.title()))
    return sum([count for id, name, year, gender, count in rows.fetchall()])

def get_lastname_percentage_rank(dbfilename, name):

    conn = sqlite3.connect(dbfilename)
    c = conn.cursor()
    rows = c.execute("SELECT * from fullnames where names = '%s'" % (name.upper()))

    try:
        result = [(name, float(percentage), int(rank)) for name, percentage, cum_freq, rank in rows.fetchall()][0]
        if result is not None:

            name_from_db, percentage_from_db, rank_from_db = result
            if name.upper() == name_from_db:
                return float(percentage_from_db), int(rank_from_db)
        else:
            return None
    except:
        return None
        
if __name__ == '__main__':
    population_percentage, db_ranking = get_lastname_percentage_rank('db//lastnames.sqlite', 'smith')
    print population_percentage, db_ranking
    firstname_count = get_firstname_count('db//firstnames.sqlite', 'john')
    print firstname_count