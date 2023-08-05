from json import loads, dumps
from logging import getLogger

from sqlalchemy import exists

from ...commands.args import SERVICE, WEB, mm, SQLITE, POSTGRESQL, URI
from ...commands.database import load, delete_current
from ...commands.help import HTML, filter, parse, P, LI, PRE
from ...commands.import_ import import_source
from ...config.utils import profiles
from ...lib import time_to_local_time, local_time_to_time
from ...lib.log import Record
from ...import_ import available_versions
from ...import_.activity import activity_imported
from ...import_.constant import constant_imported
from ...import_.diary import diary_imported
from ...import_.kit import kit_imported
from ...import_.segment import segment_imported
from ...sql import SystemConstant, Constant, StatisticJournal, ActivityJournal

log = getLogger(__name__)


ACTIVITY = 'activity'
CONFIGURED = 'configured'
CONSTANT = 'constant'
DESCRIPTION = 'description'
DIARY = 'diary'
DIRECTORY = 'directory'
IMPORTED = 'imported'
KIT = 'kit'
NAME = 'name'
PROFILE = 'profile'
PROFILES = 'profiles'
SEGMENT = 'segment'
SINGLE = 'single'
STATISTIC = 'statistic'
TIME = 'time'
VALUE = 'value'
VALUES = 'values'
VERSION = 'version'
VERSIONS = 'versions'


class Configure:

    def __init__(self, data, uri):
        self.__data = data
        self.__uri = uri
        self.__html = HTML(delta=1, parser=filter(parse, yes=(P, LI, PRE)))

    def is_configured(self):
        return bool(self.__data.sys.get_constant(SystemConstant.DB_VERSION, none=True))

    def is_empty(self, s):
        return not s.query(exists().where(ActivityJournal.id > 0)).scalar()

    def html(self, text):
        return self.__html.str(text)

    def read_profiles(self, request, s):
        fn_argspec_by_name = profiles()
        version = self.__data.sys.get_constant(SystemConstant.DB_VERSION, none=True)
        data = {PROFILES: {name: self.html(fn_argspec_by_name[name][0].__doc__) for name in fn_argspec_by_name},
                CONFIGURED: bool(version),
                DIRECTORY: self.__data.base}
        if data[CONFIGURED]: data[VERSION] = version
        return data

    def write_profile(self, request, s):
        data = request.json
        if not self.__uri:
            raise Exception(f'Bootstrap via web requires '
                            f'`{WEB} {SERVICE} ({mm(SQLITE)} | {mm(POSTGRESQL)} | {mm(URI)})`')
        load(self.__data.sys, self.__data.base, data[PROFILE], self.__uri)
        self.__data.reset()

    def delete(self, request, s):
        delete_current(self.__data.sys)
        self.__data.reset()

    def read_import(self, request, s):
        record = Record(log)
        return {IMPORTED: {DIARY: diary_imported(record, self.__data.db),
                           ACTIVITY: activity_imported(record, self.__data.db),
                           KIT: kit_imported(record, self.__data.db),
                           CONSTANT: constant_imported(record, self.__data.db),
                           SEGMENT: segment_imported(record, self.__data.db)},
                VERSIONS: available_versions(self.__data)}

    def write_import(self, request, s):
        data = request.json
        record = Record(log)
        import_source(self.__data, record, data[VERSION])
        return record.json()

    def read_constants(self, request, s):
        return [self.read_constant(s, constant)
                for constant in s.query(Constant).order_by(Constant.name).all()]

    def read_constant(self, s, constant):
        as_json = bool(constant.validate_cls)
        values = [{TIME: time_to_local_time(statistic.time),
                   VALUE: loads(statistic.value) if as_json else statistic.value,
                   STATISTIC: statistic.id}
                  for statistic in s.query(StatisticJournal).
                      filter(StatisticJournal.source_id == constant.id).all()]
        return {NAME: constant.name,
                SINGLE: constant.single,
                DESCRIPTION: self.html(constant.statistic_name.description),
                VALUES: values}

    def write_constant(self, request, s):
        data = request.json
        log.debug(data)
        constant = Constant.from_name(s, data[NAME])
        value = data[VALUES][0][VALUE]
        if constant.validate_cls:
            value = dumps(value)
        time = data[VALUES][0][TIME]
        statistic_journal_id = data[VALUES][0][STATISTIC]
        if statistic_journal_id:
            journal = s.query(StatisticJournal). \
                filter(StatisticJournal.id == statistic_journal_id,
                       StatisticJournal.source_id == constant.id).one()
            journal.set(value)
            if not constant.single:
                journal.time = local_time_to_time(time)
        else:
            if constant.single and time:
                log.warning(f'Ignoring time for {constant.name}')
                time = 0.0
            constant.add_value(s, value, time=time)

    def delete_constant(self, request, s):
        data = request.json
        log.debug(data)
        s.delete(Constant.from_name(s, data))
