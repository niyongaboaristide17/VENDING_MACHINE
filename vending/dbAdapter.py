import mysql.connector


class DatabaseAdapter:
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='messi',
            password='messi',
            database="vending_machine"
        )
        self.cursor = self.db.cursor()
        self.db_init()

    def db_init(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS PRODUCT (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price decimal(15,2))"
        )
        
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS STOCK (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT, quantity INT DEFAULT 0, FOREIGN KEY (product_id) REFERENCES PRODUCT(id) ON DELETE CASCADE)"
        )
        
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS INVOICE (id INT AUTO_INCREMENT PRIMARY KEY, created_on DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS LINE_ITEM (id INT AUTO_INCREMENT PRIMARY KEY, stock_id INT, invoice_id INT, FOREIGN KEY (stock_id) REFERENCES STOCK(id) ON DELETE CASCADE, FOREIGN KEY (invoice_id) REFERENCES INVOICE(id) ON DELETE CASCADE)"
        )
        
