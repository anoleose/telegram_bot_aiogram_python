
import os
from dotenv import load_dotenv
load_dotenv()

#захват учетных данных из виртуальной среды для большей безопасности
API_KEY_TEL       = os.environ.get('API_KEY_TEL')
API_KEY_WEATHER   = os.environ.get('API_KEY_WEATHER')
API_KEY_EXCHANGE  = os.environ.get('API_KEY_EXCHANGE')



