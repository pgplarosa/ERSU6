import re
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from sqlalchemy import create_engine

def get_faculty_profile_table(db_path='../data/db.sqlite3',
                             show=False):
    """ outputs a table with columns: name, education, 
        position, interests
    
    Parameters
    ===========
    db_path      :      str
                        path of sqlite database
    show         :      bool
                        print table if set to true
    
    Returns
    ===========
    get_faculty_profile_table    :   str
                                     json string
    """
    engine = create_engine('sqlite:///' + db_path)
    query = """
    SELECT fa.faculty_name as Name,
           fa.highest_educ_attain as Education,
           fa.position as Position,
           fa.interests as Interests, 
           sc.school_name as University
    FROM faculty fa
    LEFT OUTER JOIN school sc
    on fa.school_id = sc.school_id
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    if show:
        display(df)
    return df.to_json(orient='columns')

def get_faculty_educ_attain(db_path='../data/db.sqlite3',
                            plot=False):
    """ count the number of highest educ attainment per university
    
    Parameters
    ===========
    db_path      :      str
                        path of sqlite database
    plot         :      bool
                        display plot if set to true
    
    Returns
    ===========
    get_faculty_profile_table    :   str
                                     json string
    """
    engine = create_engine('sqlite:///' + db_path)
    query = """
    SELECT sc.school_name as University,
           fa.highest_educ_attain as Education
    FROM faculty fa
    LEFT OUTER JOIN school sc
    on fa.school_id = sc.school_id
    """
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
    df = pd.crosstab(df.University, 
                     df.Education).sort_index(ascending=False)
    if plot:
        df.plot.barh(stacked=True)
        plt.show()

    return df.to_json(orient='columns')
