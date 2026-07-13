import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# IMPORTAÇÃO DOS 10 BLOCOS OFICIAIS DA LPIC-1 / ESSENTIALS (50 QUESTÕES CADA)
from topico101 import POOL_101
from topico102 import POOL_102
from topico103 import POOL_103
from topico104 import POOL_104
from topico105 import POOL_105
from topico106 import POOL_106
from topico107 import POOL_107
from topico108 import POOL_108
from topico109 import POOL_109
from topico110 import POOL_110

# Consolidação definitiva do super banco de dados de 500 questões!
QUESTOES_POOL = POOL_101 + POOL_102 + POOL_103 + POOL_104 + POOL_105 + POOL_106 + POOL_107 + POOL_108 + POOL_109 + POOL_110
