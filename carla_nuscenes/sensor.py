import numpy as np
import carla
from .actor import Actor

def parse_image(image):
    array = np.ndarray(
            shape=(image.height, image.width, 4),
            dtype=np.uint8, buffer=image.raw_data,order="C")
    return array
 
def parse_lidar_data(lidar_data):
    # Read raw buffer as float32 (x, y, z, intensity) — avoids float64 conversion
    pts = np.frombuffer(lidar_data.raw_data, dtype=np.float32).reshape(-1, 4)

    # Filter CARLA no-hit sentinel values
    pts = pts[np.isfinite(pts).all(axis=1)].copy()

    # CARLA left-handed → nuScenes right-handed coordinate system
    pts[:, 1] = -pts[:, 1] #TODO: try to comment out this line

    # Scale intensity [0.0, 1.0] → [0.0, 255.0] to match nuScenes
    pts[:, 3] = np.clip(pts[:, 3] * 255.0, 0, 255)

    # Build channel index column (replaces the manual loop)
    channels = np.zeros(len(pts), dtype=np.float32)
    idx = 0
    for ch in range(lidar_data.channels):
        count = lidar_data.get_point_count(ch)
        channels[idx:idx + count] = ch
        idx += count

    return np.column_stack([pts, channels])  # (N, 5) float32

def parse_radar_data(radar_data):
    points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4')).copy()
    return points

def parse_data(data):
    if isinstance(data,carla.Image):
        return parse_image(data)
    elif isinstance(data,carla.RadarMeasurement):
        return parse_radar_data(data)
    elif isinstance(data,carla.LidarMeasurement):
        return parse_lidar_data(data)

def get_data_shape(data):
    if isinstance(data,carla.Image):
        return data.height,data.width
    else:
        return 0,0
class Sensor(Actor):
    def __init__(self, name, **args):
        super().__init__(**args)
        self.name = name
        self.data_list = []
    
    def get_data_list(self):
        return self.data_list
    
    def set_actor(self, id):
        super().set_actor(id)
        self.actor.listen(self.add_data)
    
    def spawn_actor(self):
        super().spawn_actor()
        self.actor.listen(self.add_data)

    def get_last_data(self):
        if self.data_list:
            return self.data_list[-1]
        else:
            return None
            
    def add_data(self,data):
        self.data_list.append((self.actor.parent.get_transform(),data))

    def get_transform(self):
        return self.actor.get_transform()
