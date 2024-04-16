# prior-laser-polsl

## Short description about work flow
1. In order to not mix libraries version between projects we will use docker so please install it link: https://www.docker.com/products/docker-desktop/.
2. To run project from IDE right click Dockerfile and select run 'Dockerfile' (first run will take some time but next will go fast). Tutorial how to set it up yourself, but you will not need to do it: https://www.youtube.com/watch?v=ck6xQqSOlpw&ab_channel=IntelliJIDEA%2CaJetBrainsIDE.
3. If you add any library to your project that is not in the installation/freeze.cfg make sure to add it to this file [example](installation/freeze.cfg:1).
4. Recommend to install GitToolBox because it automatically makes fetch. 
5. Note that besides using docker you need to have same environment in your IDE otherwise it will not give you warnings about code mistakes
6. We are using python3.12.2
7. Comments are not required, but please name your variables that while reading their name we will know what they do

### Example of readme update

pkarmanski, bl4szk4 - 16.04.2024 ver 1.0.4:
- added stage commands enum class and factory for it
- create initialize stage methods like connect, open_session, close_session in StageDAO

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



