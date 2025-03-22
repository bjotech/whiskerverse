# Whiskerverse Scripts

This directory contains utility scripts for managing the Whiskerverse game.

## Database Migration Script

The `migrate_items_table.py` script adds the image_path column to the existing items table.

### Usage

Run the migration script before importing items:
```bash
python scripts/migrate_items_table.py
```

This script:
- Checks if the image_path column exists
- Adds it if it doesn't exist
- Sets a default value pointing to eternal_scroll_of_meowgic.png
- Is safe to run multiple times (won't duplicate the column)

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

### Item Images

The script handles item images in the following way:
1. Creates necessary directories:
   - `images/`
   - `images/items/`
2. Currently assigns all items to use `images/items/eternal_scroll_of_meowgic.png`
3. When you want to add unique images:
   - Place the image in `images/items/`
   - Update the item's `image_path` in the database
   - Recommended image format: PNG
   - Recommended size: 128x128 pixels

### Setup Steps

1. Run the migration script to add image support:
```bash
python scripts/migrate_items_table.py
```

2. Create the images directory and add the default image:
```bash
mkdir -p images/items
# Add eternal_scroll_of_meowgic.png to images/items/
```

3. Place your CSV file in the `data` directory

4. Run the import script:
```bash
python scripts/import_items.py data/your_items.csv
```

### Features

- Creates necessary image directories automatically
- Skips existing items to avoid duplicates
- Uses transactions for data consistency
- Provides detailed feedback during import
- Handles errors gracefully

### Example

To import the provided item list:
```bash
python scripts/import_items.py data/Whiskerverse_Lore_Item_List.csv
```

### Future Image Updates

To update an item's image later:
```sql
UPDATE items 
SET image_path = 'images/items/your_unique_image.png' 
WHERE name = 'Item Name';
``` 