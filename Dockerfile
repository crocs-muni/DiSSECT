FROM sagemath/sagemath:9.8

# Setup sage and jupyter
RUN sage --pip install --no-cache-dir notebook

# Conform to mybinder
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/sage
ENV TARGET "${HOME}/dissect"

USER root
RUN apt-get update && apt-get install ca-certificates
RUN usermod -l ${NB_USER} sage
COPY . ${TARGET}
RUN chown -R ${NB_UID} ${TARGET}
USER ${NB_USER}

# Install DiSSECT
WORKDIR ${TARGET}
ENV PATH "${HOME}/.sage/local/bin:${PATH}"
RUN sage --pip install --user .
RUN sed -i 's/^#!.*$/#!\/usr\/bin\/env sage/' ${HOME}/.sage/local/bin/dissect-*
ENTRYPOINT []
