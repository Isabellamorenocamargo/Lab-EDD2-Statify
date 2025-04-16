class Artist:
    
    def __init__(self, uniqueID: int, name: str):
        self.uniqueID = uniqueID
        self.name = name
        self.left = None
        self.right = None
        self.balance = 0
    
    def __str__(self):
        return f"{self.name}"