"""
Settings configuration for the Mutual Fund FAQ Assistant
"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database Configuration
    chroma_db_path: str = Field(default="./data/embeddings/chroma.db", env="CHROMA_DB_PATH")
    chroma_host: str = Field(default="localhost", env="CHROMA_HOST")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT")
    
    # Scraping Configuration
    scraping_delay: int = Field(default=2, env="SCRAPING_DELAY")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="USER_AGENT"
    )
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    concurrent_requests: int = Field(default=5, env="CONCURRENT_REQUESTS")
    
    # HDFC Mutual Fund URLs (Fixed - No other URLs allowed)
    hdfc_large_cap_url: str = Field(
        default="https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        env="HDFC_LARGE_CAP_URL"
    )
    hdfc_mid_cap_url: str = Field(
        default="https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
        env="HDFC_MID_CAP_URL"
    )
    hdfc_equity_url: str = Field(
        default="https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        env="HDFC_EQUITY_URL"
    )
    hdfc_focused_url: str = Field(
        default="https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
        env="HDFC_FOCUSED_URL"
    )
    hdfc_elss_url: str = Field(
        default="https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        env="HDFC_ELSS_URL"
    )
    
    # Data Storage Paths
    raw_data_path: str = Field(default="./data/raw", env="RAW_DATA_PATH")
    processed_data_path: str = Field(default="./data/processed", env="PROCESSED_DATA_PATH")
    embeddings_path: str = Field(default="./data/embeddings", env="EMBEDDINGS_PATH")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", env="LOG_FILE")
    log_rotation: str = Field(default="daily", env="LOG_ROTATION")
    log_retention: int = Field(default=7, env="LOG_RETENTION")
    
    # Processing Configuration
    chunk_size: int = Field(default=512, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=50, env="CHUNK_OVERLAP")
    max_document_size: int = Field(default=1000000, env="MAX_DOCUMENT_SIZE")
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    
    # Compliance Settings
    max_response_sentences: int = Field(default=3, env="MAX_RESPONSE_SENTENCES")
    require_citation: bool = Field(default=True, env="REQUIRE_CITATION")
    facts_only_mode: bool = Field(default=True, env="FACTS_ONLY_MODE")
    
    # API Configuration
    api_host: str = Field(default="localhost", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    
    # Google AI Studio Configuration
    google_ai_studio_api_key: str = Field(default="", env="GOOGLE_AI_STUDIO_API_KEY")
    encryption_key: str = Field(default="default_secret_key", env="ENCRYPTION_KEY")
    
    # Development Settings
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def hdfc_urls(self) -> List[str]:
        """Get all HDFC mutual fund URLs"""
        return [
            self.hdfc_large_cap_url,
            self.hdfc_mid_cap_url,
            self.hdfc_equity_url,
            self.hdfc_focused_url,
            self.hdfc_elss_url,
        ]
    
    @property
    def hdfc_fund_names(self) -> List[str]:
        """Get HDFC fund names corresponding to URLs"""
        return [
            "hdfc-large-cap",
            "hdfc-mid-cap", 
            "hdfc-equity",
            "hdfc-focused",
            "hdfc-elss",
        ]
    
    def get_fund_url(self, fund_name: str) -> str:
        """Get URL for a specific fund name"""
        fund_mapping = dict(zip(self.hdfc_fund_names, self.hdfc_urls))
        return fund_mapping.get(fund_name, "")
    
    def ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            Path(self.raw_data_path),
            Path(self.processed_data_path),
            Path(self.embeddings_path),
            Path(self.log_file).parent,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate_urls(self) -> bool:
        """Validate that all URLs are properly formatted"""
        for url in self.hdfc_urls:
            if not url.startswith("https://groww.in/mutual-funds/"):
                return False
        return True


# Global settings instance
settings = Settings()
