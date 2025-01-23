import databases

DATABASE_URL = "sqlite:///./blog.db"
database = databases.Database(DATABASE_URL)
