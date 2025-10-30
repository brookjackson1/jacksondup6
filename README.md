# Module 6 - NASA API Integration Project

This is a Flask application that integrates with the NASA Astronomy Picture of the Day (APOD) API to display and manage astronomy pictures.

## Features

- **NASA APOD Integration**: Fetches and displays daily astronomy pictures from NASA's API
- **Database Management**: Stores favorite pictures with full CRUD operations (Create, Read, Update, Delete)
- **Date Search**: Search for pictures from any specific date in NASA's archive
- **Responsive UI**: Professional Bootstrap styling with modal dialogs
- **Error Handling**: Comprehensive error handling for API calls and database operations

## API Selection

**NASA APOD (Astronomy Picture of the Day) API**
- API Documentation: https://api.nasa.gov/
- Endpoint: https://api.nasa.gov/planetary/apod
- Features: Daily astronomy pictures with titles, dates, explanations, and high-resolution images

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
NASA_API_KEY=your_nasa_api_key
```

### 3. Create Database Table
Run the SQL script to create the required table:
```bash
python -c "import pymysql; import os; from dotenv import load_dotenv; load_dotenv(); conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME')); [conn.cursor().execute(cmd.strip()) for cmd in open('database/nasa_apod_table.sql').read().split(';') if cmd.strip()]; conn.commit(); conn.close()"
```

Or manually run `database/nasa_apod_table.sql` in your MySQL database.

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 5. Access the NASA APOD Feature
Navigate to `http://localhost:5000/nasa` or click "NASA APOD" in the navigation bar.

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