from collections import OrderedDict


class ResolverCache(object):
    """
    An object representing resolver cache.

    It takes a single argument, i.e config, which is a dictionary of data
    resolver settings. Here it is an example config:

    .. code-block:: python

        config = {
            'name': 'edm',
            'benchmark': 'BAB0',
            'reflector': 'RB2',
            'start_at': '2019-04-01',
            'end_at': '2019-08-01',
            'ci': True,
        }

    Key ``csv``, ``url``, and ``name`` are reserved as data resolver sources.
    Other keys left as optional parameters.

    Example:

    .. code-block:: python

        from komapy.series import Series

        series = Series(name='edm', fields=['timestamp', 'slope_distance'],
                        xaxis_date=True)
        cache = {}

        def cached_resolver(series):
            config = ResolverCache.get_resolver_cache_config(series)
            resolver = ResolverCache(config)
            key = hash(resolver)

            if key in cache:
                return cache[key]
            data = series.resolve_data()
            cache[key] = data
            return data
    """

    def __init__(self, config):
        self.config = config

    def __eq__(self, other):
        if isinstance(other, ResolverCache):
            return self.config == other.config
        return False

    def __hash__(self):
        casted_config = dict([(str(key), str(value))
                              for key, value in self.config.items()])
        return hash(frozenset(casted_config.items()))

    @staticmethod
    def get_resolver_cache_config(series):
        """
        Get resolver cache config from KomaPy series instance. It's simply
        takes data resolver key and optional query or csv parameters.

        :param series: KomaPy series config instance.
        :type series: :class:`komapy.series.Series`
        :return: Dictionary of :class:`komapy.cache.ResolverCache` config.
        :rtype: dict
        """
        config = {}

        sources = OrderedDict([
            ('csv', 'csv_params'),
            ('json', 'json_params'),
            ('excel', 'excel_params'),
            ('sql', 'sql_params'),
            ('url', 'query_params'),
            ('name', 'query_params'),
        ])

        for name in sources:
            source = getattr(series, name, None)
            if source:
                config[name] = source
                options = getattr(series, sources[name], {})
                if options:
                    config.update(options)
                break

        return config

    @classmethod
    def create_instance_from_series(cls, series):
        """
        Create resolver cache instance from KomaPy series.

        :param series: KomaPy series config instance.
        :type series: :class:`komapy.series.Series`
        :return: KomaPy resolver cache instance.
        :rtype: :class:`komapy.cache.ResolverCache`
        """
        config = cls.get_resolver_cache_config(series)
        return cls(config)

    @classmethod
    def create_key_from_series(cls, series):
        """
        Create resolver cache key from KomaPy series.

        :param series: KomaPy series config instance.
        :type series: :class:`komapy.series.Series`
        :return: KomaPy resolver cache key.
        :rtype: int
        """
        return hash(cls.create_instance_from_series(series))
