from .base_model import BaseModel
from .cat import Cat

class Player(BaseModel):
    table_name = 'players'
    primary_key = 'id'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.level = kwargs.get('level', 1)
        self.experience = kwargs.get('experience', 0)
        self.coins = kwargs.get('coins', 100)
        self.current_location = kwargs.get('current_location', 'Whiskerton')
        self.created_at = kwargs.get('created_at')
    
    @classmethod
    def get_or_create(cls, discord_id: int, username: str):
        """Get an existing player or create a new one"""
        player = cls.get_by_id(discord_id)
        if player:
            return player
        
        # Create new player
        player = cls(
            id=discord_id,
            username=username,
            level=1,
            experience=0,
            coins=100,
            current_location='Whiskerton'
        )
        player.save()
        return player
    
    def start_adventure(self, cat_name: str):
        """Initialize a new player's adventure with their first cat"""
        try:
            self.db.start_transaction()
            
            # Check if player already has cats
            existing_cats = self.get_cats()
            if existing_cats:
                self.db.end_transaction()
                return False, "Already started adventure"
            
            # Generate starter cat
            starter_cat = Cat.generate_random(
                player_id=self.id,
                name=cat_name,
                rarity="common"
            )
            starter_cat.set_active()
            
            self.db.end_transaction()
            return True, starter_cat
            
        except Exception as e:
            self.db.end_transaction()
            raise
    
    def add_experience(self, amount: int):
        """Add experience points and handle level ups"""
        self.experience += amount
        
        # Check for level up
        # Experience needed for next level = current_level * 1000
        while self.experience >= self.level * 1000:
            self.experience -= self.level * 1000
            self.level += 1
            return True  # Indicates a level up occurred
        
        self.save()
        return False
    
    def add_coins(self, amount: int):
        """Add or remove coins from the player"""
        self.coins += amount
        self.save()
    
    def can_afford(self, amount: int) -> bool:
        """Check if the player can afford something"""
        return self.coins >= amount
    
    def move_to(self, location: str):
        """Move the player to a new location"""
        self.current_location = location
        self.save()
    
    def get_cats(self):
        """Get all cats owned by the player"""
        query = "SELECT * FROM cats WHERE player_id = %s"
        return self.db.execute_query(query, (self.id,))
    
    def get_active_cat(self):
        """Get the player's active cat"""
        query = "SELECT * FROM cats WHERE player_id = %s AND is_active = TRUE LIMIT 1"
        results = self.db.execute_query(query, (self.id,))
        return results[0] if results else None
    
    def get_inventory(self):
        """Get the player's inventory"""
        query = """
            SELECT i.*, inv.quantity 
            FROM inventory inv 
            JOIN items i ON inv.item_id = i.id 
            WHERE inv.player_id = %s
        """
        return self.db.execute_query(query, (self.id,)) 