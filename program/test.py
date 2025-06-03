import pandas as pd
from sql_query import *
from program_flow import *

TAX_RATE = '10'
SIME_DAY = '20250320'
program_flow:object = ProgramFlow(SIME_DAY, TAX_RATE)
program_flow.start()
