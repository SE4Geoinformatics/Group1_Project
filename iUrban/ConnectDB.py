from psycopg2 import connect, DatabaseError


def connect_db():
    # # *******************************************use the dbConfig.txt

    # # use this code in VS Code
    myFile = open("E:\\PolimiCourseFiles\MyCourses\\20202021semester2\\SE4geoinformatics\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')

    # # use this code in Spyder
    # myFile = open("dbConfig.txt", "r", encoding='utf-8')

    connStr = myFile.readline()
    conn = connect(connStr)
    return conn

    # # ********************************************use the dbConfig.py
    # params = config()
    # print('Connecting to the PostgreSQL database...')
    # conn = connect(**params)
    # return conn
