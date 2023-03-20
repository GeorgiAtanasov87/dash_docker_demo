FROM continuumio/miniconda3 as miniconda

RUN mkdir -p /opt/notebooks

WORKDIR /opt/notebooks

# Install all required libraires using conda
RUN conda install nodejs jupyterlab ipywidgets plotly \
  pandas requests pendulum pyyaml sqlalchemy -y --quiet
  
# Update the old libraries in conda repo using pip
RUN pip install sqlalchemy ipywidgets plotly --upgrade

EXPOSE 8888

# ENTRYPOINT ["/bin/bash"]
CMD jupyter lab --ip=* --port=8888 --no-browser --allow-root