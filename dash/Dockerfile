FROM continuumio/miniconda3 as dash

RUN mkdir -p /opt/dash

WORKDIR /opt/dash
COPY ./environment ./environment
# Install all required libraires using conda
RUN conda env create -f ./environment/conda.yaml 

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "dash-env", "/bin/bash", "-c"]

# Update the old libraries in conda repo using pip
RUN pip install -r ./environment/requirements.txt --upgrade

COPY ./* .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "dash-env", "python", "main.py"]

EXPOSE 8050
