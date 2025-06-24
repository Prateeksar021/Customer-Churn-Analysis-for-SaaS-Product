import pandas as pd
import sqlite3
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl.log'),
        logging.StreamHandler()
    ]
)

def initialize_database():
    """Create SQLite database with required tables"""
    try:
        conn = sqlite3.connect('user_activity.db')
        cursor = conn.cursor()
        
        # Main activity table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                user_id TEXT,
                activity_date TEXT,
                session_duration REAL,
                feature_used TEXT,
                plan_type TEXT,
                location TEXT,
                load_timestamp TEXT,
                is_new INTEGER DEFAULT 0,
                is_updated INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, activity_date)
            )
        ''')
        
        # ETL log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS etl_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT,
                load_timestamp TEXT,
                rows_inserted INTEGER,
                rows_updated INTEGER,
                status TEXT
            )
        ''')
        
        conn.commit()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        conn.close()

def process_data_file(file_path):
    """Process a single CSV file with CDC tracking"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
            
        conn = sqlite3.connect('user_activity.db')
        cursor = conn.cursor()
        df = pd.read_csv(file_path)
        load_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inserted = 0
        updated = 0
        
        for _, row in df.iterrows():
            # Check if record exists
            cursor.execute('''
                SELECT session_duration, feature_used 
                FROM user_activity 
                WHERE user_id=? AND activity_date=?
            ''', (row['user_id'], row['activity_date']))
            
            existing = cursor.fetchone()
            
            if not existing:
                # Insert new record
                cursor.execute('''
                    INSERT INTO user_activity (
                        user_id, activity_date, session_duration,
                        feature_used, plan_type, location,
                        load_timestamp, is_new
                    ) VALUES (?,?,?,?,?,?,?,1)
                ''', (
                    row['user_id'], row['activity_date'],
                    row['session_duration'], row['feature_used'],
                    row['plan_type'], row['location'], load_time
                ))
                inserted += 1
            else:
                # Update if changes detected
                if (existing[0] != row['session_duration'] or 
                    existing[1] != row['feature_used']):
                    cursor.execute('''
                        UPDATE user_activity 
                        SET session_duration=?, feature_used=?,
                            load_timestamp=?, is_updated=1
                        WHERE user_id=? AND activity_date=?
                    ''', (
                        row['session_duration'], row['feature_used'],
                        load_time, row['user_id'], row['activity_date']
                    ))
                    updated += 1
        
        # Log this ETL operation
        cursor.execute('''
            INSERT INTO etl_log (
                file_name, load_timestamp,
                rows_inserted, rows_updated, status
            ) VALUES (?,?,?,?,?)
        ''', (file_path, load_time, inserted, updated, 'SUCCESS'))
        
        conn.commit()
        logging.info(f"Processed {file_path}: {inserted} inserts, {updated} updates")
        return True
        
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        cursor.execute('''
            INSERT INTO etl_log (
                file_name, load_timestamp,
                rows_inserted, rows_updated, status
            ) VALUES (?,?,?,?,?)
        ''', (file_path, load_time, 0, 0, 'FAILED'))
        conn.commit()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # Initialize database
    initialize_database()
    
    # Process all data files
    data_files = [
        "user_activity_day1.csv",
        "user_activity_day2.csv",
        "user_activity_day3.csv"
    ]
    
    for file in data_files:
        if os.path.exists(file):
            process_data_file(file)
        else:
            logging.warning(f"File {file} not found. Skipping...")
    
    logging.info("ETL process completed")