task_types = [{
        'label':"Object detection",
        'task':'detect'
    },{
        'label':"Instance Segmentation",
        'task':'segment'
    }]

hide_streamlit_style = """
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0.5rem;}
    </style>
"""

page_title="ULD Locks Detection"

stream_lit_app_title=':airplane_departure: ULD Locks Detection :airplane_arriving:'

blink_css="""
                    <style>
                        .blink {
                            animation: blink 1s steps(1, end) infinite;
                        }

                        @keyframes blink {
                            0% {
                                opacity: 1;
                            }
                            50% {
                                opacity: 0;
                            }
                            100% {
                                opacity: 1;
                            }
                        }
                    </style>
"""