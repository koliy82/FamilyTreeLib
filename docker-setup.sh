apt-get update && apt-get upgrade
apt-get install --no-install-recommends -y
pip install --upgrade pip
pip install poetry
apt-get autoremove -y
#apt-get install --no-install-recommends -y build-essential
#poetry config virtualenvs.create false
poetry install --only main,test
pip install uvicorn
pip install fastapi
#apt-get purge build-essential -y
#apt-get autoremove -y
#COPY --chown=app:app . ./
cd api
python -m app.main
#apt-get install libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 -y
#apt-get install libgl1-mesa-glx libglib2.0-0 libxcb-icccm4 libxcb-icccm4-dev libqt5pdf5 graphviz graphviz-dev -y
#apt-get install build-essential -y
#gcc --version

#apt-get install libtiff5-dev -y
#ln -s /usr/lib/x86_64-linux-gnu/libtiff.so.6.0.0 /usr/lib/x86_64-linux-gnu/libtiff.so.5
#ln -s /usr/lib/x86_64-linux-gnu/libtiff.so.6.0.0 /usr/local/lib/python3.10/site-packages/PyQt5/Qt5/plugins/imageformats/libtiff.so.5
#ln -s /usr/lib/x86_64-linux-gnu/libtiff.so.6.0.0 /usr/local/lib/python3.10/site-packages/PyQt5/Qt5/plugins/imageformats/libtiff.so

#pip install --upgrade pip
#
#pip install networkx[default,extra] pygraphviz pydot lxml
#python -m app.main