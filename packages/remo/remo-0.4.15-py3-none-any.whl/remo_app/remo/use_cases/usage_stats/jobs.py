import os
import signal
from threading import Thread, Event

from django.db.models import F
from django.utils import timezone

from remo_app.remo.models.downloads import LocalUsage, LocalStats
from remo_app.remo.services.stats import Stats
from remo_app.version import __version__


class Task:
    uuid = os.getenv('REMO_UUID', 'undefined')

    def on_start(self):
        raise NotImplementedError()

    def collect(self):
        raise NotImplementedError()

    def on_stop(self):
        raise NotImplementedError()


class StoppableTask(Thread, Task):
    _stop_event = Event()

    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        super().__init__()

    def stop(self, *args, **krwars):
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()

    def sleep(self, seconds: int):
        self._stop_event.wait(seconds)

    def run(self):
        self.on_start()
        try:
            intervals = [1, 3, 5, 10, 30, 60]  # minutes
            for minutes in intervals:
                if self.is_stopped():
                    break
                self.sleep(minutes * 60)
                if not self.is_stopped():
                    self.collect()

            two_hours = 2 * 60 * 60
            while not self.is_stopped():
                self.sleep(two_hours)
                if not self.is_stopped():
                    self.collect()
        except KeyboardInterrupt:
            pass
        self.on_stop()


class UsageInfo(Task):
    def _new(self) -> LocalUsage:
        stats = LocalUsage.objects.create()
        stats.srv_id = f'{self.uuid}_{stats.id}'
        stats.version = __version__
        stats.save()
        return stats

    def _last(self) -> LocalUsage:
        stats = LocalUsage.objects.last()
        if stats:
            return stats
        return self._new()

    def on_start(self):
        self._new()
        self.send_data()

    def send_data(self):
        for stats in LocalUsage.objects.exclude(n_checks=F('synced_check')):
            self.sync(stats)

    @staticmethod
    def sync(stats: LocalUsage):
        ok = Stats.send_usage_info(
            stats.srv_id,
            stats.version,
            stats.started_at,
            stats.n_checks,
            last_check_at=stats.last_check_at,
            stopped_at=stats.stopped_at,
        )
        if ok:
            stats.synced_check = stats.n_checks
            stats.save()

    def collect(self):
        stats = self._last()
        stats.check_usage()
        self.send_data()

    def on_stop(self):
        stats = self._last()
        stats.stopped_at = timezone.now()
        stats.save()
        self.sync(stats)


class StatsInfo(Task):
    def _new(self) -> LocalStats:
        stats = LocalStats.objects.create()
        stats.srv_id = f'{self.uuid}_{stats.id}'
        stats.save()
        return stats

    def on_start(self):
        stats = self._new()
        stats.collect_data()
        self.send_data()

    def send_data(self):
        for stats in LocalStats.objects.filter(synced=False):
            self.sync(stats)

    @staticmethod
    def sync(stats: LocalStats):
        ok = Stats.send_stats_info(
            stats.srv_id, stats.n_datasets, stats.dataset_stats, stats.annotation_set_stats,
        )
        if ok:
            stats.synced = True
            stats.save()

    def collect(self):
        stats = self._new()
        stats.collect_data()
        self.send_data()

    def on_stop(self):
        stats = self._new()
        stats.collect_data()
        self.sync(stats)


class CollectInfo(StoppableTask):
    tasks = [StatsInfo(), UsageInfo()]

    def on_start(self):
        for task in self.tasks:
            task.on_start()

    def collect(self):
        for task in self.tasks:
            task.collect()

    def on_stop(self):
        for task in self.tasks:
            task.on_stop()


def collect_usage_info():
    worker = CollectInfo()
    try:
        worker.start()
        worker.join()
    except KeyboardInterrupt:
        pass
