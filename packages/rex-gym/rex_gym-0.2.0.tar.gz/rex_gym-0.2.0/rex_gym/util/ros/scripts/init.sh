#!/bin/bash
echo Get rex-gym source code
curl --request GET -sL \
     --url 'https://github.com/nicrusso7/rex-gym/archive/master.zip'\
     --output "$HOME/catkin_ws/src"
cd "$HOME/catkin_ws" || catkin_make
source ./devel/setup.bash
echo Update Rex urdf file
sed 's/stl\//package:\/\/rex-gym\/rex_gym\/util\/pybullet_data\/assets\/urdf\/stl\//g' "$HOME/catkin_ws/src/rex-gym/rex_gym/util/pybullet_data/assets/urdf/rex.urdf" > rex_ros.urdf
echo Start ROS node
roscore &