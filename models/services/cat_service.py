from ..repositories.cat_repository import CatRepository
import random

class CatService:
    RARITY_WEIGHTS = {
        'common': ['Alley Cat', 'Domestic Shorthair', 'Tabby'],
        'uncommon': ['Siamese', 'Persian', 'Maine Coon', 'Russian Blue'],
        'rare': ['Sphynx', 'Bengal', 'Scottish Fold'],
        'epic': ['Celestial', 'Shadow Walker', 'Mystic Whisker'],
        'legendary': ['Ancient Guardian', 'Star Whisperer', 'Eternal Prowler']
    }
    
    BREED_STATS = {
        # Common breeds - balanced stats
        'Alley Cat': {'health': 100, 'attack': 10, 'defense': 10, 'speed': 10},
        'Domestic Shorthair': {'health': 95, 'attack': 12, 'defense': 9, 'speed': 11},
        'Tabby': {'health': 90, 'attack': 11, 'defense': 11, 'speed': 12},
        
        # Uncommon breeds
        'Siamese': {'health': 95, 'attack': 14, 'defense': 10, 'speed': 15},
        'Persian': {'health': 110, 'attack': 11, 'defense': 14, 'speed': 8},
        'Maine Coon': {'health': 120, 'attack': 13, 'defense': 12, 'speed': 9},
        'Russian Blue': {'health': 100, 'attack': 12, 'defense': 13, 'speed': 12},
        
        # Rare breeds
        'Sphynx': {'health': 90, 'attack': 16, 'defense': 8, 'speed': 18},
        'Bengal': {'health': 105, 'attack': 15, 'defense': 11, 'speed': 16},
        'Scottish Fold': {'health': 115, 'attack': 14, 'defense': 15, 'speed': 10},
        
        # Epic breeds
        'Celestial': {'health': 130, 'attack': 18, 'defense': 16, 'speed': 15},
        'Shadow Walker': {'health': 120, 'attack': 20, 'defense': 14, 'speed': 18},
        'Mystic Whisker': {'health': 125, 'attack': 17, 'defense': 17, 'speed': 17},
        
        # Legendary breeds
        'Ancient Guardian': {'health': 150, 'attack': 22, 'defense': 20, 'speed': 18},
        'Star Whisperer': {'health': 140, 'attack': 25, 'defense': 18, 'speed': 22},
        'Eternal Prowler': {'health': 145, 'attack': 23, 'defense': 19, 'speed': 20}
    }
    
    def __init__(self):
        self.cat_repo = CatRepository()
    
    def get_random_breed(self, rarity: str = None):
        """Get a random breed based on rarity"""
        if rarity:
            return random.choice(self.RARITY_WEIGHTS[rarity])
        
        # Default rarity weights if none specified
        weights = [0.5, 0.25, 0.15, 0.08, 0.02]  # common to legendary
        chosen_rarity = random.choices(list(self.RARITY_WEIGHTS.keys()), weights=weights)[0]
        return random.choice(self.RARITY_WEIGHTS[chosen_rarity])
    
    def generate_stats(self, breed: str):
        """Generate randomized stats based on breed"""
        base_stats = self.BREED_STATS[breed]
        return {
            stat: int(value * random.uniform(0.9, 1.1))
            for stat, value in base_stats.items()
        }
    
    def rename_cat(self, cat_id: int, player_id: int, new_name: str):
        """Rename a cat if it belongs to the player"""
        cat = self.cat_repo.get_by_id(cat_id)
        if not cat or cat['player_id'] != player_id:
            return False, "You don't own this cat!"
        
        self.cat_repo.update_name(cat_id, player_id, new_name)
        return True, f"Successfully renamed your cat to {new_name}!"
    
    def switch_active_cat(self, cat_id: int, player_id: int):
        """Switch the player's active cat"""
        cat = self.cat_repo.get_by_id(cat_id)
        if not cat or cat['player_id'] != player_id:
            return False, "You don't own this cat!"
        
        self.cat_repo.set_active(cat_id, player_id)
        return True, f"Successfully switched to {cat['name']}!" 