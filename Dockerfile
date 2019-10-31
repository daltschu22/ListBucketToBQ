FROM python:3.7-alpine

WORKDIR /usr/src

# Copies the code
COPY requirements.txt /usr/src/requirements.txt

RUN apk update \
    && apk add bash gcc git g++ libxml2-dev libxslt-dev musl-dev \
    && pip install -r requirements.txt \
    && rm -rf /tmp/* \
    && rm -rf /var/cache/apk/* \
    && rm -rf /var/tmp/*

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh--usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup

# Path configuration
ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
# Make sure gsutil will use the default service account
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

# Copies the code
COPY list_bucket.py /usr/src/list_bucket.py

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "/usr/src/list_bucket.py"]
