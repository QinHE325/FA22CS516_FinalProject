from itertools import product
from flask import current_app as app

class Inventory:
    def __init__(self, id, sid, pid, name,description,quantity,price,release_date):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.name = name
        self.description = description 
        self.quantity = quantity
        self.price = price
        self.release_date = release_date
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, sid, pid,quantity,price, release_date
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Inventory(*(rows[0])) if rows else None
    
    @staticmethod
    def product_exists(pid,name):
        rows = app.db.execute("""
SELECT name
FROM Inventory
WHERE name = :name AND pid = :pid
""",
                              name=name,pid = pid)
        return len(rows) > 0
    
    @staticmethod
    def add_inventory(self,sid,pid,name,description,quantity,price):
        if self.product_exists(pid,name):
            try:
                rows = app.db.execute("""
    INSERT INTO Inventory(sid, pid,name,description, quantity, price)
    VALUES(:sid, :pid, :name,:description, :quantity, :price)
    RETURNING id
    """,
                                    sid=sid,
                                    pid=pid,
                                    name = name,
                                    description = description,
                                    quantity=quantity, 
                                    price=price )
                id = rows[0][0]
                return Inventory.get(id)
            except Exception as e:
                print(str(e))
                return None
        # if name exists it will update quantity and description
        else:
            try:
                rows = app.db.execute("""
    UPDATE Inventory(quantity, description)
    SET quantity = quantity + :quantity, description = :description
    RETURNING id
    """,
                                    description = description,
                                    quantity=quantity, 
                                     )
                id = rows[0][0]
                return Inventory.get(id)
            except Exception as e:
                print(str(e))
                return None
         