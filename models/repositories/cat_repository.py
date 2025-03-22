from ..database import DatabaseManager

class CatRepository:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create(self, player_id: int, name: str, breed: str, stats: dict):
        query = """
            INSERT INTO cats (player_id, name, breed, health, attack, defense, speed, level, experience, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            player_id, name, breed,
            stats['health'], stats['attack'], stats['defense'], stats['speed'],
            1, 0, False
        )
        self.db.execute_query(query, params)
        # Get the last inserted cat
        return self.get_last_created_cat(player_id)
    
    def get_player_cats(self, player_id: int):
        """Get all cats owned by a player"""
        query = "SELECT * FROM cats WHERE player_id = %s"
        return self.db.execute_query(query, (player_id,))
    
    def get_by_id(self, cat_id: int):
        query = "SELECT * FROM cats WHERE id = %s"
        results = self.db.execute_query(query, (cat_id,))
        return results[0] if results else None
    
    def get_last_created_cat(self, player_id: int):
        query = "SELECT * FROM cats WHERE player_id = %s ORDER BY id DESC LIMIT 1"
        results = self.db.execute_query(query, (player_id,))
        return results[0] if results else None
    
    def get_active_cat(self, player_id: int):
        query = "SELECT * FROM cats WHERE player_id = %s AND is_active = TRUE LIMIT 1"
        results = self.db.execute_query(query, (player_id,))
        return results[0] if results else None
    
    def update_name(self, cat_id: int, player_id: int, new_name: str):
        query = "UPDATE cats SET name = %s WHERE id = %s AND player_id = %s"
        return self.db.execute_query(query, (new_name, cat_id, player_id))

    def set_active(self, cat_id: int, player_id: int):
        # First deactivate all cats for this player
        self.db.execute_query(
            "UPDATE cats SET is_active = FALSE WHERE player_id = %s",
            (player_id,)
        )
        # Then activate the selected cat
        self.db.execute_query(
            "UPDATE cats SET is_active = TRUE WHERE id = %s AND player_id = %s",
            (cat_id, player_id)
        ) 