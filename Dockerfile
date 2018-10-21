FROM ubuntu:18.04
WORKDIR /opt/dolos
RUN apt-get update && apt-get install -y python3-minimal python3-distutils wget curl lsb-release gnupg
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 ./get-pip.py
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD https://storage.googleapis.com/kubernetes-release/release/v1.11.3/bin/linux/amd64/kubectl /usr/local/bin/kubectl
RUN chmod +x /usr/local/bin/kubectl
