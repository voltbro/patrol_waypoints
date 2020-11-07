#!/usr/bin/env python3

#TODO PREVWP save and load, 

import rospy

from patrol_waypoints.srv import patrol_waypoints, patrol_waypointsResponse, patrol_waypointsRequest
from geometry_msgs.msg import Pose2D

# XML parcer's libs
import xml.etree.ElementTree as ET
import copy

class PatrolWaypointsManager():

    
    def __init__(self):
        rospy.init_node('patrol_waypoints_server')
        self.waypoints_list = []
        self.curent_wp = -1

        self.patrol_waypoints_server() 
        # NO CODE BEYOND THIS LINE IN INIT
        
    def add_wp(self, req):
        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo(req.cmd)
            rospy.loginfo(req.num)
            rospy.loginfo(req.waypoint)
            wp = req.waypoint
            if req.num > len(self.waypoints_list):
                self.waypoints_list.append(wp)
                resp.response = "Waypoint appended"
                rospy.loginfo("Waypoint appended")
            elif req.num <= 0:
                self.waypoints_list.append(wp)
                resp.response = "Waypoint appended"
                rospy.loginfo("Waypoint appended")
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

    def goto_wp(self, req):
        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("Waypoint " + str(req.num) + " to go")
            resp.response = "Waypoint " + str(req.num) + " to go"
            resp.waypoint = [self.waypoints_list[req.num - 1]]
            self.curent_wp = req.num - 1
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp
    
    def update_wp(self, req):
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

    def delete_wp(self, req):
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

    def next_wp(self, req):
        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("Next waypoint")
            resp.response = "Next waypoint"
            if self.curent_wp == len(self.waypoints_list) - 1:
                resp.waypoint = [self.waypoints_list[0]]
                self.curent_wp = 0
                resp.response = str(self.curent_wp + 1)
            else:
                resp.waypoint = [self.waypoints_list[self.curent_wp + 1]]
                self.curent_wp += 1
                resp.response = str(self.curent_wp + 1)
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp
    
    def prev_wp(self, req):
        resp = patrol_waypointsResponse()
        try:
            rospy.loginfo("Previous waypoint")
            resp.response = "Previous waypoint"
            if self.curent_wp <= 0:
                resp.waypoint = [self.waypoints_list[len(self.waypoints_list)-1]]
                resp.response = str(len(self.waypoints_list))
                self.curent_wp = len(self.waypoints_list) - 1
            else:
                resp.waypoint = [self.waypoints_list[self.curent_wp - 1]]
                resp.response = str(self.curent_wp)
                self.curent_wp -= 1
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    def list_wp(self, req):
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

    def home_wp(self, req):
        resp = patrol_waypointsResponse()
        wp = Pose2D()
        wp.x = 0
        wp.y = 0
        wp.theta = 0 
        try:
            rospy.loginfo("Going Home")
            resp.response = "Going Home"
            resp.waypoint = [wp]
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    def save_wp(self, req):
        resp = patrol_waypointsResponse()
        wp = Pose2D()
        try:
            waypoints_data_file = ('../data/'+ req.cmd.split()[1]) #TODO to point to correct dir
            root = ET.Element('data')
            for i in range(len(self.waypoints_list)):
                wpt = ET.SubElement(root, 'waypoint')
                wpt.set("id", str(i))
                wpt.set("x",str(self.waypoints_list[i].x))
                wpt.set("y",str(self.waypoints_list[i].y))
                wpt.set("theta",str(self.waypoints_list[i].theta))
            
            tree = ET.ElementTree(root)
            with open(waypoints_data_file, "w") as f:
                tree.write(f, encoding="unicode")

            resp.response = "Waypoints file succesfully saved"
            rospy.loginfo("Waypoints file succesfully saved")
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    def load_wp(self, req):
        rospy.loginfo("Waypoint file parsing started")
        resp = patrol_waypointsResponse()
        wp = Pose2D()
        try:
            waypoints_data_file = ('../data/'+ req.cmd.split()[1]) #TODO to point to correct dir
            tree = ET.parse(waypoints_data_file)
            root = tree.getroot()
            i = 0
            for waypoint in root.findall('waypoint'):
                wp.x = float(waypoint.get('x'))
                wp.y = float(waypoint.get('y'))
                wp.theta = float(waypoint.get('theta'))
                self.waypoints_list.append(copy.deepcopy(wp))
            rospy.loginfo(self.waypoints_list)
            resp.response = "Waypoints file succesfully loaded"
            rospy.loginfo("Waypoints file succesfully loaded")
            return resp
        except Exception as err:
            rospy.loginfo(str(err))
            resp.response = str(err)
            return resp

    def err_req(self, req):
        resp = patrol_waypointsResponse()
        rospy.loginfo("cmd not recognized")
        resp.response = "cmd not recognized"
        return resp
    
    def request_manager(self, req):
        if req.cmd == "add":
            return self.add_wp(req)
        elif req.cmd == "goto":
            return self.goto_wp(req)
        elif req.cmd == "update":
            return self.update_wp(req)
        elif req.cmd == "delete":
            return self.delete_wp(req)
        elif req.cmd == "next":
            return self.next_wp(req)
        elif req.cmd == "prev":
            return self.prev_wp(req)    
        elif req.cmd == "list":
            return self.list_wp(req)
        elif req.cmd == "home":
            return self.home_wp(req)
        elif req.cmd.split()[0] == "save":
            return self.save_wp(req)
        elif req.cmd.split()[0] == "load":
            return self.load_wp(req)
        else:
            return self.err_req(req)

    def patrol_waypoints_server(self):
        s = rospy.Service('patrol_waypoints', patrol_waypoints, self.request_manager)
        rospy.loginfo("Ready to manage waypoints")
        rospy.spin()


if __name__ == "__main__":
    PatrolWaypointsManager()