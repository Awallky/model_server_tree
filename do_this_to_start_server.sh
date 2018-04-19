# Use this to create a new frozen model model 
wget https://www.dropbox.com/s/lmp1dqi0d45w6ji/output_inference_graph.pb
mv output_inference_graph.pb test_ckpt/
#gsutil cp gs://cards_data/train/model.ckpt-$1.* .
#python object_detection/export_inference_graph.py \
#    --input_type image_tensor \
#    --pipeline_config_path object_detection/samples/configs/faster_rcnn_resnet101_cards.config \
#    --checkpoint_path model.ckpt-$1 \
#    --inference_graph_path test_ckpt/output_inference_graph.pb

#################################################################
# Export the server                       
#################################################################
export PYTHONPATH=$PYTHONPATH:`pwd`/models:`pwd`/models/slim

#gsutil cp gs://bicycle_only/train/model.ckpt-$1.* .
#python ./models/object_detection/export_inference_graph.py \
#    --input_type image_tensor \
#    --pipeline_config_path models/object_detection/samples/configs/faster_rcnn_resnet101_cards.config \
#    --checkpoint_path model.ckpt-$1 \
#    --inference_graph_path ./test_ckpt/output_inference_graph.pb

sh install_libs_and_run_server.sh
