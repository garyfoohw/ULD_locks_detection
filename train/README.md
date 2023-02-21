<div align="center">
  <h1>ULD Locks Detection</h1>
</div>

## First things

There is only one way to operate this notebook - via Google Colab.
The notebook is designed to mount to Google Drive to upload trained model files when training is complete.

You will also need a Roboflow account and your account's API KEY.

## Dependencies

-   Python (<=3.10.x at time of writing)
-   Ultralytics YOLOv8 (<=8.0.29 at time of writing)
-   Roboflow

## File naming convention

You will find the files are named as `xxx_yyy_zzz_train` or `xxx_yyy_zzz_infer`.

`xxx` refers to the object which the algorithm is trying to detect. Either a ULD or a Lock.
`yyy_zzz` refers to the detection task given to YOLOv8. Either Object Detection or Instance Segmentation.

## Getting started

### Training to detect the ULD / Lock

Select a file that says `xxx_yyy_zzz_train` and open it in Google Colab
Alter the `API_KEY` that corresnponds to your Roboflow account so as to access the dataset later.
Remmber to assign a GPU to the Colab Environment, and run.

The training process may take around 1 hour for 100 epochs (on Nvidia T4 GPU).

When the training is done, the following items will be stored to **Google Drive/ULD/**.

-   Best model (.pt Pytorch format)
-   Training history (Losses, mAP, Precision, Recall etc)

### Infering the ULD / Lock

Select a file that says `xxx_yyy_zzz_infer` and open it in Google Colab

-   Alter the `modelfile` that corresnponds to the trained model (.pt format) that you wish to use. The model should be placed in **Google Drive/ULD/**.
-   Set `source_zip` to the filename of the zipped file which contains all the images to be used for inferrence. The string must end with **.zip**. Place the zip file in **Google Drive/ULD/**
    You can also change some other parameters in the first cell.
    Remmber to assign a GPU to the Colab Environment, and run.

When the inference is done, the following item will be stored to **Google Drive/ULD/**.

-   Zip file of inference output (Crops/Original image with Bounding boxes/Labels)
