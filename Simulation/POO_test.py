class Person:

    def __init__(self, x, y, status='healthy', age, hygiene):
        self.x = x
        self.y = y
        self.status = status
        self.age = age
        self.hygiene = hygiene

    def change_status(self,newstatus):
        self.status = newstatus
    
