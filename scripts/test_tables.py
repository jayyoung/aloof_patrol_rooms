import rospy
import sys

from strands_perception_msgs.msg import Table
from geometry_msgs.msg import PoseWithCovariance, Polygon, Point32

from mongodb_store.message_store import MessageStoreProxy
from strands_perception_msgs.msg import Table

from strands_navigation_msgs.msg import TopologicalNode


if __name__ == '__main__':
    rospy.init_node('test_tables', anonymous = False)

    nx = Table()

    msg_store=MessageStoreProxy()

    my_table = Table()
    my_table.table_id = "SouthWestTable"
    my_table.header.frame_id = "/map"  # The parent frame that the table is in

    table_pose = PoseWithCovariance()  # The transformation to the table frame
    # Fill in the table position...
    my_table.pose = table_pose

    polygon = Polygon()                # The table top surrounding polygon in the table frame
    # Fill in the points in the polygon...

    polygon.points = [
    Point32(4,9.7,0.95),
    Point32(4,8.8,0.95),
    Point32(2.1,8.8,0.95),
    Point32(2.1,9.7,0.95),
    ]

    my_table.tabletop = polygon

    rospy.loginfo(polygon)

    # Store the table
    msg_store.insert(my_table)

    table_list = msg_store.query(Table._type)


    rospy.loginfo(table_list)
