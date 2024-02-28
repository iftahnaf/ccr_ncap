# General Information

This repository contains [Euro NCAP](https://www.euroncap.com/en/about-euro-ncap/) tests in [CARLA](https://carla.org//) simulator.

* [test_1](./test_1/) folder contains CCRs(Car-to-Car Rear stationary) test scenario in which an ego car accelerates and then brakes in from of a stationary car from 100m.

The folder contains few utilities:

1. [Controller](./test_1/controller.py) - contains simple PD and P controllers for the throttle / brake based on the current relative distance.
2. [Dynamics](./test_1/dynamics.py) - retrieve information about the state of the ego car.
3. [Scene](./test_1/scene.py) - functions to manage the simulation.
4. [Visualizer](./test_1/visualizer.py) - functions to plot ground-truth bounding box around the stationary car.
5. [Analysis](./test_1/analysis.py) - parse the `data.csv` file and plot few insights from the simulation.

<video width="640" height="480" controls>
  <source src="./test_1/test_1.mp4">
</video>

* [test_2](./test_2/) folder holds the modified [manual_control.py](https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/manual_control.py) version, integrated with lane detector, visualize the vehicle's current lanes boundaries. **(Currently contains a bug in the waypoint selection 28/02/2024)**

![](./test_2/test_2.png)

# Prerequisite

1. [CARLA docker image](https://carla.readthedocs.io/en/latest/build_docker/) - `0.9.15` version.
2. CARLA Python package, install with:

                pip install carla==0.9.15


# Install

1. Clone this repository:

                git clone git@github.com:iftahnaf/ccr_ncap.git

2. Pull the CARLA docker image `0.9.15` version:

                docker pull carlasim/carla:0.9.15

*Note: make sure that you can run docker without sudo*


# Run

* Run `test_1` with:
  
                cd ccr_ncap/
                python3 ./test_1/main.py

