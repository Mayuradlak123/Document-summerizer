import os
from dotenv import load_dotenv

# Load env file
load_dotenv()

class Settings:
    # General App Config
    APP_NAME: str = "Multi-Model Document Summarizer Agent"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Groq model IDs. Groq retires models regularly, so these are env-overridable.
    # Run `curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models`
    # to see what the current key actually has access to.
    GROQ_MODEL_FAST: str = os.getenv("GROQ_MODEL_FAST", "openai/gpt-oss-20b")
    GROQ_MODEL_HEAVY: str = os.getenv("GROQ_MODEL_HEAVY", "openai/gpt-oss-120b")
    GROQ_MODEL_JSON: str = os.getenv("GROQ_MODEL_JSON", "openai/gpt-oss-120b")
    GROQ_MODEL_VISION: str = os.getenv("GROQ_MODEL_VISION", "")
    
    # LangSmith Configuration
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "document-summarizer-agent")
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    
    # Chroma Config
    CHROMA_API_KEY: str = os.getenv("CHROMA_API_KEY", "")
    CHROMA_TENANT: str = os.getenv("CHROMA_TENANT", "default_tenant")
    CHROMA_DATABASE: str = os.getenv("CHROMA_DATABASE", "default_database")
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", 8000))
    
    # Redis Config
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", None)
    
    # Neo4j Config
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", os.getenv("NEO4J_USERNAME", "neo4j"))
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "")
    
    # PostgreSQL Config
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "")

    # Storage Config (Serverless fallback to /tmp/storage if root filesystem is read-only)
    STORAGE_DIR: str = os.getenv(
        "STORAGE_DIR",
        "/tmp/storage" if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")) else "storage"
    )
    
    @property
    def is_groq_available(self) -> bool:
        return bool(self.GROQ_API_KEY.strip())

    @property
    def is_langsmith_configured(self) -> bool:
        return bool(self.LANGCHAIN_API_KEY.strip()) and self.LANGCHAIN_TRACING_V2.lower() in ("true", "1", "t")

settings = Settings()
