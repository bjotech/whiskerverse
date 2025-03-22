from ..repositories.player_repository import PlayerRepository
from ..repositories.cat_repository import CatRepository
from ..repositories.inventory_repository import InventoryRepository
from .cat_service import CatService

class PlayerService:
    def __init__(self):
        self.player_repo = PlayerRepository()
        self.cat_repo = CatRepository()
        self.inventory_repo = InventoryRepository()
        self.cat_service = CatService()
        self.db = self.player_repo.db
    
    def get_or_create_player(self, discord_id: int, username: str):
        player = self.player_repo.get_by_id(discord_id)
        if not player:
            player = self.player_repo.create(discord_id, username)
        return player
    
    def start_adventure(self, discord_id: int, username: str, cat_name: str):
        """Initialize a new player's adventure with their first cat"""
        try:
            self.db.start_transaction()
            
            # Get or create player
            player = self.get_or_create_player(discord_id, username)
            
            # Check if player already has cats
            existing_cats = self.cat_repo.get_player_cats(discord_id)
            if existing_cats:
                self.db.end_transaction()
                return False, "Already started adventure", None
            
            # Generate starter cat
            breed = self.cat_service.get_random_breed("common")
            stats = self.cat_service.generate_stats(breed)
            
            # Create the cat
            cat = self.cat_repo.create(
                player_id=discord_id,
                name=cat_name,
                breed=breed,
                stats=stats
            )
            
            # Set as active cat
            self.cat_repo.set_active(cat['id'], discord_id)
            
            self.db.end_transaction()
            return True, "Adventure started!", cat
            
        except Exception as e:
            self.db.end_transaction()
            raise
    
    def get_profile(self, discord_id: int):
        """Get complete player profile including cats and inventory"""
        player = self.player_repo.get_by_id(discord_id)
        if not player:
            return None
        
        active_cat = self.cat_repo.get_active_cat(discord_id)
        cats = self.cat_repo.get_player_cats(discord_id)
        inventory = self.inventory_repo.get_player_items(discord_id)
        
        return {
            'player': player,
            'active_cat': active_cat,
            'cats': cats,
            'inventory': inventory
        } 