cp ~/Dev/data/nn_weights/yolov7-tiny-mrz.pt yolov7
cp ~/Dev/data/nn_weights/yolov7.pt yolov7
sudo docker build -f Dockerfile -t mrz .
sudo docker run --rm --init -p 8181:8181 --name mrz mrz
curl -v 0:8181/mrz -H "Content-Type:application/octet-stream" --data-binary @test_image.jpeg
