# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

import setup_path
import airsim

client = airsim.VehicleClient()
client.confirmConnection()

pose = client.simGetVehiclePose()
print(
    f"x={pose.position.x_val}, y={pose.position.y_val}, z={pose.position.z_val}"
)

angles = airsim.to_eularian_angles(client.simGetVehiclePose().orientation)
print(f"pitch={angles[0]}, roll={angles[1]}, yaw={angles[2]}")

pose.position.x_val = pose.position.x_val + 1
client.simSetVehiclePose(pose, True)