# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rosmobilelib']

package_data = \
{'': ['*']}

install_requires = \
['numpy-quaternion==2019.12.11.22.25.52',
 'numpy>=1.18.4,<2.0.0',
 'opencv-python>=4.3.0,<5.0.0',
 'roslibpy>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'rosmobilelib',
    'version': '0.1.2.1',
    'description': 'rosmobilelib',
    'long_description': "# rosmobilelib\n\nEnable to struct movement robotic action with ROS, the open-source robotic middleware. This library make able to run that by Python3 code on external of ROS network and workspace.\n\nThis is depended [roslibpy](https://github.com/gramaziokohler/roslibpy) that allows ROS programing without defining as ROS Node by using [rospy](http://wiki.ros.org/rospy).\n\n## Main Features\n\n- Manage features to set ROS robotic movement simply.\n- Dynamic schedule to Goal with sending/waiting of Action.\n- Provide some feature that use for programming with ROS such as coordinate transformation of **TF**.\n- Give support to synchronize to single callback for needs to subscribed multi topic such as stereo camera system.\n\n## Installation\n\nTo install rosmobilelib, use `pip`:\n\n```\npip install rosmobilelib\n```\n\nor\n\n```\npip install rosmobilelib --extra-index-url https://test.pypi.org/simple\n```\n\n## Documentation\n\nDetails coming soon. For now, just watch down and get through it.\n\n### Example implementation: \n\nImport libraries.\n\n```\nimport roslibpy as rlp\nfrom rosmobilelib import MobileClient\n```\n\nPrepare connection with roslibpy. If you desire details see [here](https://roslibpy.readthedocs.io/en/latest/examples.html).\n\n```\nclient = rlp.Ros('localhost', port=9090)\nlm1 = lambda: print('is ROS connected: ', client.is_connected)\nclient.on_ready(lm1)\nclient.run()\n```\n\nDefine `MobileClient` object and wait for to subscribe needs topics.\n\n```\nlm2 = lambda r: print('reached goal', r)\nms = MobileClient(client, lm2, odom_topic='/odom', map_topic='/map')\nms.wait_for_ready()\n```\n\nUse dynamic FCFS scheduler. Set goal and make able to execute goals. You can set goal any time not only after call start().\n\nDetails:\n\n- start(), stop(): make scheduling queue executable/inexecutable\n\n```\nms.start()\n\n# set scheduler a goal that go ahead 0.5 from robot body\nms.set_goal_relative_xy(0.5, 0, is_dynamic=False)\n\n# set relative pos(x:front:-0.5, y:left:1) based basis vector that decided dynamic after previous executed\nms.set_goal_relative_xy(-0.5, 1, is_dynamic=True)\n\n# set goal directly with world frame's pose\nms.set_goal(ms.get_vec_q(-0.4,-0.6,0), ms.get_rot_q(0,0,math.pi/2))\n\ntime.sleep(60)\n\nms.stop()\n```\n\nThere are other way to wait for time until reach goal. Exchange `time.sleep(n)` to `ms.wait_for_execute_all()`.\n\n```\n...\nms.wait_for_execute_all()\n...\n```\n",
    'author': 'moyash',
    'author_email': 'www.shinderu.www@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wwwshwww',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
