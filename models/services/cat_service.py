from ..repositories.cat_repository import CatRepository
import random

class CatService:
    def __init__(self):
        self.cat_repo = CatRepository()
        
        # Define breed pools by rarity
        self.RARITY_WEIGHTS = {
            'common': [
                'Tabby', 'Domestic Shorthair', 'Domestic Longhair',
                'Mixed Breed', 'Alley Cat'
            ],
            'uncommon': [
                'Siamese', 'Persian', 'Maine Coon', 'Russian Blue',
                'American Shorthair'
            ],
            'rare': [
                'Bengal', 'Sphynx', 'Scottish Fold', 'British Shorthair',
                'Ragdoll'
            ],
            'epic': [
                'Mystic Shadowpaw', 'Celestial Whisker', 'Astral Prowler',
                'Ethereal Purrer', 'Void Walker'
            ],
            'legendary': [
                'Ancient Mau', 'Spectral Tiger', 'Phoenix Cat',
                'Dragon Kitten', 'Cosmic Feline'
            ]
        }
        
        # Define base stats by rarity
        self.BASE_STATS = {
            'common': {'min': 8, 'max': 12},
            'uncommon': {'min': 10, 'max': 15},
            'rare': {'min': 12, 'max': 18},
            'epic': {'min': 15, 'max': 22},
            'legendary': {'min': 18, 'max': 25}
        }
    
    def get_random_breed(self, rarity=None):
        """Get a random breed, optionally from a specific rarity tier"""
        if not rarity:
            # Choose rarity based on weights
            weights = {
                'common': 0.5,
                'uncommon': 0.25,
                'rare': 0.15,
                'epic': 0.08,
                'legendary': 0.02
            }
            rarity = random.choices(
                list(weights.keys()),
                weights=list(weights.values())
            )[0]
        
        return random.choice(self.RARITY_WEIGHTS[rarity])
    
    def generate_stats(self, breed):
        """Generate random stats based on breed rarity"""
        # Find rarity of the breed
        rarity = next(
            rarity for rarity, breeds in self.RARITY_WEIGHTS.items()
            if breed in breeds
        )
        
        stat_range = self.BASE_STATS[rarity]
        return {
            'health': random.randint(stat_range['min'], stat_range['max']),
            'attack': random.randint(stat_range['min'], stat_range['max']),
            'defense': random.randint(stat_range['min'], stat_range['max']),
            'speed': random.randint(stat_range['min'], stat_range['max'])
        }
    
    def generate_random(self, player_id=None, name=None):
        """Generate a random cat with random breed and stats"""
        breed = self.get_random_breed()
        stats = self.generate_stats(breed)
        
        cat_data = {
            'player_id': player_id,
            'name': name or "Wild Cat",
            'breed': breed,
            'level': 1,
            'experience': 0,
            'health': stats['health'],
            'attack': stats['attack'],
            'defense': stats['defense'],
            'speed': stats['speed'],
            'is_active': False
        }
        
        return cat_data
    
    def save_cat(self, cat_data):
        """Save a cat to the database"""
        return self.cat_repo.create(
            player_id=cat_data['player_id'],
            name=cat_data['name'],
            breed=cat_data['breed'],
            stats={
                'health': cat_data['health'],
                'attack': cat_data['attack'],
                'defense': cat_data['defense'],
                'speed': cat_data['speed']
            }
        )
    
    def switch_active_cat(self, cat_id: int, player_id: int):
        """Switch the player's active cat"""
        # Verify cat exists and belongs to player
        cat = self.cat_repo.get_by_id(cat_id)
        if not cat:
            return False, "Cat not found"
        if cat['player_id'] != player_id:
            return False, "This cat doesn't belong to you"
        
        # Set as active
        self.cat_repo.set_active(cat_id, player_id)
        return True, f"{cat['name']} is now your active cat!"
    
    def rename_cat(self, cat_id: int, player_id: int, new_name: str):
        """Rename a cat"""
        # Verify cat exists and belongs to player
        cat = self.cat_repo.get_by_id(cat_id)
        if not cat:
            return False, "Cat not found"
        if cat['player_id'] != player_id:
            return False, "This cat doesn't belong to you"
        
        # Update name
        self.cat_repo.update_name(cat_id, player_id, new_name)
        return True, f"Successfully renamed to {new_name}!" 