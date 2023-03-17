FROM continuumio/miniconda3 as miniconda

RUN mkdir -p /opt/notebooks

WORKDIR /opt/notebooks

RUN conda install nodejs jupyterlab -y --quiet && \
    conda install plotly jupyterlab_widgets && \
    conda install pandas requests pendulum ipywidgets pyyaml

EXPOSE 8888

# ENTRYPOINT ["/bin/bash"]
CMD jupyter lab --ip=* --port=8888 --no-browser --allow-root