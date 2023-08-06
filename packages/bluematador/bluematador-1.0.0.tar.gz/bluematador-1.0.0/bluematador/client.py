import os
from statsd import client as statsd

class OverriddenClient(statsd.StatsClient):
    def _prepare(self, stat, value, rate, tags=None):
        if rate and rate != 1:
            value = '{}|@{}'.format(value, rate)
        if self._prefix:
            stat = '{}.{}'.format(self._prefix, stat)
        if tags:
            tag_string = '#'.join(self._build_tag(k, v) for k, v in tags.items())
            return '{}:{}|#{}'.format(stat, value, tag_string)
        return '{}:{}'.format(stat, value)

    def _build_tag(self, tag, value):
        if value:
            return '{}:{}'.format(tag, value)
        else:
            return tag

class BlueMatadorClient():
    def __init__(self, prefix=None, host=os.environ.get('BLUEMATADOR_AGENT_HOST', 'localhost'), port=os.environ.get('BLUEMATADOR_AGENT_PORT', 8767)):
        self.client = OverriddenClient(host, port, prefix)

    def count(self, name, value=1, sample_rate=1, labels={}):
        '''
        Send a counter metric to the Blue Matador Agent.

            Parameters:
                name (string): (required) The metric name e.g. 'myapp.request.size'. Cannot contain ':' or '|'
                value (number): (optional) the amount to increment the metric by, the default is 1.
                sample_rate (number): (optional) sends only a sample of data e.g. 0.5 indicates 50% of data being sent. Default value is 1
                labels (dict): (optional)  adds metadata to a metric. Specified as a dict of key value pairs. Cannot contain '#' or '|'
        '''
        self.client.incr(self.sanitize(name, ':'), value, sample_rate, tags=self.sanitize_labels(labels))

    def gauge(self, name, value, sample_rate=1, labels={}):
        '''
        Send a gauge metric to the Blue Matador agent.

            Parameters:

                name (string): (required) The metric name e.g. 'myapp.request.size'. Cannot contain ':' or '|'
                value (number): (required) The latest value to set for the metric
                sample_rate (number): (optional) sends only a sample of data e.g. 0.5 indicates 50% of data being sent. Default value is 1
                labels (dict): (optional)  adds metadata to a metric. Specified as a dict of key value pairs. Cannot contain '#' or '|'
        '''
        self.client.gauge(self.sanitize(name, ':'), value, sample_rate, tags=self.sanitize_labels(labels))

    def sanitize(self, source_string, replace_string):
        sanitized_string = str(source_string)
        if replace_string in sanitized_string:
            sanitized_string = sanitized_string.replace(replace_string, '_')
        if '|' in sanitized_string:
            sanitized_string = sanitized_string.replace('|', '_')
        return sanitized_string

    def sanitize_labels(self, labels):
        return {self.sanitize(k, '#'): self.sanitize(v, '#') if v else None for k, v in labels.items()}

    def close(self):
        # the statsd package doesn't currently support a close method for the udp client
        pass
