-- News Articles Table for Module 6
-- This table stores saved news articles from the News API

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
