FROM sagemath/sagemath-dev:9.0
RUN sage -i database_kohel
RUN sage --pip3 install --no-cache-dir notebook==5.*
COPY . ${HOME}/dissect
USER root
RUN chown -R 1000 ${HOME}
USER sage
WORKDIR /home/sage/dissect
RUN sage --pip3 install --upgrade -r requirements.txt
RUN sage --pip3 install --editable .
ENTRYPOINT ["sage", "--python3", "-m"]
