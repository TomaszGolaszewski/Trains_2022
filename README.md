# Trains_2022
Railway traffic control simulator written in an object-oriented way

**Project still under development**

## Instruction
- To play **'Trains'**, run the file _main_Trains2.py_
- On the right side of the window there is a control panel to control the trains.


<p align="center">
  <img src="screenshots/screenshot2.png" alt="Trains">
</p>


## To do list
- [x] Rewrite old code from Train_2015 in new object-oriented way:
  - [x] Use Python with Pygame library;
  - [x] Make space for the future open world map;
  - [x] Draw trains with sprites.
<!-- - [ ] Save map and all map-related data in database -->
- [ ] Add a feature allowing to build/modify the map:
 - [x] Basic function allowing to add new elements to the map.
<!-- - [ ] Add procedurally generating algorithm for expanding map -->
- [ ] Add AI for train engineer:
  - [x] basic check if the track in front of the train is free;
  - [x] check semaphore;
  - [x] check if the track in front of the train is reserved;
  - [ ] path-finding.
- [x] Add AI for station master:
  - [x] add semaphores;
  - [x] add control boxes:
    - [x] wait,
    - [x] return,
    - [x] load/unload,
    - [ ] control box as path-finding target.
- [ ] Add user-friendly interface.


<p align="center">
  <img src="screenshots/screenshot3.png" alt="Trains">
</p>
