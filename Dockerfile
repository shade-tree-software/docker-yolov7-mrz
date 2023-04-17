FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
ENV PATH=/root/.local/bin:$PATH
RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get install tesseract-ocr libtesseract-dev -y
RUN pip install --user -r requirements.txt
COPY ./src /app/src
COPY ./tesseract/tessdata /app/src/tesseract/tessdata
ENV PORT 8181
ENV TESSERACT_DATA_PATH /app/src/tesseract/tessdata

# set command
ENTRYPOINT ["python"]
CMD ["src/yolov7/main.py"]
