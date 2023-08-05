import mock
from bson import ObjectId
from cryptomodel.cryptostore import user_channel, user_transaction, user_notification
from cryptodataaccess.config import configure_app
from cryptodataaccess.TransactionRepository import TransactionRepository
import pytest
from cryptodataaccess.helpers import do_connect


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("cryptodataaccess.helpers.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock


def test_insert_transaction():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT")
    assert (len(user_transaction.objects) == 1)
    assert (ut.operation == 'Added')


def test_update_transaction():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.update_transaction(ut.id, 1, 1, 'OXT2', 1, 1, "EUR", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT2")
    assert (ut.currency == "EUR")
    assert (ut.operation == 'Added')


def test_update_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    with pytest.raises(ValueError):
        repo.update_transaction(ObjectId('666f6f2d6261722d71757578'), 1, 1, 'OXT', "EUR", 1, 1, "2020-01-01",
                                "kraken", source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')


def test_delete_transaction_when_does_not_exist_throws_ValueError():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    with pytest.raises(ValueError):
        repo.delete_transaction(ObjectId('666f6f2d6261722d71757578'))


def test_delete_transaction_when_does_not_exist_and_throw_is_false_does_not_throw():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    repo.delete_transaction(ObjectId('666f6f2d6261722d71757578'), throw_if_does_not_exist=False)


def test_delete_transaction_when_exists():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    assert (len(user_transaction.objects) == 1)
    ut = repo.delete_transaction(ut.id)
    assert (len(user_transaction.objects) == 0)


def test_delete_transaction_when_exists_by_source_id():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "EUR", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    assert (len(user_transaction.objects) == 1)
    ut = repo.do_delete_transaction_by_source_id(source_id=ut.source_id)
    assert (len(user_transaction.objects) == 0)


def test_fetch_transaction():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.fetch_transaction(ut.id)
    assert (ut.user_id == 1)
    assert (ut.symbol == "OXT")
    assert (ut.currency == "USD")
    assert (ut.operation == 'Added')
    assert (ut.source_id == ObjectId('666f6f2d6261722d71757578'))
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=None, operation='Added')
    ut = repo.fetch_transaction(ut.id)
    assert (ut.source_id is None)


def test_fetch_transaction():
    config = configure_app()
    repo = TransactionRepository(config, mock_log)
    do_connect(config)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    items =  ut = repo.do_fetch_distinct_user_ids()
    assert (len(items)==1)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.insert_transaction(12, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    items =  ut = repo.do_fetch_distinct_user_ids()
    assert (len(items)==2)
    user_transaction.objects.all().delete()
    ut = repo.insert_transaction(1, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.insert_transaction(12, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.insert_transaction(3, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    ut = repo.insert_transaction(122, 1, 'OXT', 1, 1, "USD", "2020-01-01", "kraken",
                                 source_id=ObjectId('666f6f2d6261722d71757578'), operation='Added')
    items =  ut = repo.do_fetch_distinct_user_ids()
    assert (len(items)==4)