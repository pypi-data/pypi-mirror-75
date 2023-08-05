import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.dateutils import date2str
from utils.code import get_md5_hash
from classcard_dataclient.models.semester import SemesterV2
from classcard_dataclient.models.schedule import RestScheduleV2, RestTableV2, PeriodSet
from config import SCHOOL_SEASON

logger = logging.getLogger(__name__)


class ScheduleSync(BaseSync):
    def __init__(self):
        super(ScheduleSync, self).__init__()
        self.offset = 300
        self.slot_map = {}
        self.semester = None
        self.rest_table = None

    def wrap_time(self, ts):
        return "{}:00".format(ts) if len(ts) < 6 else ts

    def extract_rest_table(self, rest_table):
        time_com_map = {"summer": ("summerstart", "summerend", "summerstartbefore"),
                        "winter": ("winterstart", "winterend", "winterstartbefore")}
        time_com = time_com_map[SCHOOL_SEASON]
        sql = "SELECT id, sectionname, {}, {}, {}, ver FROM mid_section " \
              "ORDER BY ver".format(time_com[0], time_com[1], time_com[2])
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            slot_id, name, start_time, stop_time, pre_time, num = row[0], row[1], row[2], row[3], row[4], row[5]
            self.slot_map[slot_id] = num
            if num <= 5:
                time_period = PeriodSet.MORNING
            elif num <= 9:
                time_period = PeriodSet.AFTERNOON
            else:
                time_period = PeriodSet.EVENING
            for week in range(1, 6):
                schedule_data = {"num": num, "order": num, "start_time": self.wrap_time(start_time),
                                 "stop_time": self.wrap_time(stop_time), "pre_time": self.wrap_time(pre_time)}
                rest_schedule = RestScheduleV2(week=week, time_period=time_period, **schedule_data)
                rest_table.add_schedule(rest_schedule)

    def sync(self):
        begin_datetime = datetime.datetime.now()
        end_datetime = begin_datetime + datetime.timedelta(days=60)
        begin_date, end_date = date2str(begin_datetime.date()), date2str(end_datetime.date())
        semester = SemesterV2(name="当前学期", begin_date=begin_date, end_date=end_date,
                              number=get_md5_hash("当前学期")[:20])
        rest_table = RestTableV2(name="全校作息", number=get_md5_hash("全校作息")[:20], semester_name=semester.name)
        self.extract_rest_table(rest_table)
        print(">>> CREATE_REST_TABLE")
        logger.info(">>> CREATE_REST_TABLE")
        self.client.create_semester(self.school_id, semester)
        self.client.create_rest_table(self.school_id, rest_table, is_active=True)
        self.close_db()
        self.semester = semester
        self.rest_table = rest_table
