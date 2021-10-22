FROM ubuntu:18.04

RUN apt-get update

RUN mkdir /workspace
WORKDIR /workspace

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    htop \
    iotop \
    tmux \
    nano \
    iputils-ping \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# Switch to bash shell
SHELL ["/bin/bash", "-c"]

# Install Miniconda and Python
ADD https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh miniconda3.sh
RUN /bin/bash miniconda3.sh -b -p /conda \
    && rm miniconda3.sh \
    && echo export PATH=/conda/bin:$PATH >> .bashrc
ENV PATH="/conda/bin:${PATH}"

# install python packages
COPY ./*.yaml /workspace/
RUN conda env create -f /workspace/conda_env.yaml
SHELL ["conda", "run", "-n", "simple_env", "/bin/bash", "-c"]

#copy app files
COPY ./*.py /workspace/
COPY entrypoint.sh /workspace/entrypoint.sh
RUN ["chmod", "+x", "/workspace/entrypoint.sh"]

RUN mkdir -p /workspace/static
COPY ./static /workspace/static/

RUN mkdir /workspace/save

EXPOSE 5006

ENTRYPOINT ["bash","/workspace/entrypoint.sh"]

