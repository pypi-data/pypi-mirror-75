from .cas_connection import CassandraConnector
from ...view.cas.fund_estimated_nav import FundEstimatedNav
from cassandra.cqlengine.management import sync_table, drop_table


def sync_cas_table():
    sync_table(FundEstimatedNav)

def drop_cas_table():
    drop_table(FundEstimatedNav)


if __name__ == '__main__':
    CassandraConnector().get_conn()
    sync_cas_table()
    # drop_cas_table()
