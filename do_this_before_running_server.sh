cd ./models
# Tensorflow and dependency installation
# pick one of the two tensorflow install options depending on if you have a gpu or not
pip install tensorflow
#pip install tensorflow-gpu
sudo apt-get install protobuf-compiler python-pil python-lxml python-tk
sudo pip install Cython
sudo pip install jupyter
sudo pip install matplotlib
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
# a test to see if the tensorflow installation went correctly
#python object_detection/builders/model_builder_test.py 

# Now to run the server
cd ..
sudo pip install flask
python deploy_server.py
