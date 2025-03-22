from ..database import DatabaseManager

class InventoryRepository:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_player_items(self, player_id: int):
        query = """
            SELECT i.*, inv.quantity 
            FROM inventory inv 
            JOIN items i ON inv.item_id = i.id 
            WHERE inv.player_id = %s
        """
        return self.db.execute_query(query, (player_id,))
    
    def add_item(self, player_id: int, item_id: int, quantity: int = 1):
        query = """
            INSERT INTO inventory (player_id, item_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """
        return self.db.execute_query(query, (player_id, item_id, quantity)) 