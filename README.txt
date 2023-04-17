sudo docker build -t mrz .
sudo docker run --rm --init -p 8181:8181 --name mrz mrz
curl -v 0:8181/mrz -H "Content-Type:application/octet-stream" --data-binary @test_image.jpeg
