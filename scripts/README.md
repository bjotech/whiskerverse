# Whiskerverse Scripts

This directory contains utility scripts for managing the Whiskerverse game.

## Import Items Script

The `import_items.py` script allows you to import items from a CSV file into the game database.

### CSV Format

Your CSV file should have the following columns:
- `name`: The name of the item
- `description`: A description of the item
- `type`: Must be one of: weapon, armor, potion, material, misc
- `rarity`: Must be one of: common, uncommon, rare, epic, legendary

Example CSV:
```csv
name,description,type,rarity
Frayed Pawstone,A common material that enhances your health.,material,common
Mystic Clawfang,A rare weapon that enhances your speed.,weapon,rare
```

### Item Values

The script automatically assigns values to items based on their rarity:
- Common: 100 coins
- Uncommon: 250 coins
- Rare: 500 coins
- Epic: 1000 coins
- Legendary: 2500 coins

### Usage

1. Place your CSV file in the `data` directory
2. Run the script:
```bash
python scripts/import_items.py data/your_items.csv
```

### Features

- Skips existing items to avoid duplicates
- Uses transactions for data consistency
- Provides detailed feedback during import
- Handles errors gracefully

### Example

To import the provided item list:
```bash
python scripts/import_items.py data/Whiskerverse_Lore_Item_List.csv
``` 