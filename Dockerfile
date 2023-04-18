FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
ENV PATH=/root/.local/bin:$PATH
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install tesseract-ocr -y
RUN pip install --user -r requirements.txt
COPY ./yolov7 /app/yolov7
ENV PORT 8181

# set command
ENTRYPOINT ["python"]
CMD ["yolov7/main.py"]

