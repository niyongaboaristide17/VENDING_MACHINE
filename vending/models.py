from datetime import datetime
from .dbAdapter import DatabaseAdapter


class ProductCrud(DatabaseAdapter):
    def create(self, name, price):
        sql = "INSERT INTO PRODUCT (name, price) VALUES (%s, %s)"
        val = (name, price)
        self.cursor.execute(sql, val)
        product_id = self.cursor.lastrowid
        self.db.commit()
        StockCrud().create(product_id)

    def find_all(self):
        self.cursor.execute("SELECT * FROM PRODUCT")
        return self.cursor.fetchall()


class StockCrud(DatabaseAdapter):
    def create(self, product_id):
        sql = "INSERT INTO STOCK (product_id) VALUES (%s)"
        val = (product_id,)
        self.cursor.execute(sql, val)
        self.db.commit()

    def increase_stock(self, quantity, stock_id):
        sql = "UPDATE STOCK SET quantity = quantity + %s WHERE id = %s"
        val = (quantity, stock_id)
        self.cursor.execute(sql, val)
        self.db.commit()
        print('SUCCESS STOCK INCREASE!!!!!')

    def product_stock(self):
        sql = "SELECT \
  PRODUCT.name AS pname, \
  PRODUCT.id AS pid, STOCK.id AS sid, STOCK.quantity AS qty, PRODUCT.price AS price FROM STOCK \
  INNER JOIN PRODUCT ON STOCK.product_id = PRODUCT.id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_one(self, stock_id):
        sql = "SELECT * FROM STOCK WHERE id = %s"
        val = (stock_id,)
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()

    def purchase_item(self, stock_id):

        if self.get_one(stock_id)[2] < 1:
            print('Stock empty')
            return
        sql = "UPDATE STOCK SET quantity = quantity - 1 WHERE id = %s"
        val = (stock_id,)
        self.cursor.execute(sql, val)
        self.db.commit()


class InvoiceCrud(DatabaseAdapter):
    def create(self, items):
        sql = "INSERT INTO INVOICE (created_on) VALUES (%s)"
        val = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),)
        self.cursor.execute(sql, val)
        invoice_id = self.cursor.lastrowid
        self.db.commit()
        stock_crud = StockCrud()
        line_item_crud = LineItemCrud()
        for value in items:
            stock_crud.purchase_item(value)
            line_item_crud.create(value, invoice_id)


class LineItemCrud(DatabaseAdapter):
    def create(self, stock_id, invoice_id):
        sql = "INSERT INTO LINE_ITEM (stock_id, invoice_id) VALUES (%s, %s)"
        val = (stock_id, invoice_id)
        self.cursor.execute(sql, val)
        self.db.commit()
