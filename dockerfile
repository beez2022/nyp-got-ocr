FROM nyp-got-ocr-cpu:latest

RUN pip install jupyterlab


ENTRYPOINT ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser",  "--allow-root", "--NotebookApp.token=''" , "--NotebookApp.password=''"]