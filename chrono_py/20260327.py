import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as irr
import math as m
import os


def main():

    # ================== 车辆 ==================
    hmmwv = veh.HMMWV_Full()

    # 👉 加速用（很重要）
    hmmwv.SetContactMethod(chrono.ChContactMethod_NSC)

    hmmwv.SetChassisCollisionType(veh.CollisionType_NONE)
    hmmwv.SetChassisFixed(False)
    hmmwv.SetInitPosition(chrono.ChCoordsysd(initLoc, initRot))

    # 👉 用轻量模型（不然会卡）
    hmmwv.SetEngineType(veh.EngineModelType_SIMPLE)
    hmmwv.SetTransmissionType(veh.TransmissionModelType_AUTOMATIC_SIMPLE_MAP)

    hmmwv.SetDriveType(veh.DrivelineTypeWV_AWD)
    hmmwv.SetSteeringType(veh.SteeringTypeWV_PITMAN_ARM)

    hmmwv.SetTireType(veh.TireModelType_TMEASY)
    hmmwv.SetTireStepSize(tire_step_size)

    hmmwv.Initialize()

    # ================== 可视化 ==================
    hmmwv.SetChassisVisualizationType(veh.VisualizationType_MESH)
    hmmwv.SetSuspensionVisualizationType(veh.VisualizationType_PRIMITIVES)
    hmmwv.SetSteeringVisualizationType(veh.VisualizationType_PRIMITIVES)
    hmmwv.SetWheelVisualizationType(veh.VisualizationType_MESH)
    hmmwv.SetTireVisualizationType(veh.VisualizationType_MESH)

    hmmwv.GetSystem().SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)

    # ================== 地面 ==================
    terrain = veh.RigidTerrain(hmmwv.GetSystem())

    patch_mat = chrono.ChContactMaterialNSC()
    patch_mat.SetFriction(0.9)

    patch = terrain.AddPatch(patch_mat, chrono.CSYSNORM, 100, 100)
    patch.SetTexture(veh.GetDataFile("terrain/textures/tile4.jpg"), 200, 200)

    terrain.Initialize()

    # ================== 可视化 ==================
    vis = veh.ChWheeledVehicleVisualSystemIrrlicht()
    vis.SetWindowTitle("Torque Control Demo")
    vis.SetWindowSize(1280, 1024)
    vis.SetChaseCamera(trackPoint, 6.0, 0.5)
    vis.Initialize()
    vis.AddSkyBox()
    vis.AddLightDirectional()
    vis.AttachVehicle(hmmwv.GetVehicle())

    # 👉 关闭 realtime（非常重要）
    hmmwv.GetVehicle().EnableRealtime(False)

    # ================== 获取轮子 ==================
    vehicle = hmmwv.GetVehicle()
    axles = vehicle.GetAxles()

    wheel_fl = axles[0].GetWheels()[0]
    wheel_fr = axles[0].GetWheels()[1]
    wheel_rl = axles[1].GetWheels()[0]
    wheel_rr = axles[1].GetWheels()[1]

    # ================== 仿真循环 ==================
    while vis.Run():

        time = hmmwv.GetSystem().GetChTime()

        vis.BeginScene()
        vis.Render()
        vis.EndScene()

        # ================== 控制输入（你之后接RL就在这里） ==================

        delta = 0.2   # 转向
        T = 200       # 扭矩大小

        T_fl = T
        T_fr = T
        T_rl = T
        T_rr = T

        # ================== 设置 steering ==================
        steering = vehicle.GetSteering(0)
        steering.SetInput(delta)

        # ================== 对轮子施加 torque ==================

        # ⚠️ 如果车不动，把 Y 改成 Z 试试
        torque_vec = chrono.ChVector3d(0, T, 0)

        wheel_fl.GetSpindle().AddTorque(torque_vec)
        wheel_fr.GetSpindle().AddTorque(torque_vec)
        wheel_rl.GetSpindle().AddTorque(torque_vec)
        wheel_rr.GetSpindle().AddTorque(torque_vec)

        # ================== 同步 ==================
        terrain.Synchronize(time)
        hmmwv.Synchronize(time, veh.DriverInputs(), terrain)

        # ================== 推进 ==================
        terrain.Advance(step_size)
        hmmwv.Advance(step_size)
        vis.Advance(step_size)

    return 0


# ================== 参数 ==================
initLoc = chrono.ChVector3d(0, 0, 1.6)
initRot = chrono.ChQuaterniond(1, 0, 0, 0)

trackPoint = chrono.ChVector3d(0.0, 0.0, 1.75)

step_size = 3e-3
tire_step_size = 1e-3

veh.SetDataPath(chrono.GetChronoDataPath() + "vehicle/")

main()