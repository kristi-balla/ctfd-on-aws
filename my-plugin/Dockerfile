FROM ctfd/ctfd:3.8.2@sha256:870e396fddf8dd1273252bae5842bda96e45d5ebbe83d1d737ef76c513055619

# i just want to use whatever ctfd delivered
# with as few modifications as possible
# hadolint ignore=DL3045
COPY requirements.txt ./

# hadolint ignore=DL3042
RUN pip install -r requirements.txt

RUN mkdir -p /opt/CTFd/CTFd/plugins/my-flag
COPY . /opt/CTFd/CTFd/plugins/my-flag
