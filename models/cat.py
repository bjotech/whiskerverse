from .base_model import BaseModel
import random
import csv
import os

class Cat(BaseModel):
    table_name = 'cats'

    # Load cat breeds and stats from CSV
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Whiskerverse_Cats_List.csv')
    BREEDS = []
    RARITY_WEIGHTS = {}
    BREED_STATS = {}

    @classmethod
    def load_cat_data(cls):
        cls.BREEDS = []
        cls.RARITY_WEIGHTS = {}
        cls.BREED_STATS = {}
        try:
            with open(cls.DATA_FILE, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    breed = row['breed']
                    rarity = row['rarity']
                    health = int(row['health'])
                    attack = int(row['attack'])
                    defense = int(row['defense'])
                    speed = int(row['speed'])
                    cls.BREEDS.append(breed)
                    if rarity not in cls.RARITY_WEIGHTS:
                        cls.RARITY_WEIGHTS[rarity] = []
                    cls.RARITY_WEIGHTS[rarity].append(breed)
                    cls.BREED_STATS[breed] = {
                        'health': health,
                        'attack': attack,
                        'defense': defense,
                        'speed': speed
                    }
        except Exception as e:
            print(f"Error loading cat data from CSV: {e}")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id')
        self.player_id = kwargs.get('player_id')
        self.name = kwargs.get('name')
        self.breed = kwargs.get('breed')
        self.level = kwargs.get('level', 1)
        self.experience = kwargs.get('experience', 0)
        # Use breed stats from loaded CSV
        breed_stats = self.BREED_STATS.get(self.breed, {'health': 100, 'attack': 10, 'defense': 10, 'speed': 10})
        self.health = kwargs.get('health', breed_stats['health'])
        self.attack = kwargs.get('attack', breed_stats['attack'])
        self.defense = kwargs.get('defense', breed_stats['defense'])
        self.speed = kwargs.get('speed', breed_stats['speed'])
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

# Load data at class initialization
Cat.load_cat_data()