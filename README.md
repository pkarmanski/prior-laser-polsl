# prior-laser-polsl

## Short description about work flow
1. In order to not mix libraries version between projects we will use docker so please install it link: https://www.docker.com/products/docker-desktop/.
2. To run project from IDE right click Dockerfile and select run 'Dockerfile' (first run will take some time but next will go fast). Tutorial how to set it up yourself, but you will not need to do it: https://www.youtube.com/watch?v=ck6xQqSOlpw&ab_channel=IntelliJIDEA%2CaJetBrainsIDE.
3. If you add any library to your project that is not in the installation/freeze.cfg make sure to add it to this file [example](installation/freeze.cfg:1).
4. Recommend to install GitToolBox because it automatically makes fetch. 
5. Note that besides using docker you need to have same environment in your IDE otherwise it will not give you warnings about code mistakes
6. We are using python3.12.2
7. Comments are not required, but please name your variables that while reading their name we will know what they do

### Changes

bl4szk4 - 14.05.2024 ver 1.0.10
- Added [css file](app/presentation/styling/main.css) for storing all custom styles
- added a base class for custom grid [basic_grid](app/presentation/components/basic_grid.py)
- added new component for displaying info about a stage [stage_info](app/presentation/components/stage_info_grid.py)
- added component with 2 buttons for basic actions [management](app/presentation/components/stage_management_grid.py)
- fixed styling in main window

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



