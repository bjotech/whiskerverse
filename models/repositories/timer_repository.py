from ..database import DatabaseManager

class TimerRepository:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_timer(self, player_id: int, action: str):
        """Get a timer record for a player and action"""
        query = "SELECT * FROM timers WHERE player_id = %s AND action = %s"
        results = self.db.execute_query(query, (player_id, action))
        return results[0] if results else None
    
    def set_timer(self, player_id: int, action: str, next_available):
        """Set or update a timer for a player and action"""
        query = """
            INSERT INTO timers (player_id, action, next_available) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE next_available = %s
        """
        return self.db.execute_query(query, (player_id, action, next_available, next_available))
    
    def delete_timer(self, player_id: int, action: str):
        """Delete a timer for a player and action"""
        query = "DELETE FROM timers WHERE player_id = %s AND action = %s"
        return self.db.execute_query(query, (player_id, action))
    
    def get_all_timers(self, player_id: int):
        """Get all timers for a player"""
        query = "SELECT * FROM timers WHERE player_id = %s"
        return self.db.execute_query(query, (player_id,))
    
    def reset_all_timers(self):
        """Reset all timers for all players by setting next_available to a past timestamp (admin function)"""
        query = "UPDATE timers SET next_available = '1970-01-01 00:00:00'"
        try:
            self.db.execute_query(query)
            return True
        except Exception as e:
            print(f"Error resetting all timers: {e}")
            return False
