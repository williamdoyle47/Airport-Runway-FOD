class Detection:
#add type hints
    def __init__(self, fod_type, location, datetime, confidence_score):
        self.fod_type = fod_type
        self.location = location
        self.datetime = datetime
        self.confidence_score = confidence_score
        # self.size = size
        # self.weight = weight
        #self.image = image
    
    def __str__(self):
        message = (
            "FOD Detected!\n"
            f"Type: {self.fod_type}\n"
            f"Coordinates: {self.location}\n"
            f"Datetime: {self.datetime}\n"
            f"confidence_score: {self.confidence_score}"
        )
        return message

if __name__ == "__main__":
    det = Detection("juice", "[0,0]", "11/19/21",".9" )
    print(det.__str__())

