"""
Configuration Module

This module defines the application configuration using Pydantic's BaseSettings.
It automatically loads settings from environment variables and/or a .env file.
It also performs type conversion and validation.
"""

import os
from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

# --- 1. Determine which .env file to load ---
# We check an environment variable 'ENVIRONMENT' to decide which file to load.
# Default to 'development' if not set.
#
# To run in production: ENVIRONMENT=production python app.py
# To run in development: python app.py (or ENVIRONMENT=development python app.py)
#
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
env_file = ".env.prod" if ENVIRONMENT == "production" else ".env"

print(f"Loading settings from: {env_file} (ENVIRONMENT='{ENVIRONMENT}')")


# --- 2. Define the Settings Class ---
class Settings(BaseSettings):
    """
    Application settings. Values are loaded from environment variables.
    Type hints are used for automatic type conversion and validation.
    """
    
    # Define which .env file(s) to load.
    model_config = SettingsConfigDict(
        env_file=env_file, 
        env_file_encoding='utf-8', 
        extra='ignore'
    )

    # --- Application ---
    # We use Field(alias=...) to map the OS environment variable name 
    # (e.g., 'ENVIRONMENT') to the internal attribute name (e.g., 'ENV').
    ENV: Literal['development', 'production', 'test'] = Field(
        default='development', 
        alias='ENVIRONMENT'
    )
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # --- Database ---
    # DATABASE_URL is for PostgreSQL (optional), DATABASE_PATH is for JSON/SQLite fallback.
    DATABASE_URL: str | None = None
    DATABASE_PATH: str = "./data/production.db"

    # --- OpenAI (Secret Management) ---
    # Use `SecretStr` for sensitive values. This field is REQUIRED (no default).
    OPENAI_API_KEY: SecretStr

    # --- Logging ---
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # --- Branding (Static Constants) ---
    # Symbols removed: (TM) used instead of ™
    COMPANY_NAME: str = 'OlympusMont Systems LLC'
    PRODUCT_NAME: str = 'DisciplineAI Assistant (TM)'
    TAGLINE: str = 'AI Efficiency, Software development and Automation Consulting'
    CORE_ENGINE: str = 'CGC CORE (TM)'
    VERSION: str = '1.0.0'

    def display(self):
        """Prints a safe summary of the configuration."""
        print("--- Configuration Summary ---")
        print(f"  Environment: {self.ENV}")
        print(f"  Host / Port: {self.HOST}:{self.PORT}")
        print(f"  Log Level:   {self.LOG_LEVEL}")
        
        # SecretStr redacts the key automatically when printed
        print(f"  OpenAI Key:  {self.OPENAI_API_KEY}")
        print("-------------------------------")
        
    @property
    def effective_db(self) -> str:
        """Returns the active database connection string (URL or Path)."""
        return self.DATABASE_URL or self.DATABASE_PATH


# --- 3. Create a single, validated instance ---
# This code runs when the file is imported.
try:
    # Create the global config instance
    config = Settings()

    # Optional: Display the config on startup
    # config.display()

except ValidationError as e:
    # Emojis removed: ❌ replaced with [ERROR]
    print("[ERROR] CONFIGURATION ERROR: Failed to load settings.")
    # Pydantic's error message is very clear about what is missing
    print(e)
    exit(1)