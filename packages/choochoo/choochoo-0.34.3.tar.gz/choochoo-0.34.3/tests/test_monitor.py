
from logging import getLogger
from subprocess import run
from tempfile import TemporaryDirectory

import sqlalchemy.sql.functions as func

from ch2.commands.read import read
from ch2.commands.args import bootstrap_dir, m, V, DEV, mm, BASE, MONITOR
from ch2.config.profile.default import default
from ch2.lib.date import to_time, local_date_to_time
from ch2.sql.tables.monitor import MonitorJournal
from ch2.sql.tables.pipeline import PipelineType
from ch2.sql.tables.statistic import StatisticJournal, StatisticName
from ch2.pipeline.calculate.monitor import MonitorCalculator
from ch2.pipeline.pipeline import run_pipeline
from ch2.data import Names as N
from tests import LogTestCase

log = getLogger(__name__)


class TestMonitor(LogTestCase):

    def test_monitor(self):
        with TemporaryDirectory() as f:
            args, data = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            args, data = bootstrap_dir(f, m(V), '5', mm(DEV),
                                       'read', 'data/test/source/personal/25822184777.fit')
            read(args, data)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            run_pipeline(data, PipelineType.CALCULATE, force=True, start='2018-01-01', n_cpu=1)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with data.db.session_context() as s:
                n = s.query(func.count(StatisticJournal.id)).scalar()
                self.assertEqual(n, 137)
                mjournal = s.query(MonitorJournal).one()
                self.assertNotEqual(mjournal.start, mjournal.finish)

    def test_values(self):
        with TemporaryDirectory() as f:
            bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            for file in ('24696157869', '24696160481', '24696163486'):
                args, data = bootstrap_dir(f, m(V), '5', mm(DEV),
                                           'read', mm(MONITOR),
                                           'data/test/source/personal/andrew@acooke.org_%s.fit' % file)
                read(args, data)
            # path = args.system_path(subdir='data', file='activity.db')
            # run(f'sqlite3 {path} ".dump"', shell=True)
            run_pipeline(data, PipelineType.CALCULATE, force=True, like=('%Monitor%',), start='2018-01-01', n_cpu=1)
            with data.db.session_context() as s:
                mjournals = s.query(MonitorJournal).order_by(MonitorJournal.start).all()
                assert mjournals[2].start == to_time('2018-09-06 15:06:00'), mjournals[2].start
                # steps
                summary = s.query(StatisticJournal).join(StatisticName). \
                    filter(StatisticJournal.time >= local_date_to_time('2018-09-06'),
                           StatisticJournal.time < local_date_to_time('2018-09-07'),
                           StatisticName.owner == MonitorCalculator,
                           StatisticName.name == N.DAILY_STEPS).one()
                if summary.value != 12757:
                    path = args.system_path(subdir='data', file='activity.db')
                    run('sqlite3 %s "select * from statistic_journal as j, statistic_journal_integer as i, '
                        'statistic_name as n where j.id = i.id and j.statistic_name_id = n.id and '
                        'n.name = \'steps\' order by j.time"' % path, shell=True)
                    run('sqlite3 %s "select * from statistic_journal as j, statistic_journal_integer as i, '
                        'statistic_name as n where j.id = i.id and j.statistic_name_id = n.id and '
                        'n.name = \'cumulative-steps\' order by j.time"' % path, shell=True)
                # connect has 12757 for this date,
                self.assertEqual(summary.value, 12757)

    FILES = ('25505915679', '25519562859', '25519565531', '25532154264', '25539076032', '25542112328')

    def generic_bug(self, files, join=False):
        with TemporaryDirectory() as f:
            args, data = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            if join:
                files = ['data/test/source/personal/andrew@acooke.org_%s.fit' % file for file in files]
                args, data = bootstrap_dir(f, mm(DEV), 'read', *files)
                read(args, data)
            else:
                for file in files:
                    args, data = bootstrap_dir(f, mm(DEV), 'read',
                                               'data/test/source/personal/andrew@acooke.org_%s.fit' % file)
                    read(args, data)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with data.db.session_context() as s:
                # steps
                summary = s.query(StatisticJournal).join(StatisticName). \
                    filter(StatisticJournal.time >= local_date_to_time('2018-10-07'),
                           StatisticJournal.time < local_date_to_time('2018-10-08'),
                           StatisticName.owner == MonitorCalculator,
                           StatisticName.name == N.DAILY_STEPS).one()
                # connect has 3031 for this date.
                self.assertEqual(summary.value, 3031)

    def test_bug(self):
        self.generic_bug(sorted(self.FILES))

    def test_bug_reversed(self):
        self.generic_bug(sorted(self.FILES, reverse=True))

    def test_bug_join(self):
        self.generic_bug(sorted(self.FILES), join=True)

    def test_bug_reversed_join(self):
        self.generic_bug(sorted(self.FILES, reverse=True), join=True)

    # issue 6
    def test_empty_data(self):
        with TemporaryDirectory() as f:
            args, data = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            args, data = bootstrap_dir(f, m(V), '5', mm(DEV),
                                      'read', 'data/test/source/other/37140810636.fit')
            read(args, data)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            run_pipeline(data, PipelineType.CALCULATE, n_cpu=1)
            # run('sqlite3 %s ".dump"' % f.name, shell=True)
            with data.db.session_context() as s:
                n = s.query(func.count(StatisticJournal.id)).scalar()
                self.assertEqual(n, 44)
                mjournal = s.query(MonitorJournal).one()
                self.assertNotEqual(mjournal.start, mjournal.finish)
