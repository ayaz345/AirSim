import setup_path
import airsim
import sys
import time

z = float(sys.argv[1]) if len(sys.argv) > 1 else 5
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

client.armDisarm(True)

landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync().join()
else:
    print("already flying...")
    client.hoverAsync().join()

print(f"make sure we are hovering at {z} meters...")

if z > 5:
    # AirSim uses NED coordinates so negative axis is up.
    # z of -50 is 50 meters above the original launch point.
    client.moveToZAsync(-z, 5).join()
    client.hoverAsync().join()
    time.sleep(5)

if z > 10:
    print("come down quickly to 10 meters...")
    z = 10
    client.moveToZAsync(-z, 3).join()
    client.hoverAsync().join()

print("landing...")
client.landAsync().join()
print("disarming...")
client.armDisarm(False)
client.enableApiControl(False)
print("done.")
