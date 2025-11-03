# Module 6 - News API Integration Project

This is a Flask application that integrates with News API to display and manage current news headlines and trending stories.

## Features

- **News API Integration**: Fetches and displays top headlines from thousands of news sources worldwide
- **Database Management**: Stores favorite articles with full CRUD operations (Create, Read, Update, Delete)
- **Search & Categories**: Search for news by keyword or browse by category (business, technology, sports, etc.)
- **Responsive UI**: Professional Bootstrap styling with modal dialogs
- **Error Handling**: Comprehensive error handling for API calls and database operations

## API Selection

**News API**
- API Documentation: https://newsapi.org/
- Endpoints:
  - Top Headlines: https://newsapi.org/v2/top-headlines
  - Everything: https://newsapi.org/v2/everything
- Features: Current news headlines, article search, category filtering, and source filtering

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Configuration
Create a `.env` file in the root directory with your database credentials:
```
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=3306
DB_NAME=your_database_name
NEWS_API_KEY=your_news_api_key
```

Get your free News API key at: https://newsapi.org/register

### 3. Create Database Table
Run the database setup script:
```bash
python create_news_table.py
```

Or manually run `database/news_articles_table.sql` in your MySQL database.

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 5. Access the News Feature
Navigate to `http://localhost:5000/news` or click "News & Trends" in the navigation bar.

## Project Structure
As your project grows, consider adding these organizational folders:

### Recommended Additions
- `docs/` - API documentation, setup guides, deployment notes
- `docs/features/` - Feature specifications and requirements  
- `docs/architecture/` - System design documents
- `tests/` - Unit and integration tests
- `migrations/` - Database schema changes (if using Flask-Migrate)
- `config/` - Environment-specific configurations
- `.github/workflows/` - CI/CD pipelines (if using GitHub)
- `.vscode/` - Cursor/VS Code workspace settings

### Documentation Files
- `CHANGELOG.md` - Track version changes and updates
- `.env.example` - Template for environment variables

**Note**: Only create these folders as your project actually needs them. Don't over-structure early.

## AI Workflow Integration
This folder includes prompts that should be copy/pasted into your docs/commands folder and then used by tagging them in the chat (e.g. @plan_feature.md) and providing additional context such as the description of your feature.

Feel free to customize them to your needs! These are really just a starting point and what works for me.

[![The Perfect Cursor AI Workflow (3 Simple Steps)](https://img.youtube.com/vi/Jem2yqhXFaU/0.jpg)](https://youtu.be/Jem2yqhXFaU)
> 🎥 The Perfect Cursor AI Workflow (3 Simple Steps)

# Example Use
## Create Brief
Used for establishing the bigger picture context of what this project is about which can be helpful to plan new features.
```
@create_brief.md 

We are building an application to help dungeon masters plan their D&D campaigns and it's going to be called Dragonroll. It will include a variety of different tools, such as a random map generator and bc generator, loot generator and so on. We will use ai and allow the dungeon master to input certain prompts or use the tools directly.
```

## Plan Feature
Used to create a technical plan for a new feature. Focuses on the technical requirements - NOT product manager context bloat or overly specific code details.
```
@plan_feature.md 

We want to add a new page that is going to be our NPC generator. To implement this, we are going to use the open ai api to generate the description of the npc as well as a name And we'll also generate an image for the npc using the open ai gpt-image-1 model.
```

## Code Review
Used to review the successful completion of a plan in a separate chat (and yes, it's this minimal)
```
@code_review.md
@0001_PLAN.md
```

## Documentation Writing
Used to create comprehensive documentation for the plan, review, and implementation.
```
@write_docs.md
@0001_PLAN.md
@0001_REVIEW.md
```