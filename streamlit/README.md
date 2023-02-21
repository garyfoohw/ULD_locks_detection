<div align="center">
  <h1>ULD Locks Detection</h1>
</div>

## Deploying the Streamlit app.

There are 2 ways to deploy the app.

-   Locally on your machine
-   On Google Colab (with access via Internet)

## Dependencies

-   Python (<=3.10.x at time of writing)
-   Streamlit
-   Ultralytics YOLOv8 (<=8.0.29 at time of writing)
-   Pillow (PIL)
-   Numpy
-   OpenCV

## Getting started

### Getting started on your local machine

To get started, you need to clone the repository and install the dependencies.

```
# clone the repository
git clone https://github.com/garyfoohw/ULD_locks_detection
```

```
# install python virtual environment
python -m venv venv
#activate virtual env (in windows):
source\Scripts\activate
```

```
# install the dependencies
pip install -r requirements.txt
```

## Running the App

After installation, run the following command to start the app:

```
streamlit run main.py
```

This will open a browser window where you can upload an image. The app will then perform object detection on the uploaded file and display the results.

### Getting started via Google Colab

To get started, you need to open the `streamlit_on_colab.ipynb` file on Google Colab and run it..
The file can be found at [https://github.com/garyfoohw/ULD_locks_detection/blob/master/streamlit/streamlit_on_colab.ipynb](https://github.com/garyfoohw/ULD_locks_detection/blob/master/streamlit/streamlit_on_colab.ipynb).

Within the notebook, you will find instruction needed to set up the Github SSH key. Pls follow instruction within the file.

## Customizing the App

You can customize the parameters of the object detection process by modifying the inference_param.py file. This file contains the parameters for the detection process.

## Limitations

This project is designed for the detection of raised locks with ULD and may not work well for detecting other objects. Also, the performance of the app may vary depending on the quality and resolution of the input image. Speed of device may also affect the usability due to inference time.

## Technical details of program flow

```
          Object      ┌────────────────────────┐
          Detection   │ Stage 1 (Detect ULD)   ├─────────────────────────┐
          ┌──────────►│ YOLOv8                 │                         ▼
          │           │ Obj Detection          │                       ┌────────────────┐
          │           └────────────────────────┘                       │  Stage 2       │  ┌───────────────┐
┌─────────┴─┐                                                          │  YOLOv8        ├─►│ Output Image  │
│ Raw Image │                                                          │  Obj Detection │  └───────────────┘
└─────────┬─┘                                                          └────────────────┘
          │           ┌────────────────────────┐     ┌────────────┐      ▲
          │           │ Stage 1 (Detect ULD)   │     │ Background │      │
          └──────────►│ YOLOv8                 ├────►│ Removal    ├──────┘
          Instance    │ Instance Segmentation  │     │            │
          Segmentation└────────────────────────┘     └────────────┘
```

## Adapted from

https://github.com/josebenitezg/yolov8-streamlit-app
