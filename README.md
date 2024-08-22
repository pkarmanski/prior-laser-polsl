# prior-laser-polsl

## Short description about work flow
1. In order to not mix libraries version between projects we will use docker so please install it link: https://www.docker.com/products/docker-desktop/.
2. To run project from IDE right click Dockerfile and select run 'Dockerfile' (first run will take some time but next will go fast). Tutorial how to set it up yourself, but you will not need to do it: https://www.youtube.com/watch?v=ck6xQqSOlpw&ab_channel=IntelliJIDEA%2CaJetBrainsIDE.
3. If you add any library to your project that is not in the installation/freeze.cfg make sure to add it to this file [example](installation/freeze.cfg:1).
4. Recommend to install GitToolBox because it automatically makes fetch. 
5. Note that besides using docker you need to have same environment in your IDE otherwise it will not give you warnings about code mistakes
6. We are using python3.12.2
7. Comments are not required, but please name your variables that while reading their name we will know what they do


### Dictionary
TODO
Stage - 
Laser - 
Printing -


### Changes
pkarmanski 22.08.2024:
- added scaling int for now
- added file upload button next to file list

bl4szk4 - 12.08.2024
- moved drawing to a separate service
- WIP drawing a preview on canvas
- small code fixes

pkarmanski - 11.08.2024 ver 1.0.19:
- preapared methods for loading file preview on canvas (still working on it)

bl4szk4 - 05.08.2024 ver 1.0.18
- Code refactor
- Added new panel
- changes in processing dxf file

bl4szk4, pkarmanski - 15.06.2024 ver 1.0.17
- Fixed notification
- Added styling for notifications
- Added basic notifications for connections and calibration
- Added destructor for MainWindow so the stage is disconnected in a safe way
- Setting default coms for stage and laser
- Updating coms
- Drag and drop for files and check box for source of drawing
- Implementation of threading

bl4szk4, pkarmanski - 10.06.2024 ver 1.0.16:
- refactored code for handling dxf files
- changed notification for msg box
- added method drawing to print_lines, so it will work depending on user choice
- removed unused files

bl4szk4 - 03.06.2024 ver 1.0.15:
- added methods for drawing lines, circles and arcs
- cleaned code for reading dxf files

pkarmanski - 27.05.2024 ver 1.0.14:
- added try catch for laser dao
- added handler for laser init
- tried to make notification

bl4szk4, pkarmanski - 24.05.2024 ver 1.0.13:
- Displaying position on main panel
- Added Prior connection handling
- Disabling other buttons but connection buttons at start

bl4szk4, pkarmanski - 21.05.2024 ver 1.0.12:
- added commands for TTL
- stage_connector renamed to prior_connector
- prior_connector moved from stage dao to service and now its is passed to stage dao and laser dao
- moved from stage dao prior connections functions
- created method for handling canvas input and "printing" them with stage and laser

bl4szk4, pkarmanski - 18.05.2024 ver 1.0.11:
- prepared notification class but it is not working yet
- extended calibration function for getting measurements of stage size
- prepared scaling function but it is not tested yet
- connected function for calibration and laser writing with buttons
- added buttons for creating stage and laser instances and connecting them with proper service functions

bl4szk4 - 14.05.2024 ver 1.0.10
- Added [css file](app/presentation/styling/main.css) for storing all custom styles
- added a base class for custom grid [basic_grid](app/presentation/components/basic_grid.py)
- added new component for displaying info about a stage [stage_info](app/presentation/components/stage_info_grid.py)
- added component with 2 buttons for basic actions [management](app/presentation/components/stage_management_grid.py)
- fixed styling in main window
- added [com port selection](app/presentation/components/com_port_grid.py) for selection of com ports for stage and laser
- added [laser by arduino](app/laser/laser_connector.py) to connect project with an arduino
- added actions to buttons to start connection with arduino and write PWM value to arduino / for testing

bl4szk4 - 10.05.2024 ver 1.0.9
- Added first version of canvas that allows to draw on the screen

bl4szk4 - 10.05.2024 ver 1.0.8:
- Fixed the problem with the app's icon. Icons are stored in [enum](app/presentation/icons/icons.py)

bl4szk4, pkarmanski - 09.05.2024 ver 1.0.8:
- refactored presentation folder and its classes so it fits whole project coding style

pkarmanski, bl4szk4 - 25.04.2024 ver 1.0.7:
- fixed some bugs while testing programme on the stage
- added [stop stage method](app/stage/daos/stage_dao.py)

pkarmanski, bl4szk4 - 24.04.2024 ver 1.0.6:
- prepared methods for writing points to the stage and checking its position and state
- checking position is handled in a separate thread
- added lock for [execute method](app/stage/daos/stage_connector.py)
- prepared tests to be handled

pkarmanski, bl4szk4 - 17.04.2024 ver 1.0.5:
- added serial to freeze.cfg for instalment
- added method for getting available com list
- added method for checking running status and position
- added attributes to StageDAO for checking its status
- added test file with random postition for further testing the methods

pkarmanski, bl4szk4 - 16.04.2024 ver 1.0.4:
- added stage commands enum class and factory for it
- create initialize stage methods like connect, open_session, close_session in StageDAO
- created basic calibration logic, added pydantic to configuration

bl4szk4 - 11.04.2024 ver 1.0.1:
- added enum with [stage errors](app/stage/enums/error_codes.py)

pkarmanski - 11.04.2024 ver 1.0.1:
- added version to [main.py](main.py:3) please update it if you make any change on dev branch
- moved functions responsible for connection to class [Stage](app/stage/daos/stage/stage.py:9) from StageDAO
- attached log config file to logging package

bl4szk4 - 10.04.2024 ver 1.0.0:
- created directory utils with yaml_manager to handle configuration from [yaml file](config.yaml)
- created [directory](app/messages) and added two files for storing info and error codes about stage
- imported [package](app/stage/x64) provided by Prior
- started work with [stage](app/stage/daos/stage_dao.py)

pkarmanski - 10.04.2024 ver 1.0.0:
- imported [library](main.py:1) (it is just an example how to write about update you don't really need to write about every package you have imported)
- created example of work flow
- added frame with directories and classes for project
- added short descriptions what classes supposed to do



