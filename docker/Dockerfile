FROM mambaorg/micromamba:1.5.9 as micromamba

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

USER root
ARG MAMBA_USER=mambauser
ARG MAMBA_USER_ID=57439
ARG MAMBA_USER_GID=57439
ENV MAMBA_USER=$MAMBA_USER
ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV MAMBA_EXE="/bin/micromamba"

COPY --from=micromamba "$MAMBA_EXE" "$MAMBA_EXE"
COPY --from=micromamba /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_shell.sh /usr/local/bin/_dockerfile_shell.sh
COPY --from=micromamba /usr/local/bin/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_initialize_user_accounts.sh /usr/local/bin/_dockerfile_initialize_user_accounts.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_setup_root_prefix.sh /usr/local/bin/_dockerfile_setup_root_prefix.sh

RUN /usr/local/bin/_dockerfile_initialize_user_accounts.sh && \
    /usr/local/bin/_dockerfile_setup_root_prefix.sh

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    git \
    bzip2 \
    unzip \
    curl \
    sudo \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    build-essential \
    cmake \
    libboost-all-dev \
    libeigen3-dev \
    libtbb2 \
    libtbb-dev \
    libsqlite3-dev \
    libpng-dev \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libjsoncpp-dev \
    libxml2-dev \
    libbz2-dev \
    libz-dev \
    libcairo2-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/
RUN git clone https://github.com/molecularinformatics/roshambo.git
WORKDIR /app/roshambo 
RUN micromamba create -n roshambo python=3.9 -y -c conda-forge
RUN micromamba install -n roshambo -c conda-forge boost-cpp boost cairo pandas pillow freetype cmake numpy eigen matplotlib -y

WORKDIR /app/roshambo
RUN git clone  https://github.com/rdkit/rdkit.git
WORKDIR /app/roshambo/rdkit
# RUN git checkout Release_2023_03_1
# RUN sed 's/23ed3f833c1ae0adb141a26b4a30d73e/850b0df852f1cda4970887b540f8f333/g' Code/GraphMol/MolDraw2D/CMakeLists.txt > Code/GraphMol/MolDraw2D/CMakeLists.txt


RUN mkdir /app/roshambo/rdkit/build
WORKDIR /app/roshambo/rdkit/build
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba run -n roshambo cmake \
    -DPy_ENABLE_SHARED=1   \
    -DRDK_INSTALL_INTREE=ON   \
    -DRDK_BUILD_AVALON_SUPPORT=ON   \
    -DRDK_BUILD_INCHI_SUPPORT=ON   \
    -DRDK_INSTALL_STATIC_LIBS=OFF   \
    -DRDK_BUILD_CPP_TESTS=ON   \
    -DRDK_BUILD_PYTHON_WRAPPERS=ON   \
    -DRDK_BUILD_YAEHMOP_SUPPORT=ON   \
    -DBoost_NO_SYSTEM_PATHS=ON   \
    -DRDK_BUILD_CAIRO_SUPPORT=ON   \
    -DRDK_BUILD_XYZ2MOL_SUPPORT=ON   \
    -DRDK_BUILD_FREESASA_SUPPORT=ON   \
    -DPYTHON_NUMPY_INCLUDE_PATH=/opt/conda/envs/roshambo/lib/python3.9/site-packages/numpy/_core/include   \
    -DBOOST_ROOT="$CONDA_PREFIX" \
    -DRDK_INSTALL_COMIC_FONTS=OFF  \
    -DINCHI_URL=https://rdkit.org/downloads/INCHI-1-SRC.zip   ..
RUN micromamba run -n roshambo make -j4 install

WORKDIR /app/roshambo/rdkit
ENV RDBASE=/app/roshambo/rdkit
ENV PYTHONPATH=$RDBASE
ENV LD_LIBRARY_PATH=$RDBASE/lib:$CONDA_PREFIX/lib

WORKDIR /app/roshambo/
ENV RDKIT_LIB_DIR=$RDBASE/lib
ENV RDKIT_INCLUDE_DIR=$RDBASE/Code
ENV RDKIT_DATA_DIR=$RDBASE/Data
ENV PYTHONPATH=$PYTHONPATH:$RDBASE
ENV CUDA_HOME=/usr/local/cuda

RUN micromamba run -n roshambo pip install -e .
RUN micromamba run -n roshambo pip install IPython pandas jupyter

SHELL ["/usr/local/bin/_dockerfile_shell.sh"]