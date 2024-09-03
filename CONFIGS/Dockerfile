# Use Ubuntu 22.04 LTS as the base image
FROM ubuntu:22.04

LABEL Ricardo Faria <ricardo88faria@gmail.com>

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Combine all package installations, locale configuration, and user setup into a single RUN statement
RUN apt-get update && \
    apt-get install -y \
        sudo \
        file \
        nano \
        locales \
        python3 \
        hostname \
        m4 \
        make \
        perl \
        tar \
        bash \
        tcsh \
        time \
        wget \
        cmake \
        pkg-config \
        libxml2-dev \
        libcurl4-openssl-dev \
        libnetcdf-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    useradd -m swe && echo "swe ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/swe && \
    echo "alias cp='cp -iv'" >> /home/swe/.bashrc && \
    echo "alias mv='mv -iv'" >> /home/swe/.bashrc && \
    echo "alias mkdir='mkdir -pv'" >> /home/swe/.bashrc && \
    echo "alias ll='ls -FGlAhp'" >> /home/swe/.bashrc

# Switch to the new user
USER swe
WORKDIR /home/swe

# Set default command
CMD ["bash"]