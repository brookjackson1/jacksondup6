-- NASA APOD (Astronomy Picture of the Day) Table
-- This table stores saved NASA Astronomy Pictures

CREATE TABLE IF NOT EXISTS nasa_apod (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    date DATE NOT NULL,
    url TEXT NOT NULL,
    explanation TEXT,
    media_type VARCHAR(50) DEFAULT 'image',
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add index for faster queries
CREATE INDEX idx_date ON nasa_apod(date);
CREATE INDEX idx_saved_at ON nasa_apod(saved_at);
