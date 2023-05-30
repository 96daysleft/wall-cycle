import random

class SortOptions:

    @property
    def hot(self):
        return "hot"
    
    @property
    def new(self):
        return "new"
    
    @property
    def top(self):
        return "top"
    
    @property
    def controversial(self):
        return "controversial"
     
    @property
    def rising(self):
        return "rising"
        
    @property
    def best(self):
        return "best"

    def properties(self):
        return [prop for prop in dir(self) if isinstance(getattr(self, prop), property)]


    def random(self):
       self.last_time_filter = random.choice(self.properties)
