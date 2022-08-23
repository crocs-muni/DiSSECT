FROM sagemath/sagemath:9.4

# Setup sage and jupyter
RUN sage --pip3 install --no-cache-dir notebook

# Conform to mybinder
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/sage
ENV TARGET "${HOME}/dissect"
COPY . ${TARGET}

USER root
RUN sed -i -re 's/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN apt-get update && apt-get install ca-certificates
RUN usermod -l ${NB_USER} sage
RUN chown -R ${NB_UID} ${TARGET}

# Install DiSSECT
USER ${NB_USER}
WORKDIR ${TARGET}
RUN sage --pip3 install --editable .
ENV PATH "${HOME}/sage/local/bin:${PATH}"
ENTRYPOINT []
