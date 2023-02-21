<div align="center">
  <h1>ULD Locks Detection</h1>
</div>

## Executive Summary

This code implements a web application that performs object detection and instance segmentation tasks on an uploaded image. The objective is to detect whether an ULD (Unit Load Device) is properly locked. The detection algorithm is based on Ultralytics' YOLOv8 and processed through a 2 stage detection algorithm. The web platform is run on Streamlit.

The user can select the desired detection method for stage 1 and and adjust the confidence threshold levels for both stages. The uploaded image is processed through the two-stage algorithm, first for ULDs and then for locks. The results are displayed in the form of bounding boxes and on-screen messages. A warning message will also be triggered if insufficient locks are detected.

## Technical details

This is a computer vision project that uses the YOLOv8 object detection algorithm to detect ULD and locks in images. The implementation uses the Ultralytics implementation of YOLOv8, which is a lightweight and fast object detection algorithm. Ultralytics is also the creator of YOLOv5. This implementation uses Streamlit for web deployment.

The app uses a 2-stage detection model to achieve the task. Stage 1 uses object detection or instace segmentation which the user can decide. Stage 2 uses object detection to detect locks in raised position or lack thereof.

If stage 1 is set to instance segmentation, a custom algorithm is also invoked to process background removal on the original image using information provided by YOLOv8 in the form of vertices of the segmentation mask. The process of background removal will allow stage 2 to detect better without confusion from nearby objects. A scale factor is also built-in to allow the algorithm to crop less tightly around the object of interest. The scale is essentially an enlargement of the polygon of the object of interest so as to force the algorithm to crop differently.

The use of streamlit platform allows for convenient adjustment of inference confidence of both stages as well as scale factor used when removing background.

The YOLOv8 models used within this package have been pre-trained separately. The training used pre-trained YOLOv8n models.

## Static demonstration

1. Here we demonstrate using Object Detection in Stage 1 to locate the 2 raised locks. The output shows the 2 locks detected in the bounding boxes drawn.

**Raw Image**<br>
![#1 Raw Image](https://user-images.githubusercontent.com/86142858/220334321-8b44ae00-b8cc-4a4a-8b43-a58c18606b2c.jpg)

**Processed Output**<br>
![#1 Processed Output](https://user-images.githubusercontent.com/86142858/220334804-57dda9e1-5087-498d-8b10-3667c69a47d4.png)

1. Next we demonstrate using Instance Segmentation in Stage 1 to locate locks. There isn't any raised locks in this sample, so the algorithm detects none, and output an error in red.

**Raw Image**<br>
![#2 Raw Image](https://user-images.githubusercontent.com/86142858/220335210-1211f3c4-8868-43f7-9cbb-06b41fe9053b.png)

**Processed Output**<br>
![#2 Processed Output](https://user-images.githubusercontent.com/86142858/220335449-ebb2cebc-d81c-438d-bc37-20062aa9f6a4.png)

## Getting started

The repository is split into 2 folders. 1 for the training algorithm 1 for the deployment.

-   To look at the training algorithm, refer to **train** folder.
-   To look at web deployment, refer to **streamlit** folder

Please refer to the README within `train` or `streamlit` folder for more details on training or web deployment.
