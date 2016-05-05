#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HW1 for RBE 595/CS 525 Motion Planning
#code based on the simplemanipulation.py example
import time
import openravepy

#### YOUR IMPORTS GO HERE ####
import heapq
import math
#### END OF YOUR IMPORTS ####

if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

def waitrobot(robot):
    """busy wait for robot completion"""
    while not robot.GetController().IsDone():
        time.sleep(0.01)

def tuckarms(env,robot):
    with env:
        jointnames = ['l_shoulder_lift_joint','l_elbow_flex_joint','l_wrist_flex_joint','r_shoulder_lift_joint','r_elbow_flex_joint','r_wrist_flex_joint']
        robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])
        robot.SetActiveDOFValues([1.29023451,-2.32099996,-0.69800004,1.27843491,-2.32100002,-0.69799996]);
        robot.GetController().SetDesired(robot.GetDOFValues());
    waitrobot(robot)

if __name__ == "__main__":

    env = Environment()
    env.SetViewer('qtcoin')
    env.Reset()
    # load a scene from ProjectRoom environment XML file
    env.Load("basicMap_V2.env.xml")
    time.sleep(0.1)

    # 1) get the 1st robot that is inside the loaded scene
    # 2) assign it to the variable named 'robot'
    robot = env.GetRobots()[0]
    
    robotRightLeg = env.ReadRobotXMLFile('LegChair_RightBased_V2.robot.xml')
    env.Add(robotRightLeg)
    T1 = matrixFromPose([1.00000,0.00000,0.00000,0.00000,0.40000,1.53000,0.0000])
   


    with env:
        robotRightLeg.SetTransform(T1)
        # the active DOF are translation in X and Y and rotation about the Z axis of the base of the robot.
        robot.SetActiveDOFs([],DOFAffine.X|DOFAffine.Y|DOFAffine.RotationAxis,[0,0,1])

        Pi = math.pi
        goalconfig_l = (23.05,2.45,0,0.5)
        goalconfig_r = (24.35,1.52,0,0.5)
        #### YOUR CODE HERE ####
        
        basicMap = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
				
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25],
				
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
				[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]]

        cell_size = 0.50
        '''initialpos = robot.ComputeAABB().pos()
        print initialpos
        T = robot.GetTransform()'''
        initialconfig_l = (0.4,2.45,0,0)           #include extra field -> height
        initialconfig_r = (0.4,1.53,0,0)
        opened_l = []
        opened_r = []
        heapq.heapify(opened_l)
        heapq.heapify(opened_r)
        closed_l = []
        closed_r = []
        Parent = {initialconfig_r : 'none', initialconfig_l : initialconfig_r}
        g_cost = {initialconfig_l : 0, initialconfig_r : 0}
        astar_free = []
        astar_collide = []
        astar_path = []
        Path = []
        L_TON = 0
        D = 1
        w_height = 0.01
        w_theta = 1
#***************************************************************************************************************************************
        ### getHeight ###

        def getHeight(x,y):
         x_h = float(x/cell_size)
         y_h = float(y/cell_size)
         xgrid = int(math.floor(x_h))
         ygrid = int(math.floor(y_h))
         return basicMap[xgrid][ygrid]

#***************************************************************************************************************************************
        ### Location Cost ###

        def locationCost(neighbour, node):                                                
         xn = neighbour[0]
         yn = neighbour[1]
         #r not rotation based
         xn1 = xn + 0.175
         xn2 = xn + 0.30
         xn3 = xn - 0.175
         xn4 = xn - 0.30
         yn1 = yn + 0.30
         yn2 = yn + 0.60
         yn3 = yn + 0.90
         #h1 = getheight(xn4,yn3)
         #h2 = getHeight(xn4,yn2)
         #h3 = getHeight(xn4,yn1)
         #r only checking non-prong parts of feet
         h4 = getHeight(xn4,yn)
         h5 = getHeight(xn3,yn)
         h6 = getHeight(xn1,yn)
         h7 = getHeight(xn2,yn)
         #h8 = getHeight(xn2,yn1)
         #h9 = getHeight(xn2,yn2)
         #h10 = getHeight(xn2,yn3)
         hcentre = getHeight(xn,yn)
         #r not getting percentage but instead costs based on senario
         #R not all spots even being used, which case is which
         if((h7 != hcentre) or (h6 != hcentre)):
          return 50
         elif((h7 == hcentre) and (h5 != hcentre) and (h4 != hcentre)):
          return 20
         elif((h7 == hcentre) and (h5 == hcentre) and (h4 != hcentre)):
          return 5
         elif((h7 == hcentre) and (h5 == hcentre) and (h4 == hcentre)):
          return 1
         else:
          return 200

 

#***************************************************************************************************************************************         

        def h_manhattan(node):
	 dx = abs(node[0] - goalconfig[0])
	 dy = abs(node[1] - goalconfig[1])
	 return D * (dx+dy)

        # Proximity to goal
        def prox_goal(node,neighbour):
         dx = abs(node[0] - neighbour[0])
	 dy = abs(node[1] - neighbour[1])
	 return D * sqrt(dx * dx + dy * dy)

#***************************************************************************************************************************************
        ### Heuristic ###	

        # Distance to Goal
        def h_euclidean(neighbour,node):        
	 dx = abs(node[0] - neighbour[0])
	 dy = abs(node[1] - neighbour[1])
         #dz = abs(node[2] - neighbour[2])
	 return D * sqrt(dx * dx + dy * dy)

        # Angle Difference to goal
        def angleChange(neighbour,node):
         return abs(node[2] - neighbour[2])

        # Height Difference to goal
        def heightChange(neighbour,node):
         return abs(node[3] - neighbour[3])

########################################################## For H        
        def costHeuristic_l(neighbour,node):                        ########### LEFT                                           
         DT = h_euclidean(neighbour,goalconfig_l)
         AG = angleChange(neighbour,goalconfig_l)
         HG = heightChange(neighbour,goalconfig_l)
         return DT + (w_theta * AG) + (w_height * HG)
       
        def costHeuristic_r(neighbour,node):                        ########### RIGHT                                          
         DT = h_euclidean(neighbour,goalconfig_r)
         AG = angleChange(neighbour,goalconfig_r)
         HG = heightChange(neighbour,goalconfig_r)
         return DT + (w_theta * AG) + (w_height * HG)


#***************************************************************************************************************************************
        ### Compute G ###

        # Transition Cost
        def transCost(neighbour,node):
         dx = abs(node[0] - neighbour[0])
	 dy = abs(node[1] - neighbour[1])
         if(dx == 0.29):
          return 1.36
         if(dx == 0.4992):
          return 2.5
         else:
          return 6         


        # Penalty for Height Change
        #r includes both, assumed is one function

########################################################## For G
        def stepCost(neighbour,node):                                     
         T = transCost(neighbour,node)
         H = heightChange(neighbour,node)
         return T + (w_height * H)

#***************************************************************************************************************************************
        # Successors -> Discrete footsteps
        def getSuccessors_l(node):
         successors = []
         SH = getHeight(node[0]+1,node[1])
         if(node[3] != SH): 
		 '''s1 = (node[0]+0.29,node[1]-0.92,node[2],node[3])
		 successors.append(s1)
		 s2 = (node[0]+0.4992,node[1]-0.92,node[2],node[3])
		 successors.append(s2)
		 s3 = (node[0]+1.052,node[1]-0.92,node[2],node[3])
		 successors.append(s3)
		 s4 = (node[0]+0.29,node[1]-0.92,node[2],node[3]+0.25)
		 successors.append(s4)
		 s5 = (node[0]+0.4992,node[1]-0.92,node[2],node[3]+0.25)
		 successors.append(s5)'''
		 s6 = (node[0]+1.052,node[1]-0.92,node[2],node[3]+0.25)
		 successors.append(s6)
		 return successors
         else:
                 s1 = (node[0]+0.29,node[1]-0.92,node[2],node[3])
		 successors.append(s1)
		 s2 = (node[0]+0.4992,node[1]-0.92,node[2],node[3])
		 successors.append(s2)
		 s3 = (node[0]+1.052,node[1]-0.92,node[2],node[3])
		 successors.append(s3)  
                 return successors

        def getSuccessors_r(node):
         successors = []
         SH = getHeight(node[0]+1,node[1])
         if(node[3] != SH):
		 '''s1 = (node[0]+0.29,node[1]+0.92,node[2],node[3])
		 successors.append(s1)
		 s2 = (node[0]+0.4992,node[1]+0.92,node[2],node[3])
		 successors.append(s2)
		 s3 = (node[0]+1.052,node[1]+0.92,node[2],node[3])
		 successors.append(s3)
		 s4 = (node[0]+0.29,node[1]+0.92,node[2],node[3]+0.25)
		 successors.append(s4)
		 s5 = (node[0]+0.4992,node[1]+0.92,node[2],node[3]+0.25)
		 successors.append(s5)'''
		 s6 = (node[0]+1.052,node[1]+0.92,node[2],node[3]+0.25)
		 successors.append(s6)
		 return successors
         else:
                 s1 = (node[0]+0.29,node[1]+0.92,node[2],node[3])
		 successors.append(s1)
		 s2 = (node[0]+0.4992,node[1]+0.92,node[2],node[3])
		 successors.append(s2)
		 s3 = (node[0]+1.052,node[1]+0.92,node[2],node[3])
		 successors.append(s3)
                 return successors
#***************************************************************************************************************************************

        def update_node_l(neighbour,node):
         h = costHeuristic_l(neighbour,node)
         g_cost[neighbour] = g_cost[node] + stepCost(neighbour,node)
         g = g_cost[neighbour]
         l = locationCost(neighbour,node)
         if((l == 50) or (l == 200)):
          return 'prune'
         else:
          f_neighbour = g + h + l
          return f_neighbour 
 
        def update_node_r(neighbour,node):
         h = costHeuristic_r(neighbour,node)
         g_cost[neighbour] = g_cost[node] + stepCost(neighbour,node)
         g = g_cost[neighbour]
         l = locationCost(neighbour,node)
         if((l == 50) or (l == 200)):
          return 'prune'
         else:
          f_neighbour = g + h + l
          return f_neighbour 

        def display_path(final_node):
         r_white = 1
         node = final_node
         while node is not initialconfig_r:
          if(r_white%2 == 0):
		  print "Path : node: Left",node
		  astar_path.append(env.plot3(points=array(((node[0],node[1],node[3]),(node[0]+0.175,node[1],node[3]),(node[0]+0.30,node[1],node[3]),
		                           (node[0]-0.175,node[1],node[3]),(node[0]-0.30,node[1],node[3]),(node[0]+0.30,node[1]-0.30,node[3]),
		                           (node[0]+0.30,node[1]-0.60,node[3]),(node[0]+0.30,node[1]-0.90,node[3]),(node[0]-0.30,node[1]-0.30,node[3]),
		                           (node[0]-0.30,node[1]-0.60,node[3]),(node[0]-0.30,node[1]-0.90,node[3]))),
		                           pointsize=0.05,
		                           colors=array(((0,0,0))),
		                           drawstyle=1))
		  '''astar_path.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+0.175,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-0.175,neighbour[1],neighbour[3]),(neighbour[0]-0.30,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]+0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.90,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]-0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.90,neighbour[3]))),
		                           pointsize=0.02,
		                           colors=array(((0,0,0))),
		                           drawstyle=1))'''
		  node = Parent[node]
                  r_white += 1
          else:
                  print "Path : node: Right",node
		  astar_path.append(env.plot3(points=array(((node[0],node[1],node[3]),(node[0]+0.175,node[1],node[3]),(node[0]+0.30,node[1],node[3]),
		                           (node[0]-0.175,node[1],node[3]),(node[0]+0.30,node[1],node[3]),(node[0]+0.30,node[1]+0.30,node[3]),
		                           (node[0]+0.30,node[1]+0.60,node[3]),(node[0]+0.30,node[1]+0.90,node[3]),(node[0]-0.30,node[1]+0.30,node[3]),
		                           (node[0]-0.30,node[1]+0.60,node[3]),(node[0]-0.30,node[1]+0.90,node[3]))),
		                           pointsize=0.05,
		                           colors=array(((1,1,1))),
		                           drawstyle=1))
		  '''astar_path.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+0.175,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-0.175,neighbour[1],neighbour[3]),(neighbour[0]-0.30,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]+0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.90,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]-0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.90,neighbour[3]))),
		                           pointsize=0.02,
		                           colors=array(((0,0,0))),
		                           drawstyle=1))'''
		  node = Parent[node]
                  r_white += 1   
           

        '''def reachable(node):                             ############## collision check function
         #r we dont want collision checking with the model here. we want height to be defined as max height so there is no collisions. dependent on the resolution of the foot discritization
         #r if we dont, then we need this. will have to check for time
         robot.SetActiveDOFValues(node);
         incollision = env.CheckCollision(robot)
         if incollision:
          return False
         else:
          return True'''       
        print "Huzzahh"
############################ A* Algorithm ######################################################################
        
        f_start_l = costHeuristic_l(initialconfig_l,goalconfig_l) + g_cost[initialconfig_l] 
        f_cost_l = {initialconfig_l : f_start_l}
        heapq.heappush(opened_l,(f_start_l,initialconfig_l))
        f_start_r = costHeuristic_r(initialconfig_r,goalconfig_r) + g_cost[initialconfig_r] 
        f_cost_r = {initialconfig_r : f_start_r}
        heapq.heappush(opened_r,(f_start_r,initialconfig_r))
        foot = 1
        #while (len(opened_l) and len(opened_r)):
        while len(opened_l):
         if(foot%2 == 0):
                 #print 'started' 
                 foot += 1                                         ###########################################################  Even -> left stable, search right
                 f, node = heapq.heappop(opened_l)
		 closed_l.append(node)
		 prox_ = prox_goal(node,goalconfig_l)
		 if ((prox_ <= 0.06) and (node[3] == 0.5)):                              
		  L_TON += 1
                  foot += 1
                  continue
		 neighbours = getSuccessors_l(node)   
		 for neighbour in neighbours:                                      
		  '''Clear = reachable(neighbour)                                     ## collision check
		  if Clear is False:
		   astar_collide.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+17.5,neighbour[1],neighbour[3]),(neighbour[0]+30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-17.5,neighbour[1],neighbour[3]),(neighbour[0]-30,neighbour[1],neighbour[3]),(neighbour[0]+30,neighbour[1]+30,neighbour[3]),
		                           (neighbour[0]+30,neighbour[1]+60,neighbour[3]),(neighbour[0]+30,neighbour[1]+90,neighbour[3]),(neighbour[0]-30,neighbour[1]+30,neighbour[3]),
		                           (neighbour[0]-30,neighbour[1]+60,neighbour[3]),(neighbour[0]-30,neighbour[1]+90,neighbour[3]))),
		                           pointsize=neighbour[3],
		                           colors=array(((1,0,0))),
		                           drawstyle=1))'''

		  if neighbour not in closed_r:
		   '''astar_free.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]))),
		                           pointsize=0.05,
		                           colors=array(((0,0,1))),
		                           drawstyle=1))
		   astar_free.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+0.175,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-0.175,neighbour[1],neighbour[3]),(neighbour[0]-0.30,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]+0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.90,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]-0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.90,neighbour[3]))),
		                           pointsize=0.05,
		                           colors=array(((0,0,1))),
		                           drawstyle=1))'''

		   if neighbour in f_cost_r.keys():
		    if (f_cost_r[neighbour],neighbour) in opened_r:
		     if (g_cost[neighbour] > g_cost[node] + 1):
		      f_cost_r[neighbour] = update_node_r(neighbour,node)
		   else:
		    Parent[neighbour] = node
		    f_neighbour = update_node_r(neighbour,node) 
		    if(f_neighbour == 'prune'):
		     continue
		    else:
		     f_cost_r[neighbour] = f_neighbour
		     heapq.heappush(opened_r,(f_neighbour,neighbour))
         
                    

         else:    
                 #print 'right'  
                 foot += 1                                      ######################################################################### Odd -> Right stable, search left
         	 f, node = heapq.heappop(opened_r)
		 closed_r.append(node)
		 prox_ = prox_goal(node,goalconfig_r)
		 if ((prox_ <= 0.06 and node[3] == 0.5) or (L_TON == 1)):                              ## change constraints
		  display_path(node)
		  print "Path : node: Right",initialconfig_r
		  break
		 neighbours = getSuccessors_r(node)   
		 for neighbour in neighbours:                                      
		  '''Clear = reachable(neighbour)                                     ## collision check
		  if Clear is False:
		   astar_collide.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+17.5,neighbour[1],neighbour[3]),(neighbour[0]+30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-17.5,neighbour[1],neighbour[3]),(neighbour[0]-30,neighbour[1],neighbour[3]),(neighbour[0]+30,neighbour[1]+30,neighbour[3]),
		                           (neighbour[0]+30,neighbour[1]+60,neighbour[3]),(neighbour[0]+30,neighbour[1]+90,neighbour[3]),(neighbour[0]-30,neighbour[1]+30,neighbour[3]),
		                           (neighbour[0]-30,neighbour[1]+60,neighbour[3]),(neighbour[0]-30,neighbour[1]+90,neighbour[3]))),
		                           pointsize=neighbour[3],
		                           colors=array(((1,0,0))),
		                           drawstyle=1))'''

		  if neighbour not in closed_l:
		   '''astar_free.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]))),
		                           pointsize=0.05,
		                           colors=array(((0,0,1))),
		                           drawstyle=1))
		   astar_free.append(env.plot3(points=array(((neighbour[0],neighbour[1],neighbour[3]),(neighbour[0]+0.175,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1],neighbour[3]),
		                           (neighbour[0]-0.175,neighbour[1],neighbour[3]),(neighbour[0]-0.30,neighbour[1],neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]+0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]+0.30,neighbour[1]-0.90,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.30,neighbour[3]),
		                           (neighbour[0]-0.30,neighbour[1]-0.60,neighbour[3]),(neighbour[0]-0.30,neighbour[1]-0.90,neighbour[3]))),
		                           pointsize=0.05,
		                           colors=array(((0,0,1))),
		                           drawstyle=1))'''

		   if neighbour in f_cost_l.keys():
		    if (f_cost_l[neighbour],neighbour) in opened_l:
		     if (g_cost[neighbour] > g_cost[node] + 1):
		      f_cost_l[neighbour] = update_node_l(neighbour,node)
		   else:
		    Parent[neighbour] = node
		    f_neighbour = update_node_l(neighbour,node) 
		    if(f_neighbour == 'prune'):
		     continue
		    else:
		     f_cost_l[neighbour] = f_neighbour
		     heapq.heappush(opened_l,(f_neighbour,neighbour))
        

        
        print 'L',len(opened_l) 
        print 'R',len(opened_r)
        if ((len(opened_l) == 0) and (len(opened_r) == 0)) : 
         print "No Solution found"
        
        else:
         print "Solution Found"
         '''Path.append(initialconfig)
         L = len(Path)
         traj = RaveCreateTrajectory(env,'')
         traj.Init(robot.GetActiveConfigurationSpecification())
         for step in Path:
          i = 0
          traj.Insert(i,step)
          i += 1
         planningutils.RetimeActiveDOFTrajectory(traj,robot,hastimestamps=False,maxvelmult=1)
         print 'duration',traj.GetDuration()'''
    #robot.GetController().SetPath(traj)
    robot.WaitForController(0)

      
        
         
   
    waitrobot(robot)

    raw_input("Press enter to exit...")

