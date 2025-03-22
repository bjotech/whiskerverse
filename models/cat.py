from .base_model import BaseModel
import random

class Cat(BaseModel):
    table_name = 'cats'
    
    BREEDS = [
        # Common breeds
        'Alley Cat', 'Domestic Shorthair', 'Tabby',
        # Uncommon breeds
        'Siamese', 'Persian', 'Maine Coon', 'Russian Blue',
        # Rare breeds
        'Sphynx', 'Bengal', 'Scottish Fold',
        # Epic breeds
        'Celestial', 'Shadow Walker', 'Mystic Whisker',
        # Legendary breeds
        'Ancient Guardian', 'Star Whisperer', 'Eternal Prowler'
    ]
    
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
        
        # Uncommon breeds - slightly better stats
        'Siamese': {'health': 95, 'attack': 14, 'defense': 10, 'speed': 15},
        'Persian': {'health': 110, 'attack': 11, 'defense': 14, 'speed': 8},
        'Maine Coon': {'health': 120, 'attack': 13, 'defense': 12, 'speed': 9},
        'Russian Blue': {'health': 100, 'attack': 12, 'defense': 13, 'speed': 12},
        
        # Rare breeds - specialized stats
        'Sphynx': {'health': 90, 'attack': 16, 'defense': 8, 'speed': 18},
        'Bengal': {'health': 105, 'attack': 15, 'defense': 11, 'speed': 16},
        'Scottish Fold': {'health': 115, 'attack': 14, 'defense': 15, 'speed': 10},
        
        # Epic breeds - powerful stats
        'Celestial': {'health': 130, 'attack': 18, 'defense': 16, 'speed': 15},
        'Shadow Walker': {'health': 120, 'attack': 20, 'defense': 14, 'speed': 18},
        'Mystic Whisker': {'health': 125, 'attack': 17, 'defense': 17, 'speed': 17},
        
        # Legendary breeds - exceptional stats
        'Ancient Guardian': {'health': 150, 'attack': 22, 'defense': 20, 'speed': 18},
        'Star Whisperer': {'health': 140, 'attack': 25, 'defense': 18, 'speed': 22},
        'Eternal Prowler': {'health': 145, 'attack': 23, 'defense': 19, 'speed': 20}
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.player_id = kwargs.get('player_id')
        self.name = kwargs.get('name')
        self.breed = kwargs.get('breed')
        self.level = kwargs.get('level', 1)
        self.experience = kwargs.get('experience', 0)
        self.health = kwargs.get('health', self.BREED_STATS[self.breed]['health'])
        self.attack = kwargs.get('attack', self.BREED_STATS[self.breed]['attack'])
        self.defense = kwargs.get('defense', self.BREED_STATS[self.breed]['defense'])
        self.speed = kwargs.get('speed', self.BREED_STATS[self.breed]['speed'])
        self.is_active = kwargs.get('is_active', False)
        self.created_at = kwargs.get('created_at')
    
    @classmethod
    def generate_random(cls, player_id: int, name: str, rarity: str = None):
        """Generate a random cat with the given rarity"""
        if rarity is None:
            # Default rarity weights
            weights = [0.5, 0.25, 0.15, 0.08, 0.02]  # common, uncommon, rare, epic, legendary
            rarity = random.choices(list(cls.RARITY_WEIGHTS.keys()), weights=weights)[0]
        
        breed = random.choice(cls.RARITY_WEIGHTS[rarity])
        base_stats = cls.BREED_STATS[breed]
        
        # Add some randomness to stats (±10%)
        stats = {
            stat: int(value * random.uniform(0.9, 1.1))
            for stat, value in base_stats.items()
        }
        
        cat = cls(
            player_id=player_id,
            name=name,
            breed=breed,
            health=stats['health'],
            attack=stats['attack'],
            defense=stats['defense'],
            speed=stats['speed']
        )
        cat.save()
        return cat
    
    def add_experience(self, amount: int):
        """Add experience points and handle level ups"""
        self.experience += amount
        leveled_up = False
        
        # Check for level up
        # Experience needed for next level = current_level * 800
        while self.experience >= self.level * 800:
            self.experience -= self.level * 800
            self.level += 1
            
            # Increase stats on level up
            self.health += int(self.health * 0.1)
            self.attack += int(self.attack * 0.1)
            self.defense += int(self.defense * 0.1)
            self.speed += int(self.speed * 0.1)
            
            leveled_up = True
        
        self.save()
        return leveled_up
    
    def set_active(self, active: bool = True):
        """Set this cat as the active cat for battles"""
        if active:
            # First, deactivate all other cats for this player
            self.db.execute_query(
                "UPDATE cats SET is_active = FALSE WHERE player_id = %s",
                (self.player_id,)
            )
        
        self.is_active = active
        self.save()
    
    def calculate_damage(self, target, move_power: int):
        """Calculate damage for an attack move"""
        # Basic damage formula: (attack * move_power) / target_defense
        base_damage = (self.attack * move_power) / target.defense
        
        # Add randomness (±20%)
        variance = random.uniform(0.8, 1.2)
        
        # Critical hit chance (10%)
        if random.random() < 0.1:
            variance *= 1.5
        
        return int(base_damage * variance) 