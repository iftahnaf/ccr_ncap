#################### BASE IMAGE ####################
FROM ubuntu:22.04 as base

# Installing pip
RUN apt-get update && apt-get install -y python3-pip ffmpeg libsm6 libxext6 libgl1

RUN pip3 install --upgrade pip
RUN pip install carla==0.9.15 pygame numpy opencv-python matplotlib pandas

####################################################


FROM base as dev

COPY test_1 /test_1
COPY test_2 /test_2

CMD [ "/bin/bash" ]