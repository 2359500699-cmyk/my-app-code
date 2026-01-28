import json
import os
class RoomDataManager:
    def _init_(self,filename="roomdata.json"):
        self.filename=filename
        self.data=self.load_data()
    def load_data(self):