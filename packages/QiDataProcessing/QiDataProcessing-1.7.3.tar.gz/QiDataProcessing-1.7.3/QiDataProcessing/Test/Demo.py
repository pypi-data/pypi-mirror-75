import time

import pandas as pd

from QiDataProcessing.BaseBarHelper import BaseBarHelper
from QiDataProcessing.Core.EnumMarket import EnumMarket
from QiDataProcessing.Core.TradingDayHelper import TradingDayHelper
from QiDataProcessing.Instrument.InstrumentManager import InstrumentManager
from QiDataProcessing.QiDataController import QiDataController
import datetime
from QiDataProcessing.Core.EnumBarType import EnumBarType
from QiDataProcessing.QiDataDirectory import QiDataDirectory
from QiDataProcessing.TradingFrame.YfTimeHelper import YfTimeHelper

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

trading_day = datetime.datetime(2019, 10, 13)
tick_path = "\\\\192.168.1.200\\MqData\\futuretick\\Future"
min_path = "\\\\192.168.1.200\\MqData\\futuremin"
day_path = "\\\\192.168.1.200\\MqData\\futureday"

qi_data_directory = QiDataDirectory()
qi_data_directory.trading_day = trading_day
qi_data_directory.future_tick = tick_path
qi_data_directory.future_tick_cache = tick_path
qi_data_directory.future_min = min_path
qi_data_directory.future_day = day_path

qi_data_controller = QiDataController(qi_data_directory)

instrument_id = 'IC9999'
# 获取交易所代码
exchange_id = qi_data_controller.instrument_manager.get_exchange_id(instrument_id)
# 获取期货品种列表
lst_product_ids = qi_data_controller.instrument_manager.get_product_ids(EnumMarket.期货, exchange_id)
# 获取期货主力合约列表
lst_main_contract = qi_data_controller.instrument_manager.get_main_contracts(EnumMarket.期货, exchange_id)
# 获取期货上市日期
listing_date = qi_data_controller.instrument_manager.get_listing_date(EnumMarket.期货, instrument_id)
# 获取期货活跃日期
active_date = qi_data_controller.instrument_manager.get_active_date(EnumMarket.期货, instrument_id)

begin_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2020,7,1)

# 进行活跃日期的判断
if begin_date < active_date:
    begin_date = active_date

interval = 5
bar_type = EnumBarType.minute
bar_series = qi_data_controller.load_bar_series_by_date(EnumMarket.期货, instrument_id, interval, bar_type, begin_date, end_date)
index = 1
for bar in bar_series:
    print("["+instrument_id+"]"+str(index)+":"+bar.to_string()+','+str(bar.pre_close)+bar.end_time.strftime('%Y%m%d %H%M%S%f'))
    index += 1
