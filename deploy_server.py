#####import various libraries needed (put this and global defs in separate file to import later?)#####
import sys 
import os
import flask
from werkzeug import secure_filename
from io import StringIO
from flask import render_template, send_from_directory, request, redirect, url_for
from flask import jsonify
import base64
import tensorflow as tf
import numpy as np
import flask
from collections import defaultdict
from matplotlib import pyplot as plt
from PIL import Image
sys.path.append("..")
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from threading import Thread
from time import sleep
####################################################################################

################################global defs#########################################
PATH_TO_CKPT = os.path.join('test_ckpt', 'output_inference_graph.pb')
PATH_TO_LABELS = os.path.join('data', 'card_label_map.pbtxt')
NUM_CLASSES = 24
UPLOAD_FOLDER='static/images'
IMAGE_SIZE = (12, 8)
sys.path.append("..")
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
####################################################################################

app = flask.Flask(__name__)
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

detection_graph = tf.Graph()
def load_graph(trained_model):
    #anything in following scope with be added to or run operation from detection_graph
    with detection_graph.as_default() as graph:
    #graph object holds a network of nodes, each repr. one operation, connected to each other as
    #inputs and outputs
    #need to actually load the model in od_graph_def using tf.GraphDef
    #create empty GraphDef object that were going to populate with data from our file
        od_graph_def = tf.GraphDef()
        #google cloud storage exports as tf.gfile so you can use for saving and loading ckpts
        #open output inf. graph for reading in binary mode
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            #serialized_graph contains binary version of graph
            serialized_graph = fid.read()
            #read data back to python
            od_graph_def.ParseFromString(serialized_graph)
            #import graph from od_graph_def into the current default Graph
            tf.import_graph_def(od_graph_def, name='')
    return graph

"""
# Looks for files with 'ext' extensions in the input directory
# and removes all files containing the matching extension
# Returns the number of files removed from the directory
"""
def clear_images_dir(dir_name, ext):
    files_removed = 0
    for file in os.listdir(dir_name):
        if(file.endswith(ext)):
            try:
                #print("Freeing up disk space", file)
                os.remove(os.path.join(dir_name,file))
                files_removed += 1
            except:
                print("Failed to remove", file)
    return files_removed

@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('mainpg.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@app.route('/result',methods = ['POST'])
def result():
   if request.method == 'POST':
       print("Uploading file to server...")
       clear_images_dir(UPLOAD_FOLDER, '.jpg')
       upload_file = request.files['file']
       filename = secure_filename(upload_file.filename)
       upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
       image_path = os.path.join(UPLOAD_FOLDER, filename)
       image_size=128
       num_channels=3
       with detection_graph.as_default():
           print("With graph as default...")
           with tf.Session(graph=detection_graph) as sess:
               image = Image.open(image_path)
               # the array based representation of the image will be used later in order to prepare the
               # result image with boxes and labels on it.
               print("Loading image to numpy array...")
               image_np = load_image_into_numpy_array(image)
               #Expand dimensions since the model expects images to have shape: [1, None, None, 3]
               #make the np image 4d now
               image_np_expanded = np.expand_dims(image_np, axis=0)
               print("Getting relevant tensors from graph...")
               image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
               # Each box represents a part of the image where a particular object was detected.
               boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
               # Each score represent how level of confidence for each of the objects.
               # Score is shown on the result image, together with the class label.
               scores = detection_graph.get_tensor_by_name('detection_scores:0')
               classes = detection_graph.get_tensor_by_name('detection_classes:0')
               num_detections = detection_graph.get_tensor_by_name('num_detections:0')
               # Actual detection.
               print("Running detection...")
               (boxes, scores, classes, num_detections) = sess.run(
                   [boxes, scores, classes, num_detections],
                   feed_dict={image_tensor: image_np_expanded})
               print("Getting card list and drawing boxes...")
               #edited vis_util func to return list of cards
               card_list = vis_util.get_image_cards(
                   image_np,
                   np.squeeze(boxes),
                   np.squeeze(classes).astype(np.int32),
                   np.squeeze(scores),
                   category_index)
	       #print("Card list",card_list, "scores:", scores, "classes", classes, "num_detections:", num_detections)
               #edited vis_util func to return PIL image
               im_result = vis_util.visualize_boxes_and_labels_on_image_array(
                   image_np,
                   np.squeeze(boxes),
                   np.squeeze(classes).astype(np.int32),
                   np.squeeze(scores),
                   category_index,
                   use_normalized_coordinates=True
                    )
               #for debugging
               print(card_list)
	       #print(request.base_url)
	       #print(category_index)
               #scale image and save to display
               im_result.thumbnail((250,250))
               im_result.save(image_path[:-4] + '.jpg', "JPEG")
	       """
	       try:
			os.remove(os.path.join(UPLOAD_FOLDER,filename))
	       except:
	       		print("Unable to remove file:", os.path.join(UPLOAD_FOLDER,filename))
	       """
               return render_template('userSubmissionResults.html', cards=card_list, card_image = filename[:-4] +".jpg")


###############################run the app############################
print("Loading graph...")
app.graph=load_graph(PATH_TO_CKPT)
print("Starting server...")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("5000"), debug=False, use_reloader=False)

