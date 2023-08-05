import time
import sys
import math
from contextlib import contextmanager
from collections import defaultdict

from hdrh.histogram import HdrHistogram
from hdrh.iterators import LinearIterator


class PerfStats(object):
    def __init__(self, raw_stats=None):
        self.d = dict()
        if raw_stats:
            self.combine_stats(raw_stats)


    def combine_stats(self, raw_stats):
        for name, elapsed in raw_stats.items():
            g = self.d.get(name, defaultdict(float))
            if 'hist' not in g:
                maxhist = max(elapsed[0] * 2, 30) * 1000  # milliseconds
                g['hist'] = HdrHistogram(10, int(maxhist), 2)  # 10 milliseconds-..., 2 sig figs
            for e in elapsed:
                g['count'] += 1.0
                g['time'] += e
                g['hist'].record_value(int(e * 1000))
            self.d[name] = g

    def read_stats(self, name):
        if name in self.d:
            entry = self.d[name]
            return entry['count'], entry['time']/entry['count'], entry['hist']

    def all_stat_names(self):
        return self.d.keys()

    def print_percentiles(self, name='default', file=sys.stdout):
        self.print_percentile(name, file=file)
        for n in sorted(self.all_stat_names()):
            if n != name:
                self.print_percentile(n, file=file)

    def print_percentile(self, name, file=sys.stdout):
        if name in self.d:
            hist = self.d[name]['hist']
            print('counter {}, counts {}'.format(name, hist.get_total_count()), file=file)
            for pct in (50, 90, 95, 99):
                print('counter {}, {}%tile: {:.1f}s'.format(name, pct, hist.get_value_at_percentile(pct)/1000.), file=file)

    def print_histograms(self, name='default', file=sys.stdout):
        self.print_histogram(name, file=file)
        for n in sorted(self.all_stat_names()):
            if n != name:
                self.print_histogram(n, file=file)

    def print_histogram(self, name, value_units_per_bucket=3, file=sys.stdout):
        if name in self.d:
            hist = self.d[name]['hist']
            ivalues = [x for x in LinearIterator(hist, value_units_per_bucket)]
            valuemax = max([x.count_at_value_iterated_to for x in ivalues])
            if not valuemax:
                valuemax = 1.
            for ivalue in ivalues:
                print('counter {}, {} {}'.format(name,
                                                 ivalue.value_iterated_to/1000.,
                                                 ivalue.count_at_value_iterated_to))
#            for ivalue in ivalues:
#                print('counter {}, {} {}'.format(name,
#                                                 ivalue.value_iterated_to/1000.,
#                                                 ''.join(['*'] * math.ceil(ivalue.count_at_value_iterated_to/valuemax))))


@contextmanager
def record_wallclock(name, raw_stats):
    try:
        start = time.time()
        yield
    finally:
        if name not in raw_stats:
            raw_stats[name] = []
        raw_stats[name].append(time.time() - start)


@contextmanager
def record_iowait(name, raw_stats):
    try:
        start_t = time.time()
        start_c = time.process_time()
        yield
    finally:
        if name not in raw_stats:
            raw_stats[name] = []
        duration = time.time() - start_t
        cpu = time.process_time() - start_c
        raw_stats[name].append(duration - cpu)
