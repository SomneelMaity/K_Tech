import os
from dotenv import load_dotenv

load_dotenv()

class setting:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY","")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ugc.db")
    
    @property
    def has_anthropic(self)->bool:
        return bool(self.ANTHROPIC_API_KEY)