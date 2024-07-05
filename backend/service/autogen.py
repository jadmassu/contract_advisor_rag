import os, sys
from dotenv import load_dotenv
rpath = os.path.abspath('/home/user/Documents/10/w11/contract_advisor_rag')

if rpath not in sys.path:
    sys.path.insert(0, rpath)
load_dotenv()