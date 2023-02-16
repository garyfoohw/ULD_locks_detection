import os, shutil
import pandas as pd
import numpy as np
import cv2

def get_stage2_dir(detect):
    if detect:
        return "predict2"
    else:
        return "predict"

def check_folders():
    #clear 'runs' and 'crops' folder so as to start afresh
    folders_to_remove=['runs','crops']
    for folder in folders_to_remove:
        shutil.rmtree(folder,ignore_errors=True)

    paths = {
        'data_path' : 'data',
        'images_path' : 'data/images',
        # 'videos_path' : 'data/videos',
        'crops':'crops'
        
    }
    # Check whether the specified path exists or not
    notExist = list(({file_type: path for (file_type, path) in paths.items() if not os.path.exists(path)}).values())
    
    if notExist:
        print(f'Folder {notExist} does not exist. We will create it!')
        # Create a new directory because it does not exist
        for folder in notExist:
            os.makedirs(folder)
            print(f"The new directory {folder} is created!")
    
def count_locks_detected(path):
    try:
        with open(path, 'r') as fp:
            return len(fp.readlines())
    except:
        #no raised locks found = no label text file
        return 0

def df_coords_to_list(df):
    """
    returnds a list [[x1,y1],[x2,y2]...] from a df with 'x' and 'y' columns
    """
    list_=[]
    for i in range(df.shape[0]):
        list_.append(
            [df['x'].iloc[i],
            df['y'].iloc[i]]
        )
    return list_

def scale_contour(vertices, scale,img_width,img_height):
    M = cv2.moments(vertices)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    vertices_norm = vertices - [cx, cy]
    vertices_scaled = vertices_norm * scale
    vertices_scaled = vertices_scaled + [cx, cy]
    vertices_scaled = vertices_scaled.astype(np.int32)
    # print(vertices_scaled[:,0])
    # if x<0
    vertices_scaled[:,0]=np.where(vertices_scaled[:,0]<0,0,vertices_scaled[:,0])
    # if x>img_width
    vertices_scaled[:,0]=np.where(vertices_scaled[:,0]>=img_width,img_width-1,vertices_scaled[:,0])
    # if y<0
    vertices_scaled[:,1]=np.where(vertices_scaled[:,1]<0,0,vertices_scaled[:,1])
    # if y>img_width
    vertices_scaled[:,1]=np.where(vertices_scaled[:,1]>=img_height,img_height-1,vertices_scaled[:,1])

    return vertices_scaled

def remove_background(img_path,label_file_path,bg="white",scale=1.2):
    """
    img_path: path to original image
    label_file: path to image file
    bg: background, "white" or "black". Default: white
    scale: factor to scale the contour bigger
    return None

    Function remove background and write to storage    

    Adapted from https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python
    Adapter from https://medium.com/analytics-vidhya/tutorial-how-to-scale-and-rotate-contours-in-opencv-using-python-f48be59c35a2
    """
    # read labels file
    textfile=open(label_file_path,'r')
    lines=textfile.readlines()

    #number of lines = number of uld detected since there is only 1 class
    for line_idx in range(len(lines)):
        #replace \b and split by space
        l=lines[line_idx].replace("\n","").split(" ")
        #remove first element which is the class detected        
        l=l[1:]

        # get number of vertices
        n_vertices=len(l)/2

        #push vertices to a dataframe 
        array=[]
        for x in range(int(n_vertices)):
            d={
                'x':l[2*x],
                'y':l[2*x+1]
            }
            array.append(d)
        df=pd.DataFrame(array)
        df=df.astype(float)

        # read in original iamge
        img=cv2.imread(img_path)

        # get image dimensions
        img_width=img.shape[1]
        img_height=img.shape[0]

        #convert normalized coordiantes to pixel position
        df['x']=round(df['x']*img_width)
        df['y']=round(df['y']*img_height)
        df=df.astype(int)

        #covnert df to a list [[x1,y1],[x2,y2]...] to feed into cv2 later, convert to numpy array
        vertices=df_coords_to_list(df)
        vertices=np.array(vertices)
        vertices=scale_contour(vertices,scale,img_width,img_height)
        # find the outer rectangular cropping box, find the x,y,w,h and crop the image.
        rect=cv2.boundingRect(vertices)
        x,y,w,h=rect
        cropped=img[y:y+h,x:x+w].copy()
        #adjust the vertices, after cropping
        vertices=vertices-vertices.min(axis=0)

        #create a matrix of zeroes, following the shape of the cropped image.
        mask=np.zeros(cropped.shape[:2],np.uint8)
        
        #make the layer a mask of the vertices
        a=cv2.drawContours(image=mask,contours=[vertices],contourIdx=-1,
                 color=(255,255,255), thickness=-1, lineType=cv2.LINE_AA)
        
        #produce instance with black bg
        cropped_black=cv2.bitwise_and(cropped,cropped,mask=mask)

        if bg=="black":
            output=cropped_black
        elif bg=="white":
            #produce instance with white bg
            background=np.ones_like(cropped,np.uint8)*255
            cropped_white=background+cropped_black
            output=cropped_white
        else:
            print("Error: 'bg' must be 'black' or 'white'")

        #export
        output_path=os.path.join("crops",f"{line_idx}.png")
        
        if not cv2.imwrite(output_path,output):
            raise Exception("Could not write image") 
        