FROM ubuntu:24.04

ARG INSTALL_ROOT="/root/.local"
ENV PATH="${INSTALL_ROOT}/bin:${PATH}"

RUN apt-get update && \
    apt-get -y install \
        mc \
        git \
        curl \
        nano \
        tar \
        less \
        tree \
        python3 \
        python3-pip

COPY ./mc_ini_nice_colors/ini "/root/.config/mc/"

ARG MAMBA_URL="https://micro.mamba.pm/api/micromamba/linux-64/latest"
RUN mkdir -p ${INSTALL_ROOT} && \
    curl -Ls ${MAMBA_URL} | tar -C ${INSTALL_ROOT} -xvj bin/micromamba

RUN micromamba shell init --shell bash && \
    echo "micromamba activate" >> ~/.bashrc

SHELL ["micromamba", "run", "/bin/bash", "--login", "-c"]

RUN micromamba install -y cartopy -c conda-forge
RUN pip install \
    loguru \
    tqdm \
    hydra-core \
    h5py \
    pyresample \
    geopy \
    scikit-learn \
    black \
    ruff

ARG PROJECT_WORKDIR="/root/dpr_wind_speed"
RUN mkdir -p ${PROJECT_WORKDIR} && cd ${PROJECT_WORKDIR}

RUN git config --global --add safe.directory ${PROJECT_WORKDIR}

WORKDIR ${PROJECT_WORKDIR}
#ENTRYPOINT ["python", "-m", "bin.main"]
