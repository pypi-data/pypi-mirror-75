import mock
from cryptomodel.coinmarket import  prices
from mongoengine import  Q
from cryptodataaccess.config import configure_app
import pytest
from cryptodataaccess.helpers import do_connect
from tests.helpers import insert_prices_record


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_eval_collection():
    config = configure_app()
    do_connect(config)
    actual_count = prices.objects()
    j = "prices"
    assert(len(eval(j).objects()) == len(actual_count))


def test_get_latest_prices_by_date_eval():
    config = configure_app()
    do_connect(config)
    actual_count = prices.objects()
    j = "prices"
    prices.objects.all().delete()
    insert_prices_record()
    exec("before_date = '2021-01-01'")
    assert (len( eval("prices.objects(Q(status__timestamp__lte=before_date)).order_by('-status__timestamp')[:1]")) == 1)

    eval("prices.objects(Q(status__timestamp__lte=before_date)).order_by('-status__timestamp')[:1]")
