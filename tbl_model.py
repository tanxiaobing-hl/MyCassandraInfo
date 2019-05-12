# coding=utf-8

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
import config as settings
import pandas as pd

hosts = settings.DB_CONTACT_POINTS
authProvider = PlainTextAuthProvider(username=settings.DB_USER, password=settings.DB_PASSWORD)
# cluster = {'protocol_version': settings.CASSAN_PROTOCOL_VERSION, 'auth_provider': authProvider}
clusterParamDict = {'auth_provider': authProvider}
keyspace = settings.DB_KEYSPACE
connection.setup(hosts, keyspace, **clusterParamDict)
cluster = connection.get_cluster()
session = connection.get_session()
session.set_keyspace(settings.DB_KEYSPACE)
# session.default_fetch_size = 50000
session.default_timeout = 120


class tbl_hello_world(Model):
    task_id = columns.BigInt(partition_key=True, primary_key=True)
    start_time = columns.Text()
    end_time = columns.Text()
    is_risk = columns.Boolean()
    predictable_characterization = columns.Text()
    predictable_identification = columns.Boolean()
    fault_scenario = columns.Text()
    root_cause = columns.Text()
