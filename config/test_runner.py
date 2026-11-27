from django.test.runner import DiscoverRunner


class PostgreSQLTestRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        kwargs["keepdb"] = True
        super().__init__(*args, **kwargs)