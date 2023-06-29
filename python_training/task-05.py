import psycopg2

def execute_sql(statement):
    '''Inserts hard-coded data to EMPLOYEE.
    '''
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.commit()
        print("Statement executed successfully.")
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("An error occurred:", e)

def select_data():
    '''Prints out in console all from EMPLOYEE.
    '''
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EMPLOYEE")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print("An error occurred:", e)

# Main program
def main():
    action = input("Enter the action to execute (select, insert, update, delete): ")

    # Hard-coded data operations
    if action == "select":
        select_data()
    elif action == "insert":
        insert_statement = "INSERT INTO EMPLOYEE (FIRST_NAME, LAST_NAME, SALARY, START_DATE) " \
                           "VALUES ('John', 'Doe', 5000, '2023-01-01'), " \
                           "('Jane', 'Smith', 6000, '2023-02-01'), " \
                           "('Mike', 'Johnson', 7000, '2023-03-01')"
        execute_sql(insert_statement)
    elif action == "update":
        update_statement = "UPDATE EMPLOYEE SET SALARY = 5500 WHERE ID = 1"
        execute_sql(update_statement)
    elif action == "delete":
        delete_statement = "DELETE FROM EMPLOYEE WHERE ID = 2"
        execute_sql(delete_statement)
    else:
        print("Invalid action. Please try again.")

if __name__ == '__main__':
    # Database connection details
    dbname = 'postgres'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    main()

# # Manually create pgAdmin table (db Query Tool terminal)
# CREATE TABLE EMPLOYEE (
#     ID SERIAL PRIMARY KEY,
#     FIRST_NAME VARCHAR(50),
#     LAST_NAME VARCHAR(50),
#     SALARY FLOAT,
#     START_DATE DATE
# );
