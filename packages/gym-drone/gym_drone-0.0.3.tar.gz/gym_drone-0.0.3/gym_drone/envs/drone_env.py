import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

class DroneEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
      p.connect(p.DIRECT)
      p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])
      self.action_space = spaces.Box(np.array([-1]*4)) #düzelt
      self.observation_space = spaces.Box(np.array([-1]*5), np.array([1]*5)) #düzelt

        
    def reset(self):

      p.resetSimulation()
      p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0) 
      p.setGravity(0,0,-10)
      urdfRootPath=pybullet_data.getDataPath()
      

      planeUid = p.loadURDF(os.path.join(urdfRootPath,"plane.urdf"), basePosition=[0,0,-0.65])

      rest_poses = [-0.00014997142013351944, 0.0, -0.00015266248612005358, -0.0001551747838289301]
      self.droneid = p.loadURDF(os.path.join(urdfRootPath, "urdf/Drone.urdf"))
      for i in range(4): #dzüelt
          p.resetJointState(self.droneid,i, rest_poses[i])

      state_motor = []
      for i in range(4):
        for j in range(len(p.getJointState(droneId,i))):
          if type(p.getJointState(droneId,i)[j]) == tuple:
                for k in range(5):
                    state_motor.append(p.getJointState(droneId,i)[j][k])
          else:
            state_motor.append(p.getJointState(droneId,i)[j])


      state_robot = getBasePositionAndOrientation(droneid)  #dzüelt
      observation = state_robot + state_motor  #dzüelt
      p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)
      return observation

    def step(self, action):
        p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING)
        orientation = p.getQuaternionFromEuler([0.,-math.pi,math.pi/2.])
        motor1 = action[0]
        motor2 = action[1]
        motor3 = action[2]
        motor4 = action[3]


        position = []
        velocity = []

        for i in range(4):
          position.append(p.getJointState(droneid,i)[0])
          position.append(p.getJointState(droneid,i)[1])


        m = p.calculateInverseDynamics(self.droneid,position,velocity,action, orientation)

        p.setJointMotorControlArray(self.pandaUid, range(4), p.VELOCİTY_CONTROL, target_velocities = m)


        p.stepSimulation()


        state_object, _ = p.getBasePositionAndOrientation(self.objectUid)
        state_motor = []
        for i in range(4):
          for j in range(len(p.getJointState(droneId,i))):
            if type(p.getJointState(droneId,i)[j]) == tuple:
                  for k in range(5):
                      state_motor.append(p.getJointState(droneId,i)[j][k])
            else:
              state_motor.append(p.getJointState(droneId,i)[j])

        state_robot = getBasePositionAndOrientation(droneid)  #dzüelt
        observation = state_robot + state_motor
        return obs, reward, done, info

        if 0.50 > state_object[2] > 0.45:
            reward = 1
            done = True
        else:
            reward = 0
            done = False
        info = state_object
        observation = state_robot + state_fingers
        return observation, reward, done, info


    def render(self, mode='human'):

      view_matrix = p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0.7,0,0.05],
                                                          distance=.7,
                                                          yaw=90,
                                                          pitch=-70,
                                                          roll=0,
                                                          upAxisIndex=2)
      proj_matrix = p.computeProjectionMatrixFOV(fov=60,
                                                    aspect=float(960) /720,
                                                    nearVal=0.1,
                                                    farVal=100.0)
      (_, _, px, _, _) = p.getCameraImage(width=960,
                                            height=720,
                                            viewMatrix=view_matrix,
                                            projectionMatrix=proj_matrix,
                                            renderer=p.ER_BULLET_HARDWARE_OPENGL)

      rgb_array = np.array(px, dtype=np.uint8)
      rgb_array = np.reshape(rgb_array, (720,960, 4))

      rgb_array = rgb_array[:, :, :3]
      return rgb_array

        
    def close(self):
      p.disconnect()
