#!/usr/bin/env python3
import os
import glob
import psycopg2
import logging
import time
import sys
import importlib.util

from psycopg2.extensions import AsIs

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# PostgreSQL connection details
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'warranty_db')
DB_USER = os.environ.get('DB_USER', 'warranty_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'warranty_password')
DB_ADMIN_USER = os.environ.get('DB_ADMIN_USER', 'warracker_admin')
DB_ADMIN_PASSWORD = os.environ.get('DB_ADMIN_PASSWORD', 'change_this_password_in_production')

def get_db_connection(max_attempts=5, attempt_delay=5):
    """Get a connection to the PostgreSQL database with retry logic"""
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt}/{max_attempts})")
            
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            
            # Set autocommit to False for transaction control
            conn.autocommit = False
            
            logger.info("Database connection successful")
            return conn
            
        except Exception as e:
            logger.error(f"Database connection error (attempt {attempt}/{max_attempts}): {e}")
            
            if attempt < max_attempts:
                logger.info(f"Retrying in {attempt_delay} seconds...")
                time.sleep(attempt_delay)
            else:
                logger.error("Maximum connection attempts reached. Could not connect to database.")
                raise

def load_python_migration(file_path):
    """Load a Python migration module dynamically"""
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def apply_migrations():
    """Apply all SQL and Python migration files in the migrations directory"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create migrations table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Get list of migration files (both SQL and Python)
        migration_dir = os.path.dirname(os.path.abspath(__file__))
        sql_files = sorted(glob.glob(os.path.join(migration_dir, '*.sql')))
        py_files = sorted(glob.glob(os.path.join(migration_dir, '*.py')))
        # Filter out this script itself
        py_files = [f for f in py_files if os.path.basename(f) != 'apply_migrations.py']
        
        # Combine and sort all migration files by name
        all_migration_files = sorted(sql_files + py_files)
        
        if not all_migration_files:
            logger.info("No migration files found.")
            return
        
        # Get list of already applied migrations
        cur.execute("SELECT filename FROM migrations")
        applied_migrations = set([row[0] for row in cur.fetchall()])
        
        # Apply each migration file if not already applied
        for migration_file in all_migration_files:
            filename = os.path.basename(migration_file)
            
            if filename in applied_migrations:
                logger.info(f"Migration {filename} already applied, skipping.")
                continue
            
            logger.info(f"Applying migration: {filename}")
            
            try:
                if migration_file.endswith('.sql'):
                    # Apply SQL migration
                    with open(migration_file, 'r') as f:
                        sql = f.read()
                    
                    cur.execute(
                        sql,
                        {
                            "db_name": AsIs(DB_NAME),
                            "db_user": AsIs(DB_USER),
                            "db_admin_user": AsIs(DB_ADMIN_USER),
                            "db_admin_password": AsIs(DB_ADMIN_PASSWORD),
                        }
                    )
                elif migration_file.endswith('.py'):
                    # Apply Python migration
                    migration_module = load_python_migration(migration_file)
                    if hasattr(migration_module, 'upgrade'):
                        migration_module.upgrade(cur)
                    else:
                        logger.warning(f"Python migration {filename} does not have an upgrade function, skipping.")
                        continue
                
                # Record the migration as applied
                cur.execute(
                    "INSERT INTO migrations (filename) VALUES (%s)",
                    (filename,)
                )
                
                conn.commit()
                logger.info(f"Migration {filename} applied successfully")
                
            except Exception as e:
                conn.rollback()
                logger.error(f"Error applying migration {filename}: {e}")
                if migration_file.endswith('.sql'):
                    logger.error(f"\nQUERY: {sql}\n")
                raise
        
    except Exception as e:
        logger.error(f"Migration error: {e}")
        if conn:
            conn.rollback()
        raise
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        apply_migrations()
        logger.info("Migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration process failed: {e}")
        sys.exit(1) 
