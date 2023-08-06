from datetime import datetime

import mock
from cryptomodel.coinmarket import  prices
from cryptomodel.cryptomodel import user_transaction, exchange_rates
from mongoengine import  Q

from cryptodataaccess.Rates.RatesMongoStore import RatesMongoStore
from cryptodataaccess.Rates.RatesRepository import RatesRepository
from cryptodataaccess.Rates.RatesStore import RatesStore
from cryptodataaccess.config import configure_app
import pytest
from cryptodataaccess.helpers import do_connect
from tests.helpers import insert_prices_record, insert_exchange_record


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_fetch_symbol_rates_for_date_pass_str_or_dt():
    config = configure_app()
    do_connect(config)
    user_transaction.objects.all().delete()
    exchange_rates.objects.all().delete()
    prices.objects.all().delete()

    insert_prices_record()
    insert_exchange_record()

    config = configure_app()
    store = RatesMongoStore(config,mock_log)
    rates_repo = RatesRepository(store)
    do_connect(config)

    rates_repo.fetch_symbol_rates_for_date(datetime.today())
    rates_repo.fetch_symbol_rates_for_date("2040-01-01")

    assert (len(prices.objects) == 1 )
