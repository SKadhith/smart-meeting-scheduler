# Application
--------Interview schedule system---------------
from datetime import datetime, timedelta

class Meeting:
    def __init__(self): 
        self.working_hours = (9, 17)  
        self.holidays = {"2025-01-01", "2025-12-25"}  
        self.schedules = {} 

    def is_work_day(self, date):
        weekday = date.weekday()
        return weekday < 5 and date.strftime("%Y-%m-%d") not in self.holidays
    
    def check_available_slots(self, user, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_work_day(date):
            return "No available slots"
        
        booked = self.schedules.get(user, {}).get(date_str, [])
        available_slots = []
        start = datetime.strptime(f"{self.working_hours[0]}:00", "%H:%M").time()
        
        for end in [slot[0] for slot in booked] + [datetime.strptime(f"{self.working_hours[1]}:00", "%H:%M").time()]:
            if start < end:
                available_slots.append((start, end))
            start = booked.pop(0)[1] if booked else end        
        if not available_slots:
            return "No available slots"
        formatted_slots = [f"{s.strftime('%I:%M %p')} – {e.strftime('%I:%M %p')}" for s, e in available_slots]
        return "Available slots:\n" + "\n".join(formatted_slots)
    

    def schedule_meeting(self, user, date_str, start_time, end_time):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_work_day(date):
            return "Cannot schedule on weekends or holidays."
        
        start_dt = datetime.strptime(start_time, "%H:%M").time()
        end_dt = datetime.strptime(end_time, "%H:%M").time()
        
        if not (self.working_hours[0] <= start_dt.hour < self.working_hours[1] and 
                self.working_hours[0] < end_dt.hour <= self.working_hours[1] and 
                start_dt < end_dt):
            return "Its must within working hours."
        
        self.schedules.setdefault(user, {}).setdefault(date_str, [])
        for existing_start, existing_end in self.schedules[user][date_str]:
            if not (end_dt <= existing_start or start_dt >= existing_end):
                return "Time slot overlaps existing meeting."
        
        self.schedules[user][date_str].append((start_dt, end_dt))
        self.schedules[user][date_str].sort()
        return "Meeting is scheduled successfully."

    def view_meet(self, user, date_str):
        meetings = self.schedules.get(user, {}).get(date_str, [])
        if not meetings:
            return "No meetings scheduled"        
        formatted_meetings = [f"{s.strftime('%I:%M %p')} – {e.strftime('%I:%M %p')}" for s, e in meetings]
        return "Scheduled meetings:\n" + "\n".join(formatted_meetings)
scheduler = Meeting()
print(scheduler.schedule_meeting("Adhi", "2025-03-18", "10:00", "11:00"))
print(scheduler.check_available_slots("Adhi", "2025-03-18"))
print(scheduler.view_meet("Adhi", "2025-03-18"))

