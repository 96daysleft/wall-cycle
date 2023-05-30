import random

class TimeOptions:

    @property
    def all(self):
        return "all"
    
    @property
    def day(self):
        return "day"
    
    @property
    def hour(self):
        return "hour"
    
    @property
    def month(self):
        return "month"
     
    @property
    def week(self):
        return "week"
        
    @property
    def year(self):
        return "year"

    def properties(self):
        return [prop for prop in dir(self) if isinstance(getattr(self, prop), property)]


    def random(self):
       self.last_time_filter = random.choice(self.properties)
