import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# SQL to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS news_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) DEFAULT 'Unknown',
    description TEXT,
    url TEXT NOT NULL,
    url_to_image TEXT,
    published_at VARCHAR(50),
    source_name VARCHAR(255),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_url (url(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

try:
    # Connect to database
    connection = pymysql.connect(**db_config)
    print("Connected to database successfully!")

    # Create table
    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)
        print("[SUCCESS] news_articles table created successfully!")

    connection.commit()
    connection.close()
    print("[SUCCESS] Database setup complete!")

except Exception as e:
    print(f"[ERROR] {e}")
