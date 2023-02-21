# code based on: https://github.com/xugaoxiang/yolov5-streamlit
# Adapted to use with Yolov8

import os, time
import streamlit as st
from ultralytics import YOLO
from ultralytics.yolo.utils import set_settings
from PIL import Image
from inference_param import param_uld, param_locks
from vars import task_types, hide_streamlit_style, page_title,stream_lit_app_title, blink_css
from utils import check_folders, count_locks_detected, remove_background, get_stage2_dir

# This will check if we have all the folders to save our files for inference
check_folders()

# This will set the runs directory where yolo stage 1 exports the file to.
# This step is requried because yolo sometime uses the wrong path based on previous installations.
set_settings(kwargs={'runs_dir':os.path.join(os.getcwd(),'runs')})

if __name__ == '__main__':

    #set HTML title
    st.set_page_config(
        page_title=page_title,
    )    
    
    ######### START SIDEBAR #########
    # Select object detection or instance segmentation
    task = st.sidebar.radio(label="Detection mode",
                                options=[task_type['task'] for task_type in task_types],
                                format_func=lambda z: [x['label'] for x in task_types if x['task']==z][0])
    
    #show slider only for instance segmentation
    if task=="segment":
        scale=st.sidebar.slider("Segmentation mask enlarge scale",min_value=1.0,max_value=1.3,step=0.01,value=1.2)
    
    #show slider to set confidence levels
    stage_1_conf=st.sidebar.slider("Stage 1 min confidence threshold",min_value=0.01,
                                   max_value=0.99,step=0.01,value=param_uld['min_confidence_treshold'])
    stage_2_conf=st.sidebar.slider("Stage 2 min confidence threshold",min_value=0.01,
                                   max_value=0.99,step=0.01,value=param_locks['min_confidence_treshold'])

    #image upload
    uploaded_file = st.sidebar.file_uploader(
        "Load File", type=['png', 'jpeg', 'jpg'],label_visibility="collapsed")
    if uploaded_file is not None:
        is_valid = True
        with st.spinner(text='Loading...'):
            picture = Image.open(uploaded_file).save(f'data/images/{uploaded_file.name}')
            source = f'data/images/{uploaded_file.name}'
    else:
        is_valid = False
    
    ######### END SIDEBAR #########
    
    # to reduce top whitespace in streamlit
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        
    #title
    st.title(stream_lit_app_title)

    if is_valid:
        start_time0=time.time()
        with st.spinner('Wait for it...'):
            #set params
            detect=True if task=="detect" else False
            stage2_dir=get_stage2_dir(detect)

            #Step 1: find ULD:
            #load model
            model_uld=YOLO(os.path.join('models',f'uld_{param_uld["task"]}.pt'))
            #start timer
            start_time1=time.time()            
            #make inference
            model_uld.predict(task=task,
                source=source,
                save_crop=param_uld['save_crop_images'],
                conf=stage_1_conf,
                save=param_uld['save_original_with_bounding_box'],
                save_txt=param_uld['save_bounding_box_data'])
            #end timer
            end_time1=time.time()
            #write inference time
            st.sidebar.write(f"ULD detection runtime: {(end_time1-start_time1)*1000:.1f} ms")

            #run backgroudn removal, only for instance segmentation
            if not detect:
                try:
                    detected_label_files=os.listdir(os.path.join("runs","segment","predict","labels"))
                    start_time_r=time.time()
                    remove_background(img_path=source,
                                    label_file_path=os.path.join("runs","segment","predict","labels",detected_label_files[0]),
                                    bg="white",scale=scale)
                    end_time_r=time.time()
                    st.sidebar.write(f"Background removal runtime: {(end_time_r-start_time_r)*1000:.1f} ms")
                except:
                    st.write("No ULD detected. Try lowering the stage 1 confidence.")
                    is_valid=False

            #detect number of ULD    
            if detect:
                try:
                    detected_ULD=os.listdir(os.path.join("runs","detect","predict","crops","ULD"))
                except:
                    st.write("No ULD detected. Try lowering the stage 1 confidence.")
                    is_valid=False
                    
            else:
                if is_valid:
                    detected_ULD=os.listdir(os.path.join("crops"))
            
            
            #Step 2 Locks:
            if is_valid:
                #load model
                model_locks=model_uld=YOLO(os.path.join('models','locks.pt'))
                
                #for each ULD image detected
                for uld_img_idx in range(len(detected_ULD)):
                    #pick the source based on folder path (detect of segment)
                    if detect:
                        source = os.path.join("runs","detect","predict","crops","ULD",detected_ULD[uld_img_idx])
                    else:
                        source = os.path.join("crops",detected_ULD[uld_img_idx])
                    #start inference timer
                    start_time2=time.time()
                    #make inference
                    model_locks.predict(task=param_locks['task'],
                        source=source,
                        save_crop=param_locks['save_crop_images'],
                        conf=stage_2_conf,
                        save=param_locks['save_original_with_bounding_box'],
                        save_txt=param_locks['save_bounding_box_data'])
                    #end eimter
                    end_time2=time.time()
                    #write inference time
                    st.sidebar.write(f"Locks detection time for ULD #{uld_img_idx+1}: {(end_time2-start_time2)*1000:.1f} ms")
                #write number of ULD found to screen.
                st.sidebar.write(f"Detected {len(detected_ULD)} ULD{'s' if len(detected_ULD)>=2 else ''}.")
                    
                #find path of each image of ULD with bounding box generated by yolo.
                uld_with_locks_bb=os.listdir(os.path.join("runs","detect",stage2_dir))
                #remove 'labels' directory from list detected by listdir
                uld_with_locks_bb.remove("labels")
                
                #iterate through each image found
                for i in range(len(uld_with_locks_bb)):
                    uld_with_lock_fn = uld_with_locks_bb[i]
                    #get filename without extension
                    fn=uld_with_lock_fn.split('.')[0]
                    #count number of locks based on number of lines in labels.txt
                    locks_detected=count_locks_detected(os.path.join("runs","detect",stage2_dir,"labels",
                                                                    f"{fn}.txt"))
                    #if less than 2 lock detected, write warning
                    if(locks_detected<2):
                        #write blinking CSS
                        st.write(blink_css,unsafe_allow_html=True)
                        #write message
                        st.write(f"<div style='color:red;font-size:30px' class='blink'><blink>WARNING. SOME LOCKS MAY BE UNRAISED.</blink></div>",
                                    unsafe_allow_html=True)
                    #write general output
                    st.write(f"ULD #{i+1} &rarr; {locks_detected} lock{'s' if locks_detected>=2 else ''} detected.")

                    #show image to screen
                    if detect:
                        st.image(os.path.join("runs","detect",stage2_dir,uld_with_lock_fn),output_format ="PNG")
                    else:
                        st.image(os.path.join("runs","detect","predict",uld_with_lock_fn),output_format ="PNG")
                    
                    #draw horizontal rule
                    st.write("<hr>",unsafe_allow_html=True)
        end_time0=time.time()
        st.sidebar.write(f"Total runtime: {(end_time0-start_time0)*1000:.1f} ms")