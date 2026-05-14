# carla_nuscenes
Generate dataset in nuscenes format using Carla! You can config your dataset in configs.
- change lidar rotation frequency from 100 to 20hz in calibrated_sensors.yaml
- change parse_lidar_data in sensor.py
- change timestamps unit in  transform_timestamp in utils.py to microseconds 10e5 to 1e6
