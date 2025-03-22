import csv
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import our models
sys.path.append(str(Path(__file__).parent.parent))

from models.database import DatabaseManager

def ensure_image_directories():
    """Create necessary image directories if they don't exist"""
    image_dirs = ['images', 'images/items']
    for dir_path in image_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Ensured directory exists: {dir_path}")

def import_items_from_csv(csv_path):
    """Import items from a CSV file into the database"""
    db = DatabaseManager()
    
    try:
        # Ensure image directories exist
        ensure_image_directories()
        
        # Start a transaction for all inserts
        db.start_transaction()
        
        # First, let's get existing items to avoid duplicates
        existing_items = db.execute_query("SELECT name FROM items")
        existing_names = {item['name'] for item in existing_items}
        
        # Read the CSV file
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            items_to_insert = []
            
            for row in reader:
                # Skip if item already exists
                if row['name'] in existing_names:
                    print(f"Skipping existing item: {row['name']}")
                    continue
                
                # Calculate value based on rarity
                value = {
                    'common': 100,
                    'uncommon': 250,
                    'rare': 500,
                    'epic': 1000,
                    'legendary': 2500
                }.get(row['rarity'].lower(), 100)
                
                # Generate image path (for now, all use the same image)
                image_path = 'images/items/eternal_scroll_of_meowgic.png'
                
                items_to_insert.append((
                    row['name'],
                    row['description'],
                    row['type'],
                    row['rarity'],
                    value,
                    image_path
                ))
        
        if items_to_insert:
            # Insert new items
            insert_query = """
                INSERT INTO items (name, description, type, rarity, value, image_path)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            for item in items_to_insert:
                try:
                    db.execute_query(insert_query, item)
                    print(f"Added item: {item[0]} (Image: {item[5]})")
                except Exception as e:
                    print(f"Error adding item {item[0]}: {str(e)}")
        
        # Commit the transaction
        db.end_transaction()
        print(f"\nSuccessfully imported {len(items_to_insert)} items!")
        
    except Exception as e:
        print(f"Error during import: {str(e)}")
        db.end_transaction()
        return False
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python import_items.py <path_to_csv>")
        print("Example: python import_items.py data/Whiskerverse_Lore_Item_List.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
    
    success = import_items_from_csv(csv_path)
    if not success:
        print("Import failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 