import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci

class TimerActionClient(Node):

    def __init__(self):
        super().__init__('timer_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, seconds):
        goal_msg = Fibonacci.Goal()
        goal_msg.target_number = seconds

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected.')
            return
        self.get_logger().info('Goal accepted.')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Time: {feedback_msg.feedback.current_time}s')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Done! Total time: {result.total_time}s')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = TimerActionClient()
    client.send_goal(12)
    rclpy.spin(client)
