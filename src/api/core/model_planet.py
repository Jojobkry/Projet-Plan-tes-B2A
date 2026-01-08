class Planet:
    def __init__(self, name, mass, radius, distance):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.distance = distance

    def __repr__(self):
        return f"<Planet {self.name}: mass={self.mass}, radius={self.radius}, distance={self.distance}>"