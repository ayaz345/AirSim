# Python client example to get Lidar data from a drone, although this script works for any AirSim-supported vehicle
# This script is for Lidar sensors using 'VehicleInertialFrame' as DataFrame under settings.json
# Sample settings.json used for this script:
'''
{
    "SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/main/docs/settings_json.md",
    "SettingsVersion": 1.2,

    "SimMode": "Multirotor",

     "Vehicles": {
        "Drone1": {
            "VehicleType": "SimpleFlight",
            "AutoCreate": true,
            "Sensors": {
                "LidarSensor1": { 
                    "SensorType": 6,
                    "Enabled" : true,
                    "NumberOfChannels": 1,
                    "RotationsPerSecond": 10,
                    "Range":12,
                    "PointsPerSecond": 8000,
                    "X": 0, "Y": 0, "Z": -1,
                    "Roll": 0, "Pitch": 90, "Yaw" : 0,
                    "VerticalFOVUpper": 0,
                    "VerticalFOVLower": 0,
                    "HorizontalFOVStart": 0,
                    "HorizontalFOVEnd": 0,
                    "DrawDebugPoints": true,
                    "DataFrame": "VehicleInertialFrame"
                },
                "LidarSensor2": { 
                    "SensorType": 6,
                    "Enabled" : true,
                    "NumberOfChannels": 1,
                    "RotationsPerSecond": 10,
                    "Range":12,
                    "PointsPerSecond": 8000,
                    "X": 0, "Y": 0, "Z": -1,
                    "Roll": 90, "Pitch": 90, "Yaw" : 0,
                    "VerticalFOVUpper": 0,
                    "VerticalFOVLower": 0,
                    "HorizontalFOVStart": 0,
                    "HorizontalFOVEnd": 0,
                    "DrawDebugPoints": true,
                    "DataFrame": "VehicleInertialFrame"
                }
            }
        }
    }
}
'''
import setup_path 
import airsim
import numpy as np

class LidarTest:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.VehicleClient()
        self.client.confirmConnection()
        print('Connected!\n')

    def execute(self,vehicle_name,lidar_names):
        print('Scanning Has Started\n')
        print('Use Keyboard Interrupt \'CTRL + C\' to Stop Scanning\n')
        existing_data_cleared = False   #change to true to superimpose new scans onto existing .asc files
        try:
            while True:
                for lidar_name in lidar_names:
                    filename = f"{vehicle_name}_{lidar_name}_pointcloud.asc"
                    f = open(filename,'w') if not existing_data_cleared else open(filename,'a')
                    lidar_data = self.client.getLidarData(lidar_name=lidar_name,vehicle_name=vehicle_name)

                    for i in range(0, len(lidar_data.point_cloud), 3):
                        xyz = lidar_data.point_cloud[i:i+3]

                        f.write("%f %f %f %d %d %d \n" % (xyz[0],xyz[1],xyz[2],255,255,0))
                    f.close()
                existing_data_cleared = True
        except KeyboardInterrupt:
            airsim.wait_key('Press any key to stop running this script')
            print("Done!\n")

# main
if __name__ == "__main__":
    lidarTest = LidarTest()
    lidarTest.execute('Drone1',['LidarSensor1','LidarSensor2'])
