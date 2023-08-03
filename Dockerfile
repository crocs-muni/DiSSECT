FROM sagemath/sagemath:9.8

ENV HOME /home/sage
ENV TARGET "${HOME}/dissect"

USER root
RUN apt-get update && apt-get install ca-certificates
COPY . ${TARGET}
RUN chown -R sage ${TARGET}
USER sage

WORKDIR ${TARGET}
ENV PATH "${HOME}/.sage/local/bin:${PATH}"
RUN sage --pip install --user .
RUN sed -i 's/^#!.*$/#!\/usr\/bin\/env sage/' ${HOME}/.sage/local/bin/dissect-*
CMD ["sage", "-n", "jupyter", "dissect/analysis/playground.ipynb", "--ip='0.0.0.0'", "--port=8888"]
