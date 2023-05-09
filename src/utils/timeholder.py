class Timeholder():
    last_update = 0
    @classmethod
    def update_time(cls, time: int):
        cls.last_update = time
        return
    
    @classmethod
    def get_time(cls):
        return cls.last_update