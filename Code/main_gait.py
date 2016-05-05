#Author : varun verlencar
"""
Main implementation of Bipedal Gait trajectory
"""
import time
import openravepy
from copy import deepcopy
from math import sin,cos,acos,asin,pow,sqrt,atan2
from math import degrees as d
import random

if not __openravepy_build_doc__:
	from openravepy import *
	from numpy import *

def get_footsteps(_file_name):
	#get footsteps from footstep planner solution
	with open(_file_name) as f:
		footsteps = [[0,0,0,0,0,0]]
		for line in f:
			line = line.split() # to deal with blank 
			if line:	# lines (ie skip them)
				line = [float(i) for i in line]
				footsteps.append(line)
	return footsteps

def waitrobot(robot):
	"""busy wait for robot completion"""
	while not robot.GetController().IsDone():
		time.sleep(0.01)
def get_init_foot():
	return 0

def randomGoalIk(x,z,baseFoot):
	
	while (True):
		
		#generate random values for support leg
		 t0 = (random.random()*(pi/2.0))-(pi/4.0)
		 t1 = (random.random()*(pi/2.0))-(pi/2.0)
		 t2 = (random.random()*(1.0*pi))-(pi/2.0)
		 
		 t01 = t0+t1
		 t012 = t01+t2
		 
		 if ((t012 > 0.349066) or (t012 < -0.349066)):
			 # print('Chair angle fail')
			 # print('')
			 continue
		 l = 62.0
		 
		 #foward kinematics from support ankle to hip node
		 xhip = l*sin(t0) + l*sin(t01)
		 zhip = l*cos(t0) + l*cos(t01)
		 
		 # print('hip', xhip,zhip)
		 direction = 1.0
		 if (baseFoot == 'left'):
			 direction = 1.0
		 elif (baseFoot == 'right'):
			 direction = -1.0
			 #~define fail case
		 #define new reference for goal point to place ankle of swing leg
		 xNew = (direction*100*x) - xhip
		 zNew = zhip- (100*z)
		 
		 #rotate referrence frame to use standard equations
		 copyX = deepcopy(xNew)
		 xNew = deepcopy(zNew)
		 zNew = -1.0*deepcopy(copyX)
		 
		 # print('new s',xNew,zNew)
		 phi = 0.0 #total angle constrant to define third joint of swing leg, based in rotated reference frame
		 
		 
		 #calculate needed values
		 x2 = pow(xNew,2)
		 z2 = pow(zNew,2)
		 ls = pow(l,2)
		 dist = sqrt(x2 + z2)
		 
		 #check that desired point is withing workspace of swing leg
		 if (dist > 124.0):
			 # print('dist fail')
			 continue
		
		 #calculate angle of knee joint
		 t4 = acos( ((x2+z2)-(ls+ls))/(2*l*l))
		 
		 #calculate joint one, t4 or hip joint
		 gamma = acos( (x2 + z2 + ls - ls)/(2*l*sqrt(x2 + z2)))
		 beta = atan2(zNew,xNew) 
		 t3 = beta - gamma
		 
		 #calculate ankle joint to maintaing flat ground contact
		 t5 = phi - (t3+t4)
		 
		 #convert calculated joints to reference basis for Legchair model
		 t3Real = t3-t012 #account for rotation of hip frame due to support leg angles
		 t4Real = t4
		 t5Real = t5
		 
		 
		 #print values
		 # print('in joints', d(t0),d(t1),d(t2))
		 # print('calculated joints',d(t3),d(t4),d(t5))
		 # print('updated joints', d(t0),d(t1),d(t2),d(t3Real),d(t4Real),d(t5Real))
		 # print('fk', l*cos(t3)+l*cos(t3+t4),l*sin(t3)+l*sin(t3+t4))
		 # print('gamma inner',(x2 + z2 + ls - ls)/(2*l*sqrt(x2 + z2)))
		 # print('gamma', gamma)
		 # print('beta', beta)
		 
		 #check that all joint constraints are met
		 if ( (t3Real < -1.0*pi/2) or (t3Real > 1.0*pi/2)):
			 # print('t3fail')
			 # print('')
			 continue
		 
		 if ( (t4Real < 0) or (t3Real > 1.0*pi/2)): #opposite of ik direction
			 # print('t4fail')
			 # print('')
			 continue
			 
		 if ( (t5Real < -1.0*pi/4) or (t3Real > 1.0*pi/4)): #opposite of ik direction
			 # print('t5fail')
			 # print('')
			 continue
		 
		 if ((t0+t1+t2+t3Real+t4Real+t5Real) != 0):
			 # print('tAllfail')
			 # print('')
			 continue
		 
		 
		 #return random-calculated succesful joints for desired pose
		 break
	# print [[t0, t1, t2, t3Real, t4Real, t5Real],[l*cos(t0)+l*cos(t0+t1),l*sin(t0)+l*sin(t0+t1)]]
	return [[t0, t1, t2, t3Real, t4Real, t5Real],[l*cos(t0)+l*cos(t0+t1),l*sin(t0)+l*sin(t0+t1)]]

if __name__ == "__main__":

	env = Environment()
	env.SetViewer('qtcoin')
	env.Reset() 

	# load a scene
	env.Load('plannerplugin/scenes/basicMap_V2.env.xml')
	time.sleep(0.1)
	robot2 = env.ReadRobotXMLFile('plannerplugin/robots/LegChair_RightBased_V3.robot.xml')

	# get the robot
	robot1 = env.GetRobots()[0]
	robot = robot2

	RaveInitialize()
	RaveLoadPlugin('plannerplugin/build/plannerplugin')

	jointnames = ['leftAnkle','leftKnee','leftHip','rightHip','rightKnee','rightAnkle']
	indices = [robot.GetJoint(name).GetDOFIndex() for name in jointnames]

	flag = True
	zp = 1
	T = robot1.GetTransform() 
	TR = T[0:4,3]	
	goalconfig =[]
	startconfig = [[0,0,0,0,0,0]]
	

	########### Find IK solution #############
	footsteps = get_footsteps('Footsteps/Basic/footsteps_basic.txt')
	# tt = 1
	# ttt =1
	# tttt =1
	# while(tt):
	# 	g = randomGoalIk(1.452,0,'left')[0]
	# 	pos = randomGoalIk(1.452,0,'left')[1]
	# 	if (abs(pos[0] - 0.4 <0.5) and ttt):
	# 		goalconfig = goalconfig.append(g)
	# 		ttt =0
	# 		print goalconfig
	# 	elif (abs(pos[0] - 1.452 <0.5) and tttt):
			# tttt= 0
	# 	elif (ttt == 0 and tttt==0):
	# 		tt = 0
	baselegName = 'left'
	for i in range(1,len(footsteps)):
		if(i ==0):
			baselegName = 'left'
		if(i%2 ==0):
			baselegName = 'right'
		else:
			baselegName = 'right'
		# print footsteps[i][0]-footsteps[i-1][0],'\n'
		g = randomGoalIk(footsteps[i][0]-footsteps[i-1][0],0,baselegName)
		# print g[0]
		goalconfig.append(g[0])
		startconfig.append(g[0])
	print goalconfig
		
	###check solutions below######
	# for i in range(0,len(goalconfig)):
	# 	with env:
	# 		robot1.SetActiveDOFs([robot1.GetJoint(name).GetDOFIndex() for name in jointnames])
	# 		robot1.SetActiveDOFValues(goalconfig[i]);
	# 		env.UpdatePublishedBodies() # allow viewer to update new robot
	# 		time.sleep(5.0/len(goalconfig))



	########### Plan Gait #############
	left_foot_orient = 0 # for dynamic walking
	right_foot_orient = 0
	foot_orient = 0 #for static walking
	_smoothPath = []; nodes =[]; lowerlimit=[];upperlimit=[];_unsmoothPath =[]
		
	######Test cases#######
	# startconfig = [[0,0,0,0,0,0],[.3,-0.35,-0.17,-.17,.35,0.05],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.30],[0,0,0,0,0,0],[.3,-0.35,-0.17,-.17,.35,0.05],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.30]]
	# goalconfig = [[.3,-0.35,-0.17,-.17,.35,0.05],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.30],[0,0,0,0,0,0],[.3,-0.35,-0.17,-.17,.35,0.05],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.30],[0,0,0,0,0,0]]
		
	# goalconfig = [[-.05,-0.35,0.17,.17,.35,-0.3]]
	# startconfig = [[.3,-0.35,-0.17,-.17,.35,0.05]]

	# s = [[0,0,0,0,0,0],[.25,-0.15,-0.1,-.1,-.15,0.25],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.3],[0,0,0,0,0,0],[.25,-0.15,-0.1,-.1,-.15,0.25]]
	# g = [[.25,-0.15,-0.1,-.1,-.15,0.25],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.3],[0,0,0,0,0,0],[.25,-0.15,-0.1,-.1,-.15,0.25],[0,0,0,0,0,0]]

	# startconfig = [[0,0,0,0,0,0],[.25,-0.15,-0.1,-.1,-.15,0.25],[0,0,0,0,0,0],[-0.05,-0.35,0.17,.17,.35,-0.3]] + s + s + s +s
	# goalconfig = g + g + g + g + g

	# g = [[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3],[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3]]
	# s = [[-0.05,-0.35,0.17,.17,.35,-0.3],[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3],[.3,-0.35,-0.17,-.17,.35,0.05]]
	# goalconfig = [[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3],[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3]]+g +g+g
	# startconfig = [[0,0,0,0,0,0],[.3,-0.35,-0.17,-.17,.35,0.05],[-0.05,-0.35,0.17,.17,.35,-0.3],[.3,-0.35,-0.17,-.17,.35,0.05]]+s+s+s
	

	next_foot = 0 #set 0 for Leftbase model and 5(as per other foot) for Rightbase model
	stepsize = [0.25]
	goalbias = [0.26]
	baseleg = [0,1,2]
	BiRRT = 1 #set 1 for BI-RRT 0 for RRT

	plannermodule = RaveCreateModule(env,'plannermodule')
	
	for m in range(0,len(goalconfig)): 
		
		with env:	
			if next_foot == 0:
				robot = robot1	
				baseleg = [0,1,2]
				flag = False				
				next_foot = 5	
				f1 = open('Footsteps/Basic/Bi-RRT/Leftfoot2.txt', 'a'); 
				if zp !=1:
					env.Add(robot)
					env.Remove(robot2)	
					zp =2				
					T = robot.GetTransform()[0:4,0:4]
					T[0,3] = TR[0]
					T[1,3] = TR[1]
					T[2,3] = TR[2]
					T[3,3] = TR[3]								
					robot.SetTransform(T)	
						
			else:
				robot = robot2	
				# baseleg = [5,4,3]	
				env.Remove(robot1)
				env.Add(robot)
				flag = True
				next_foot = 0
				zp = 2
				T = robot.GetTransform()[0:4,0:4]
				T[0,3] = TR[0]
				T[1,3] = TR[1]
				T[2,3] = TR[2]
				T[3,3] = TR[3]
				robot.SetTransform(T)
				f1 = open('Footsteps/Basic/Bi-RRT/Rightfoot2.txt', 'a');
			f1.write("\n\nPlan\n")

			
			env.UpdatePublishedBodies() 
			robot.SetActiveDOFs([robot.GetJoint(name).GetDOFIndex() for name in jointnames])
			robot.SetActiveDOFValues(startconfig[m]);
			
			initConfig =  startconfig[m] + goalconfig[m] + goalbias + stepsize + baseleg + [BiRRT]
			a = time.time()
			print "Planning Started"
			path = plannermodule.SendCommand('gaitplanner %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f end'%tuple(initConfig))
			a = time.time()-a
			print '\n time:', a
			

			if path is None:
				raveLogWarn('command failed!')
			else:
				bisect = path.split(';');
				cuta = bisect[0].split(',')
				cutb = bisect[1].split(',')

				for i in range(0,len(cuta)-1):
					frag=cuta[i].split();
					frag=[float(i) for i in frag];
					_unsmoothPath.append(frag);

				for i in range(0,len(cutb)-1):
					frag=cutb[i].split();
					frag=[float(i) for i in frag];
					_smoothPath.append(frag);
		
			lowerlimit,upperlimit = robot.GetDOFLimits(indices)

			handles2=[]
			for i in (_unsmoothPath):
				arr=array([i[0],i[1],i[2],i[3],i[4],i[5]])
				robot.SetActiveDOFValues(arr)
				pt=robot.GetManipulator('foot').GetTransform()[0:3,3]
				handles2.append(env.plot3(pt,pointsize=0.025,colors=array(((1,0,0))),drawstyle=1))

			handles1=[]
			for i in (_smoothPath):
				# for k in range(0,len(i)-1):
				# 	if (i[k] != goalconfig[m][k]):
				# 		if (i[k] < lowerlimit[k]):
				# 			i[k]  = lowerlimit[k]
				# 		elif(i[k] > upperlimit[k]):
				# 			i[k] = upperlimit[k]
				arr=array([i[0],i[1],i[2],i[3],i[4],i[5]])
				robot.SetDOFValues(arr,indices)
				pt=robot.GetManipulator('foot').GetTransform()[0:3,3]
				handles1.append(env.plot3(pt,pointsize=0.03,colors=array(((0,0,1))),drawstyle=1))
				# env.UpdatePublishedBodies() 

			traj = RaveCreateTrajectory(env,'')
			traj.Init(robot.GetActiveConfigurationSpecification())		

			for j in range(0,len(_smoothPath)):
				traj.Insert(j,_smoothPath[j])
				pp = ['Node']+[j]+_smoothPath[j]
				f1.write(str(pp))
				f1.write("\n")
			f1.write(str('Computation Time:'))
			f1.write(str(a))
			numNodes = len(_unsmoothPath)
			f1.write(str('	Nodes:'))
			f1.write(str(numNodes))
			f1.write(str('	Bias:'))
			f1.write(str(goalbias))
			f1.write(str('	Step Size:'))
			f1.write(str(stepsize))
			f1.close()
				

			planningutils.RetimeActiveDOFTrajectory(traj,robot,hastimestamps=False,maxvelmult=1)
			print 'duration',traj.GetDuration()
			
		robot.GetController().SetPath(traj)
		robot.WaitForController(0)
		TR = robot.GetManipulator('foot').GetTransform()[0:4,3]

		### END OF YOUR CODE ###
		waitrobot(robot)
	raw_input("Press enter to exit...")
""" Trjectory execution"""
