import database as db
import setup

# Driver code
if __name__ == "__main__":

    """
    Please enter the necessary information related to the DB at this place. 
    Please change PW and ROOT based on the configuration of your own system. 
    """
    #Database Credentials
    PW = "admin@2498347"  # IMPORTANT! Put your MySQL Terminal password here.
    ROOT = "root"
    DB = "ecommerce_record"  # This is the name of the database we will create in the next step - call it whatever you like.
    LOCALHOST = "localhost"

    # Connecting with the schema in MySQL
    connection = db.create_db_connection(LOCALHOST, ROOT, PW, DB)

    print("----------------E-commerce data storage Solution ------------------")
    print("\n")
    print("----------------Solution - Problem 2.b ----------------------------")
    # Here we will start inserting the data points into the orders' table
    print("Inserting additional 5 new orders: ")
    new_orders = """
    INSERT INTO orders VALUES
    (101, 12456, 2, 300, '4', '13'),
    (102, 32678, 5, 100, '2', '14'),
    (103, 87612, 6, 200, '1', '15'),
    (104, 87623, 7, 120, '3', '6'),
    (105, 8971, 1, 0, '5', '7')
    """
    db.create_insert_query(connection, new_orders)
    # Data insertion in the orders' table is completed.
    print("------------------ Solution - Problem 2.b is complete. -----------")
    print("\n")

    print("-------------------- Solution - Problem 2.c -----------------------")
    print("Listing all the orders: ")
    q1 = """
    SELECT * FROM orders;
    """
    orders = db.select_query(connection, q1)
    for order in orders:
        print(order)

    print("------------------ Solution - Problem 2.c is complete. -----------")
    print("\n")

    print("-------------------- Solution - Problem 3.a -----------------------")

    q2 = """
    SELECT * FROM orders 
    WHERE total_value = (select MIN(total_value) FROM orders);
    """

    min_order_detail = db.select_query(connection, q2)
    print("Order with minimum value is: ")
    print(min_order_detail)

    q3 = """
    SELECT * FROM orders 
    WHERE total_value = (select MAX(total_value) FROM orders);
    """

    max_order_detail = db.select_query(connection, q3)
    print("Order with maximum value is: ")
    print(max_order_detail)

    print("------------------ Solution - Problem 3.a is complete. -----------")
    print("\n")

    print("-------------------- Solution - Problem 3.b -----------------------")

    print("Listing orders with value greater than average order value of all the orders: ")

    q4 = """
    SELECT * FROM orders 
    WHERE total_value > (select AVG(total_value) FROM orders);
    """
    orders = db.select_query(connection, q4)
    for order in orders:
        print(order)

    print("------------------ Solution - Problem 3.b is complete. -----------")
    print("\n")

    print("-------------------- Solution - Problem 3.c -----------------------")

    print("Fetching customer details with max value order")
    q5 = """
    SELECT o.customer_id, MAX(o.total_value) as MAX_Value, c.user_name, c.user_email
    FROM ecommerce_record.orders o 
    LEFT JOIN ecommerce_record.users c ON o.customer_id = c.user_id 
    GROUP BY o.customer_id;
    """

    highest_purchase_per_customer = db.select_query(connection, q5)

    sql = '''
    INSERT INTO customer_leaderboard (customer_id, total_value, customer_name, customer_email) 
    VALUES (%s, %s, %s, %s)
    '''
    print("Initiating the data insertion in customer_leaderboard table: ")

    db.insert_many_records(connection, sql, highest_purchase_per_customer)
    print("Data is inserted in customer_leaderboard table.")
    print("------------------ Solution - Problem 3.c is complete. -----------")
    print("\n")
