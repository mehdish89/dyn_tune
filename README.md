# dyn_tune
**dyn_tune** is a package providing automatic tuning of dynamically reconfigurable parameters for a simulated or physical robotic system operating in ROS. Every parameter that is defined using [dynamic_reconfigure](http://wiki.ros.org/dynamic_reconfigure) package, could potentially be tuned using this tool. The user is in charge of providing a ROS bag as ground truth/experiment, as well as defining an objective funciton over the values published on ROS topics. The objective value for each set of parameter values determines how favorable those parameter values are. A stochastic optimization algorithm is used to find the optimum set of values for the parameters. 

## Install/Test
For installing this package, first create a Catkin workspace if you dont have it already.
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/
$ catkin_init_workspace
```
Then, clone the repository in it and build the workspace.

```
$ cd ~/catkin_ws/src
$ git clone https://github.com/mehdish89/dyn_tune
$ catkin_make
$ source ~/catkin_ws/devel/setup.bash
```
Once everything is built, you could utilize the tool for parameter tuning by running the command below and using ROS services.
```
$ rosrun dyn_tune dyn_tune_main.py
```
Use the command below to see a list of services available.
```
$ rosservice list 
/create_function
/dyn_tune_backbone/get_loggers
/dyn_tune_backbone/set_logger_level
/list_available_functions
/optimize
/rosout/get_loggers
/rosout/set_logger_level
```
## GUI
You could utilize the tool in a much more conveniently, by installing [rqt_dyn_tune](https://github.com/mehdish89/rqt_dyn_tune) package, which is a rqt plugin graphical user interface for **dyn_tune**.

![alt text](https://raw.githubusercontent.com/mehdish89/rqt_dyn_tune/master/rqt_dyn_tune.png)

## Applications
Since the optimization method is completely end-to-end, a wide range of parameters could be tuned using **dyn_tune** with no knowledge of underlying mechanism required. The package could be used for tuning simulation parameters, caliberation of sensors/cameras, tuning PIDs, etc. The advantage to this method is that user only need to specify the expected outcome rather than implementing a caliberation/tuning method based on the mechanics of the task/problem. In another word, the user does not need to worry about the nature of the parameters and what is the right value for them. Instead, they are only required to specify the high-level expected outcome of the task that should presumably be achieved by the right values for the parameters.
