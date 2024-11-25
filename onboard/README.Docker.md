# Building and running your application

### RUN ALL COMMANDS FROM THIS DIRECTORY
Note: 
- Can run buildrun_windows.bat on windows for streamlining most of this process
- Can run buildrun_linux_mac.sh on linux or mac for streamlining most of this process

### Ensure docker desktop is running 

To build onboard application run the following from this directory 
    - "app" will be the name of the build image
    - the arm64 platform is necessary for deployment on raspberry pi

`docker build --platform linux/amd64,linux/arm64 -t app .`

To run the container run:
`docker run app`


Note: To see all your docker images run the following command
`docker images`

# Deploying to raspberry pi

Save the application image as a tar file using the following command:
`docker save -o ./build/app.tar app`

Copy the image to the raspberry pi using scp
`scp ./build/app.tar groupc@hsi.local:~/`

(On on the pi) Load the image 
`docker load -i ~/app.tar`
