from datetime import datetime
from cryptomodel.coinmarket import prices
from cryptomodel.fixer import exchange_rates
from cryptomodel.readonly import SymbolRates
from mongoengine import Q
from cryptodataaccess.helpers import server_time_out_wrapper, do_connect

DATE_FORMAT = "%Y-%m-%d"


class CalculatorRepository:

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def evaluate_variable(self):
        pass

    def evaluate_expression(self):
        pass


class StatementExecutor:

    def prepare(self):
        pass

    def execute(self):
        pass


class MongoEngineStatementExecutor(StatementExecutor):
    pass
