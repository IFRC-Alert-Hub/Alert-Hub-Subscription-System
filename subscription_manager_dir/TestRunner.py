from django.test.runner import DiscoverRunner

class AlertDBTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Use your existing database as the test database
        from django.db import connections
        from django.db.backends.dummy.base import DatabaseWrapper

        test_db_alias = 'AlertDB'
        connections.databases[test_db_alias] = connections.databases['AlertDB']
        connections[test_db_alias] = DatabaseWrapper(connections[test_db_alias])

        # Continue with the rest of the setup
        return super().setup_databases(**kwargs)