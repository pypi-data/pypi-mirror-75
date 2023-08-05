# 全局配置
import string
import random
from logging import DEBUG

SETTINGS = {
    # 市场名称
    "MARKET_NAME": "",
    # 账户token长度
    "TOKEN_LENGTH": 20,
    # 数据精确度
    "POINT": 2,
    # 是否开启成交量计算模拟
    # TODO 暂时没有实现相关功能
    "VOLUME_SIMULATION": False,
    # 是否开启账户与持仓信息的验证
    "VERIFICATION": True,
    # 引擎撮合速度（秒）
    # 设置此参数时请参考行情的刷新速度
    "PERIOD": 3,
    # 数据持久化模式
    # 实时持久化，会大幅降低整个模拟交易程序的执行效率，建议在手工交易时使用
    # 定时持久化，系统会在指定的时间间隔进行自动持久化，时间间隔越低，效率越低，建议进行低频程序化交易时使用
    # 手动持久化，系统会在接收到命令时进行持久化操作，建议在回测时使用
    "PERSISTENCE_MODE": "",
    # 数据持久化时间间隔
    # TODO 暂时没有实现相关功能
    "P_TIMING": 0,
    # mongoDB 参数
    "MONGO_HOST": "",
    "MONGO_PORT": 0,
    # 本地行情数据， 用于web交易回看
    "HQ_MONGO_HOST": "",
    "HQ_MONGO_PORT": 0,
    "ACCOUNT_DB": "pt_account",
    "POSITION_DB": "pt_position",
    "TRADE_DB": "pt_trade",
    "ACCOUNT_RECORD": "pt_acc_record",
    "POS_RECORD": "pt_pos_record",
    # tushare行情源参数(填写你自己的tushare token，可以前往https://tushare.pro/ 注册申请)
    "TUSHARE_TOKEN": "",
    # pytdx行情参数（可以去各家券商下载通达信交易软件找到相关的地址）
    "TDX_HOST": "210.51.39.201",
    "TDX_PORT": 7709,
    # 账户初始参数
    "CAPITAL": 1000000.00,  # 初始资金
    "COST": 0.0003,  # 交易佣金
    "TAX": 0.001,  # 印花税
    "SLIPPOINT": 0.01,  # 滑点（暂未实现）
    # log服务参数
    "log.active": True,
    "log.level": DEBUG,
    "log.console": True,
    # email服务参数(根据实际情况进行使用）
    "email.server": "",
    "email.port": 0,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",
}


def get_token():
    """生成账户token值"""
    w = string.ascii_letters + string.digits
    count = SETTINGS["TOKEN_LENGTH"]
    token = []

    for i in range(count):
        token.append(random.choice(w))

    return "".join(token)
