import datetime
from sync.base import BaseSync
from utils.loggerutils import logging
from classcard_dataclient.models.classroom import Classroom, RoomType

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self):
        super(ClassroomSync, self).__init__()
        now = datetime.datetime.now()
        self.offset = 300
        self.appeared_number = []
        self.classroom_list = []
        self.classroom_map = {}
        self.name_num = {}
        self.building_map = {}
        self.building_list = set()

    def extract_building(self):
        sql = "SELECT id, areaname, fullname, pid, levf FROM mid_areainfo ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, fullname, parent_id, level = row[0], row[1], row[2], row[3], row[4]
            self.building_map[external_id] = fullname
            self.building_list.add(parent_id)

    def extract_classroom(self):
        sql = "SELECT id, fullname, pid, levf FROM mid_areainfo ORDER BY levf"
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            external_id, name, parent_id, level = row[0], row[1], row[2], row[3]
            if external_id in self.building_list:
                continue
            building = self.building_map.get(parent_id, None)
            number = str(external_id)
            try:
                name_info = name.split("-")
                floor = name_info[-1][0] if len(name_info[-1]) <= 3 else name_info[-1][:2]
            except (Exception,):
                floor = None
            if name not in self.name_num:
                self.name_num[name] = number
                classroom = Classroom(number=number, name=name, building=building,
                                      floor=floor, school=self.school_id, category=RoomType.TYPE_PUBLIC)
                self.classroom_list.append(classroom)
            self.classroom_map[number] = self.name_num[name]

    def sync(self):
        self.extract_building()
        self.extract_classroom()
        if not self.classroom_map:
            logger.info("没有教室信息")
            return
        self.client.create_classrooms(self.school_id, self.classroom_list)
        self.close_db()
