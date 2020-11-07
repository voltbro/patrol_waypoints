# patrol_waypoints
Turtlebro patrol waypoints service

Commands for service which should been envoked through rosservice call method.
The structure of command is as follow:
cmd "String"
num "int32"
Waypoint #Pose2D object
x "float64"
y "float64"
theta "float64"

example:
rosservice call /patrol_waypoints "cmd: 'add'
num: '2'
waypoint:
    x: '1.0'
    y: '2.1'
    theta: '90'"
This exapmle will add waypoint with coordinates x 1.0 y 2.1 and left turn by 90 degrees to the second place in list if exist or append it to the end of the list if no 2nd waypoint exist yet


cmd "add" appending the waypoint written below to the waypoints list
if num != "0" adding the waypoint written below to the index equals of num the waypoints list splited in such case

cmd "delete" removing waypoint from waypoints list
if num => "0" it removes biggest by index (left in list) waypoint, else it removes the waypoint with index equals to num
indexes of waypoints list started with 1 not 0!

cmd "update" changing waypoint's valuse with index equals to num

cmd "list" returns list of waypoints currently existing in service

cmd "next" returns next waypoint. The return is single Pose2D object in list.

cmd "prev" returns previous waypoint. The return is single Pose2D object in list.

cmd "goto" returns single Pose2D object - waypoint from waypoint list with index equals to num.

cmd "save filename" saves XML file with waypoints list into /data/ folder
example:
rosservice call /patrol_waypoints "cmd: 'save goals.xml'
num: ''
waypoint
    x: ''
    y: ''
    theta: ''"

cmd "load filename" loads XML file with waypoints lists and appends it to existing waypoints list from /data/ folder

