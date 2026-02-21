import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __sub__(self, no):
        #Вычитание точек (вектор из no в self)
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)
        
    def dot(self, no):
        #Скалярное произведение векторов
        return self.x * no.x + self.y * no.y + self.z * no.z
        
    def cross(self, no):
        #Векторное произведение векторов
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )
        
    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    AB = b - a
    BC = b - c
    CD = d - c
    
    # Вычисляем нормали к плоскостям (векторные произведения)
    X = AB.cross(BC)  # нормаль к плоскости ABC
    Y = BC.cross(CD)  # нормаль к плоскости BCD
    
    # Вычисляем косинус угла между нормалями
    dot_product = X.dot(Y)
    mag_X = X.absolute()
    mag_Y = Y.absolute()
    
    # Избегаем деления на ноль
    if mag_X == 0 or mag_Y == 0:
        return 0.0
    
    cos_phi = dot_product / (mag_X * mag_Y)
    
    # Ограничиваем значение косинуса диапазоном [-1, 1]
    cos_phi = max(-1.0, min(1.0, cos_phi))
    
    # Берём абсолютное значение для получения острого угла (0-90 градусов)
    cos_phi = abs(cos_phi)
    
    # Вычисляем угол в радианах, затем переводим в градусы
    angle_rad = math.acos(cos_phi)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg

if __name__ == '__main__':
    pass
