#!/usr/bin/env python3

#TODO PREVWP save and load, 

import rospy

from patrol_waypoints.srv import patrol_waypoints, patrol_waypointsResponse, patrol_waypointsRequest
from geometry_msgs.msg import Pose2D

class PatrolWaypointsManager():
    
    def __init__(self):

        rospy.init_node('patrol_waypoints_server')
        self.waypoints_list = []
        self.wpselector = 0

        self.patrol_waypoints_server() 
        # NO CODE BEYOND THIS LINE IN INIT
        
    def addwp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo(req.cmd)
            rospy.loginfo(req.num)
            rospy.loginfo(req.waypoint)
            wp = req.waypoint
            if req.num > len(self.waypoints_list):
                self.waypoints_list.append(wp)
                resp.response = "Waypoint added"
            elif req.num <= 0:
                self.waypoints_list.append(wp)
                resp.response = "Waypoint added"
            elif req.num < len(self.waypoints_list) and req.num > 0:
                first_part_of_wp_list = self.waypoints_list[:(req.num-1)]
                second_part_of_wp_list = self.waypoints_list[(req.num-1):]
                first_part_of_wp_list.append(wp)
                first_part_of_wp_list.extend(second_part_of_wp_list)
                self.waypoints_list = first_part_of_wp_list
                resp.response = "Waypoint" + str(req.num) + "added"
            resp.waypoint = [wp]
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    
    def gotowp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("Waypoint " + str(req.num) + " to go")
            resp.response = "Waypoint " + str(req.num) + " to go"
            resp.waypoint = [self.waypoints_list[req.num - 1]]
            self.wpselector = req.num
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    
    def updatewp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo(req.cmd)
            rospy.loginfo(req.num)
            rospy.loginfo(req.waypoint)
            wp = req.waypoint
            self.waypoints_list[req.num - 1] = wp   
            resp.response = "Waypoint " + str(req.num) + " updated"
            resp.waypoint = [wp]
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp


    def deletewp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo(req.cmd)
            rospy.loginfo(req.num)
            rospy.loginfo(req.waypoint)
            wp = self.waypoints_list.pop(req.num - 1)   
            resp.response = "Waypoint " + str(req.num) + " deleted"
            resp.waypoint = [wp]
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp
    
    def listwp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("List of waypoints")
            resp.response = "List of waypoints"
            resp.waypoint = self.waypoints_list
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp


    def nextwp(self, req):

        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("Next waypoint")
            resp.response = "Next waypoint"
            if self.wpselector < len(self.waypoints_list):
                resp.waypoint = [self.waypoints_list[self.wpselector]]
                self.wpselector += 1
            else:
                resp.waypoint = [self.waypoints_list[0]]
                self.wpselector = 1
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    #TODO PREVWP save and load

    def err_req(self, req):

        resp = patrol_waypointsResponse()
        rospy.loginfo("cmd not recognized")
        resp.response = "cmd not recognized"
        return resp

    
    def request_manager(self, req):

        if req.cmd == "add":
            return self.addwp(req)
        elif req.cmd == "goto":
            return self.gotowp(req)
        elif req.cmd == "update":
            return self.updatewp(req)
        elif req.cmd == "delete":
            return self.deletewp(req)
        elif req.cmd == "next":
            return self.nextwp(req)
        elif req.cmd == "prev":
            return self.prevwp(req)    
        elif req.cmd == "list":
            return self.listwp(req)
        elif req.cmd == "home":
            return self.homewp(req)
        elif req.cmd == "save":
            return self.homewp(req)
        elif req.cmd == "load":
            return self.homewp(req)
        else:
            return self.err_req(req)


    def patrol_waypoints_server(self):

        s = rospy.Service('patrol_waypoints', patrol_waypoints, self.request_manager)
        rospy.loginfo("Ready to manage waypoints")
        rospy.spin()

if __name__ == "__main__":
    PatrolWaypointsManager()