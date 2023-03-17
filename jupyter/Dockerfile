FROM continuumio/miniconda3 as miniconda

RUN mkdir -p /opt/notebooks

WORKDIR /opt/notebooks

RUN conda install nodejs -y --quiet
RUN conda install jupyterlab -y --quiet
RUN conda install -n base jupyterlab_widgets
RUN conda install -n base ipywidgets -y --quiet
RUN conda install plotly -y --quiet
RUN conda install pandas requests pendulum pyyaml -y --quiet
RUN pip install sqlalchemy
RUN pip install ipywidgets plotly --upgrade


EXPOSE 8888

# ENTRYPOINT ["/bin/bash"]
CMD jupyter lab --ip=* --port=8888 --no-browser --allow-root