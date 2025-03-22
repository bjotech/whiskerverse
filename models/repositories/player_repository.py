from ..database import DatabaseManager

class PlayerRepository:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_by_id(self, player_id: int):
        query = "SELECT * FROM players WHERE id = %s"
        results = self.db.execute_query(query, (player_id,))
        return results[0] if results else None
    
    def create(self, player_id: int, username: str):
        query = """
            INSERT INTO players (id, username, level, experience, coins, current_location)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (player_id, username, 1, 0, 100, 'Whiskerton'))
        return self.get_by_id(player_id)
    
    def get_cats(self, player_id: int):
        query = "SELECT * FROM cats WHERE player_id = %s"
        return self.db.execute_query(query, (player_id,))
    
    def get_inventory(self, player_id: int):
        query = """
            SELECT i.*, inv.quantity 
            FROM inventory inv 
            JOIN items i ON inv.item_id = i.id 
            WHERE inv.player_id = %s
        """
        return self.db.execute_query(query, (player_id,)) 