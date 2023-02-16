param_uld={
    'task' : "segment", #will be overwritten by script on load
    'min_confidence_treshold':0.9,
    'save_crop_images':True, #needs to be True when using detect
    'save_original_with_bounding_box':True,
    'save_bounding_box_data':True, #needs to be True when using segment
}

param_locks={
    'task' : "detect",
    'min_confidence_treshold':0.25,
    'save_crop_images':False,
    'save_original_with_bounding_box':True,
    'save_bounding_box_data':True,
}

