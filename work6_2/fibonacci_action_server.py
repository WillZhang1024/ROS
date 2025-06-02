import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci 
import time

class TimerActionServer(Node):

    def __init__(self):
        super().__init__('timer_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci', 
            self.execute_callback)

    async def execute_callback(self, goal_handle):
        self.get_logger().info(f'Received goal to count {goal_handle.request.target_number} seconds.')

        feedback_msg = Fibonacci.Feedback()
        for i in range(goal_handle.request.target_number):
            time.sleep(1)
            feedback_msg.current_time = i + 1
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.current_time}s')

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.total_time = goal_handle.request.target_number
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = TimerActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()
