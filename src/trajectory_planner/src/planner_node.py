#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose2D
from graphical_client.msg import Pose2D_Array
import sympy
import sympy as sym
from sympy.abc import s
from sympy.geometry import Point, Circle,Segment, intersection, Ray

poseSelf= Pose2D()
poseTarget= Pose2D()
poseObs0= Pose2D()
poseObs1= Pose2D()
poseObs2= Pose2D()
poseObs3= Pose2D()
poseObs4= Pose2D()
poseObs5= Pose2D()
poseObs6= Pose2D()
poseObs7= Pose2D()
newP=[]
index=[]
def init_pose():
    pose = Pose2D()
    pose.x = 0
    pose.y = 0
    pose.theta = 0
    return pose
def callbackSelf(dataSelf):
    poseSelf.x =int(dataSelf.x)
    poseSelf.y =int(dataSelf.y)
    poseSelf.theta =int(dataSelf.theta)

def callbackTarget(dataTarget):
    poseTarget.x =int(dataTarget.x)
    poseTarget.y =int(dataTarget.y)
    poseTarget.theta = int(dataTarget.theta)

def callbackObs0(dataObs):
    poseObs0.x = int(dataObs.x)
    poseObs0.y = int(dataObs.y)
    poseObs0.theta = int(dataObs.theta)

def callbackObs1(dataObs):
    poseObs1.x = int(dataObs.x)
    poseObs1.y = int(dataObs.y)
    poseObs1.theta = int(dataObs.theta)

def callbackObs2(dataObs):
    poseObs2.x = int(dataObs.x)
    poseObs2.y = int(dataObs.y)
    poseObs2.theta = int(dataObs.theta)

def callbackObs3(dataObs):
    poseObs3.x = int(dataObs.x)
    poseObs3.y = int(dataObs.y)
    poseObs3.theta = int(dataObs.theta)

def callbackObs4(dataObs):
    poseObs4.x = int(dataObs.x)
    poseObs4.y = int(dataObs.y)
    poseObs4.theta = int(dataObs.theta)

def callbackObs5(dataObs):
    poseObs5.x = int(dataObs.x)
    poseObs5.y = int(dataObs.y)
    poseObs5.theta = int(dataObs.theta)

def callbackObs6(dataObs):
    poseObs6.x = int(dataObs.x)
    poseObs6.y = int(dataObs.y)
    poseObs6.theta = int(dataObs.theta)

def callbackObs7(dataObs):
    poseObs7.x = int(dataObs.x)
    poseObs6.y = int(dataObs.y)
    poseObs7.theta = int(dataObs.theta)

def calcCircs():
    obsCirculo=[]
    obsCirculo.append(Circle(Point(int(poseObs0.x),int(poseObs0.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs1.x),int(poseObs1.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs2.x),int(poseObs2.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs3.x),int(poseObs3.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs4.x),int(poseObs4.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs5.x),int(poseObs5.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs6.x),int(poseObs6.y)), 180))
    obsCirculo.append(Circle(Point(int(poseObs7.x),int(poseObs7.y)), 180))
    return obsCirculo;

def calcIntersect(circles,segment):
    intersect=[]
    intersect.append(intersection(segment, circles[0]))
    intersect.append(intersection(segment, circles[1]))
    intersect.append(intersection(segment, circles[2]))
    intersect.append(intersection(segment, circles[3]))
    intersect.append(intersection(segment, circles[4]))
    intersect.append(intersection(segment, circles[5]))
    intersect.append(intersection(segment, circles[6]))
    intersect.append(intersection(segment, circles[7]))
    return intersect;

def distanceVector(point):
    distances=[]
    n=len(newP)
    for x in xrange(n):
        laux=newP[x]
        distances.append(point.distance(laux[0]))

    return distances;
def arrange(point):
    aux=[]
    distances= distanceVector(point)
    m=len(distances)
    while m != 0 :
        ind_min= distances.index(min(distances))
        aux.append(ind_min)
        del distances[ind_min]
        m=len(distances)

    return aux;

# regresa un objeto Point para librar el obstaculo en cuestion
def recalc(inter, centro,circ):
    a= inter[0]
    b= inter[1]
    seg= Segment(a,b)
    c= seg.midpoint
    line= Ray(centro,c)
    return intersection(line,circ);

def intDiscriminator(list):
    if(len(list)==2):
        out=2
    else :
        out=0

    return out

def planner():
    pub = rospy.Publisher('/trajectory', Pose2D_Array, queue_size=10)
    rospy.Subscriber('/y_r0', Pose2D, callbackSelf)
    rospy.Subscriber('/ball', Pose2D, callbackTarget)
    rospy.Subscriber('/b_r0', Pose2D, callbackObs0)
    rospy.Subscriber('/b_r2', Pose2D, callbackObs2)
    rospy.Subscriber('/b_r1', Pose2D, callbackObs1)
    rospy.Subscriber('/b_r3', Pose2D, callbackObs3)
    rospy.Subscriber('/b_r4', Pose2D, callbackObs4)
    rospy.Subscriber('/b_r5', Pose2D, callbackObs5)
    rospy.Subscriber('/b_r6', Pose2D, callbackObs6)
    rospy.Subscriber('/b_r7', Pose2D, callbackObs7)
    rospy.init_node('planner')
    #rate = rospy.Rate(1) # 10hz!!!! CAMBIARLO

    # while not rospy.is_shutdown():
    pointSelf= Point(int(poseSelf.x),int(poseSelf.y))
    pointTarget= Point(int(poseTarget.x),int(poseTarget.y))
    arr = Pose2D_Array()  #contiene la salida del nodo
    arr.poses.append(poseSelf) #el primer punto siempre es donde se encuentra el robot actualmente
    obstacles= calcCircs()
    trajectory = Segment(pointSelf,pointTarget)
    intersections= calcIntersect(obstacles, trajectory)

    numIntersect= len(intersections[0])+len(intersections[1])+len(intersections[2])+len(intersections[3])+len(intersections[4])+len(intersections[5])+len(intersections[6])+len(intersections[7])

    if numIntersect==0:
        arr.poses.append(poseTarget)
    else:
        while not numIntersect==0 :
            if len(intersections[0])==2 :
                index.append(0)
                newP.append(recalc(intersections[0],Point(poseObs0.x,poseObs0.y), obstacles[0]))
            if len(intersections[1])==2 :
                index.append(1)
                newP.append(recalc(intersections[1],Point(poseObs1.x,poseObs1.y), obstacles[1]))
            if len(intersections[2])==2 :
                index.append(2)
                newP.append(recalc(intersections[2],Point(poseObs2.x,poseObs2.y), obstacles[2]))
            if len(intersections[3])==2 :
                index.append(3)
                newP.append(recalc(intersections[3],Point(poseObs3.x,poseObs3.y), obstacles[3]))
            if len(intersections[4])==2 :
                index.append(4)
                newP.append(recalc(intersections[4],Point(poseObs4.x,poseObs4.y), obstacles[4]))
            if len(intersections[5])==2 :
                index.append(5)
                newP.append(recalc(intersections[5],Point(poseObs5.x,poseObs5.y), obstacles[5]))
            if len(intersections[6])==2 :
                index.append(6)
                newP.append(recalc(intersections[6],Point(poseObs6.x,poseObs6.y), obstacles[6]))
            if len(intersections[7])==2 :
                index.append(7)
                newP.append(recalc(intersections[7],Point(poseObs7.x,poseObs7.y), obstacles[7]))
            print "New points calced: ", newP
            puntosOrdenados= arrange(pointSelf)
            ntraj=[]
            ntraj.append(pointSelf)
            for x in range(len(puntosOrdenados)):
                poseAdd= init_pose()
                laux=newP[puntosOrdenados[x]]
                poseAdd.x=int(laux[0].x)
                poseAdd.y= int(laux[0].y)
                poseAdd.theta= 0
                ntraj.append(laux[0])
                arr.poses.append(poseAdd)

            ntraj.append(pointTarget)
            arr.poses.append(poseTarget)

            nintersect=[]
            numIntersect=0
            # for x in xrange(len(puntosOrdenados)):
            #     seg= Segment(ntraj[x],ntraj[x+1])
            #     nintersect= calcIntersect(obstacles, seg)
            #     numIntersect= numIntersect+len(nintersect[0])+len(nintersect[1])+len(nintersect[2])+len(nintersect[3])+len(nintersect[4])+len(nintersect[5])+len(nintersect[6])+len(nintersect[7])

        print "The array is:", arr
        pub.publish(arr)
        while True:
            b=1
        #rate.sleep()

if __name__ == '__main__':
    try:
        planner()
    except rospy.ROSInterruptException:
        pass
