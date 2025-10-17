class DatabaseManager:
    def __init__(self):
        self.session = get_db_session()

    def store_course(self, course):
        obj = Course(**course)
        self.session.merge(obj)
        self.session.commit()

    def store_assignments(self, assignments):
        for a in assignments:
            self.session.merge(Assignment(**a))
        self.session.commit()

    def store_announcements(self, announcements):
        for ann in announcements:
            self.session.merge(Announcement(**ann))
        self.session.commit()

    def store_grades(self, grades):
        for g in grades:
            self.session.merge(Grade(**g))
        self.session.commit()

    def update_sync_status(self, timestamp):
        print(f"Last sync completed at {timestamp}")
