import pandas as pd
from sql_query import *
from program_flow import *

TAX_RATE = '10'
sime_day = '20250320'
program_flow = ProgramFlow(sime_day, TAX_RATE)
program_flow.start()
