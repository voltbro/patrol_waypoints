# patrol_waypoints
Turtlebro patrol waypoints service

commands for service which should been envoked through rosservice call method

cmd "add" appending the waypoint written below to the waypoints list
if num != "0" adding the waypoint written below to the index equals of num the waypoints list splited in such case

cmd "delete" removing waypoint from waypoints list
if num == "0" it removes biggest by index (left in list) waypoint, else it removes the waypoint with index equals to num
indexes of waypoints list started with 1 not 0!

cmd "update" changing waypoint's valuse with index equals to num

cmd "list" returns list of waypoints currently existing in service

cmd "next" returns next waypoint. The return is single Pose2D object in list.

cmd "prev" returns previous waypoint. The return is single Pose2D object in list.

cmd "goto" returns single Pose2D object - waypoint from waypoint list with index equals to num.

cmd "save filename" saves XML file with waypoints list into /data/ folder

cmd "load filename" loads XML file with waypoints lists and appends it to existing waypoints list from /data/ folder


