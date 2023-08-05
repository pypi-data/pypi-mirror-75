import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from utils.dateutils import datetime2str, datetime2str_z
from classcard_dataclient.models.classroom import Classroom, RoomType
from classcard_dataclient.models.meeting_room import MeetingRoom, MeetingRoomRule

logger = logging.getLogger(__name__)


class MeetingRoomSync(BaseSync):
    def __init__(self):
        super(MeetingRoomSync, self).__init__()
        now = datetime.datetime.now()
        self.datetime_line = "1970-01-01 12:12:12" or datetime2str(now)
        self.offset = 300
        self.place_appeared_number = []
        self.place_list = []
        self.meeting_map = {}
        self.host_map = {}
        self.meeting_user_map = {}
        self.meeting_room_list = []

    def extract_meeting_user(self):
        sql = "SELECT OutID, MeetNo FROM M_Meeting_Man_Out ORDER BY MeetNo"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            user_num, meet_no = row[0], row[1]
            if meet_no not in self.meeting_user_map:
                self.meeting_user_map[meet_no] = set()
            self.meeting_user_map[meet_no].add(user_num)

    def extract_host_map(self):
        sql = "SELECT OUTID, NAME FROM BASE_CUSTOMERS ORDER BY OUTID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            number, name = row[0], row[1]
            self.host_map[number] = name

    def extract_meeting_room(self):
        sql = "SELECT MeetNo,MeetName,MeetContent,Moderator,PlaceName,StAfter,StBefore,EndAfter,PlanStart,PlanEnd " \
              "FROM M_Meeting_Info_Out WHERE PlanStart > '{}' ORDER BY PlaceID".format(self.datetime_line)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            meet_no, name, remarks, host = row[0], row[1], row[2], row[3]
            place_name, later_time = row[4], row[5]
            active_start, active_end = row[6], row[7]
            start_time, end_time = row[8], row[9]
            left_seconds = (start_time - active_start).seconds
            right_seconds = (active_end - end_time).seconds
            mid_seconds = (later_time - start_time).seconds
            left = -(left_seconds % 60 + left_seconds // 60)
            right = right_seconds % 60 + right_seconds // 60
            mid = mid_seconds % 60 + mid_seconds // 60
            place_num = self.add_meeting_place(place_name)
            host = self.host_map.get(host, "主持人")
            meeting_room = MeetingRoom(name=name, host=host, remarks=remarks, start_time=datetime2str_z(start_time),
                                       end_time=datetime2str_z(end_time), active_start=datetime2str_z(active_start),
                                       active_end=datetime2str_z(active_end), classroom_number=place_num,
                                       extra_info={"meet_no": meet_no}, school=self.school_id)
            meeting_rule = MeetingRoomRule(left=left, right=right, mid=mid, school=self.school_id)
            meeting_room.rule = meeting_rule
            meeting_user = self.meeting_user_map.get(str(meet_no), [])
            meeting_room.user_numbers = list(meeting_user)
            self.meeting_room_list.append(meeting_room)

    def add_meeting_place(self, name):
        number = get_md5_hash(name)
        if number not in self.place_appeared_number:
            self.place_appeared_number.append(number)
            classroom = Classroom(number=number, name=name, school=self.school_id, category=RoomType.TYPE_PUBLIC)
            self.place_list.append(classroom)
        return number

    def extract_meeting_place(self):
        sql = "SELECT PlaceID,PlaceName FROM M_Meeting_Place_Out ORDER BY PlaceID"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            number, name = str(row[0]), row[1]
            number = get_md5_hash(name)
            if number not in self.place_appeared_number:
                self.place_appeared_number.append(number)
                classroom = Classroom(number=number, name=name, school=self.school_id, category=RoomType.TYPE_PUBLIC)
                self.place_list.append(classroom)

    def sync(self):
        self.extract_host_map()
        self.extract_meeting_user()
        self.extract_meeting_room()
        if not self.place_list:
            logger.info("没有会议室信息")
            return
        self.client.create_classrooms(self.school_id, self.place_list)
        self.client.create_meeting_rooms(self.school_id, self.meeting_room_list)
        self.close_db()
