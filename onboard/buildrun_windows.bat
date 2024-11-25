docker build --platform linux/amd64,linux/arm64 -t app .
mkdir build
docker save -o ./build/app.tar app
docker run app
scp ./build/app.tar groupc@hsi.local:~/
pause