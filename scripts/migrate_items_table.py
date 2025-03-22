import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import our models
sys.path.append(str(Path(__file__).parent.parent))

from models.database import DatabaseManager

def migrate_items_table():
    """Add image_path column to items table if it doesn't exist"""
    db = DatabaseManager()
    
    try:
        # Check if column exists
        check_column_query = """
        SELECT COUNT(*) as count
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = %s
        AND TABLE_NAME = 'items'
        AND COLUMN_NAME = 'image_path'
        """
        
        result = db.execute_query(check_column_query, (db.database,))
        column_exists = result[0]['count'] > 0
        
        if not column_exists:
            print("Adding image_path column to items table...")
            
            # Add the column
            alter_table_query = """
            ALTER TABLE items
            ADD COLUMN image_path VARCHAR(255) DEFAULT 'images/items/eternal_scroll_of_meowgic.png'
            """
            
            db.execute_query(alter_table_query)
            print("Successfully added image_path column!")
        else:
            print("image_path column already exists in items table.")
        
        return True
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        return False

def main():
    success = migrate_items_table()
    if not success:
        print("Migration failed!")
        sys.exit(1)
    else:
        print("Migration completed successfully!")

if __name__ == "__main__":
    main() 