import streamlit as st
import numpy as np
import base64
import pickle
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx as get_report_ctx

#Load developed Machine Learning Model for Contact area
model = pickle.load(open('gb_model.pkl','rb'))

#Load developed Machine Learning Model for Tyre deflection
model1 = pickle.load(open('gb_model1.pkl','rb'))
#loaded_model_CA = keras.models.load_model('gb.h5')
scaler_X_model = pickle.load(open('X_scaler.pkl','rb'))
#scaler_Y_model = pickle.load(open('Scaler_Y (2).pkl','rb'))


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def add_logos(logo1, logo2):
    with open(logo1, "rb") as file:
        encoded_logo1 = base64.b64encode(file.read()).decode()
    with open(logo2, "rb") as file:
        encoded_logo2 = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <div class='header' style='display: flex; justify-content: space-between;'>
            <img src="data:image/png;base64,{encoded_logo1}" style='height: 60px; width: auto;'>
            <img src="data:image/png;base64,{encoded_logo2}" style='height: 60px; width: auto;'>
        </div>
        """,
        unsafe_allow_html=True
    )

# Usage
add_bg_from_local('img_3.png')
add_logos("IIT-Kharagpur.png", "tractlogo.png")

def add_photos_and_names(photos, names, designation, positions):
    for photo, name, designation, position in zip(photos, names, designation, positions):
        with open(photo, "rb") as file:
            encoded_photo = base64.b64encode(file.read()).decode()
        st.markdown(
            f"""
            <div style='position: fixed; {position}'>
                <img src="data:image/png;base64,{encoded_photo}" style='height: 100px; width: 100px;'>
                <h2 style='color: #FF0000;font-size:24px;text-align: left;'>{name}</h2>
                <h3 style='color: black;font-size:14px;text-align: left;'>{designation}</h3>
                
            </div>
            """,
            unsafe_allow_html=True
        )
add_photos_and_names(
    ["img_5.png", "img_6.png",  ],
    ["Rajesh Yadav", "Prof. H Raheman", ], ["(RS, IIT Kharagpur)", "(Professor, IIT Kharagpur)",],

    ["bottom: 80px; left: 27%;", "bottom: 80px; right: 0%;", ]
)
st.markdown('''<p style='text-align: center; font-size: 12px; bottom: 1 px;'>Developed by Rajesh Yadav</p>''', unsafe_allow_html=True)



st.markdown(""" <h1 style= "font-weight: bold; text-align: center; color: black; font-size:36px;"> Tyre Contact Characteristics</h1>""", unsafe_allow_html=True)
st.sidebar.markdown(f'<h1 style="font-weight: bold; color:green;font-size:40px;">{"Enter the following Inputs"}</h1>', unsafe_allow_html=True)
tyre= st.sidebar.selectbox('Tyre type: ',('<select>','Tubeless', 'Tube-type'))
if tyre == 'Tubeless':
    tt = 1
elif tyre == 'Tube-type':
    tt = 0

inflation_pressure = st.sidebar.number_input('Enter the inflation pressure of the tyre (kPa)',0.0)
inflation_pressure_psi = inflation_pressure*0.14
normal_load = st.sidebar.number_input('Enter the normal load on the tyre, kg',0.0 )

st.markdown(f'<h1 style="color:#00008B;font-size:32px;">{"Specified inputs"}</h1>', unsafe_allow_html=True)

col1,col2 = st.columns(2)
with col1:
    st.markdown('<p style="text-align: center;background-color:#FEE715FF;color:#101820FF;'
            'font-size:24px;border-radius:2%;">Type of tyre</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;background-color:#FEE715FF;color:#101820FF;'
            'font-size:24px;border-radius:2%;">Inflation pressure of tyre</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;background-color:#FEE715FF;color:#101820FF;'
                'font-size:24px;border-radius:2%;">Normal load on tyre</p>', unsafe_allow_html=True)


with col2:
    st.markdown(f'<p style="text-align: center;background-color:#FFFACD;color:#000000;'
                f'font-size:24px;border-radius:2%;">{tyre} </p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center;background-color:#FFFACD;color:#000000;'
                f'font-size:24px;border-radius:2%;">{inflation_pressure} kPa</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center;background-color:#FFFACD;color:#101820FF;'
                f'font-size:24px;border-radius:2%;">{normal_load} kg</p>', unsafe_allow_html=True)

st.write('')

if st.button('Evaluate'):
    st.markdown(f'<h1 style="text-align: center;color:#00008B;'
                f'font-size:36px;">{" Predicted Contact Characteristics"}</h1>', unsafe_allow_html=True)

    querry = [tt, normal_load, inflation_pressure_psi]

    querry = np.array([[querry]])
    querry = querry.reshape(1, 3)

    #Contact Area

    predicted_CA= model.predict(querry)[0]
    arr = np.array(predicted_CA *1000000)
    arr_2d = arr.reshape(-1, 1)

    #Tyre deflection
    predicted_def = model1.predict(querry)[0]
    arr1 = np.array(predicted_def)
    arr_2d1 = arr1.reshape(-1, 1)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="text-align: center; background-color:#d077ec; color:black; font-size: 24px;font-weight: bold;'
                    'border-radius: 2%;">Contact Area</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; background-color:#d077ec; color:black; font-size: 24px;font-weight: bold;'
                    'border-radius: 2%;">Tyre Deflection</p>', unsafe_allow_html=True)


    with col2:
        #st.markdown(f'<p style="text-align: center;background-color:#FBEAEB; color:#101820FF; font - size: 18px;'
        #            f'border - radius: 2 %;">{np.round(arr_2d[0][0] / 1, 2)} Square millimeter</p>',
         #           unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center;background-color:#6bf8a1; color:#101820FF; font-size: 24px;font-weight: bold;'
                    f'border-radius: 2%;">{np.round(arr_2d[0][0] / 1, 2)} Square millimeter</p>',
                    unsafe_allow_html=True)
        #st.markdown(f'<p style="text-align: center;background-color:#FBEAEB;color:#101820FF;'
        #            f'font - size: 18px; border - radius: 2 %; ">{np.round(arr_2d1[0][0]/1,2)} mm</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center;background-color:#6bf8a1;color:#101820FF;'
                    f'font-size: 24px;font-weight: bold;border-radius: 5%;">{np.round(arr_2d1[0][0]/1,2)} mm</p>',
                    unsafe_allow_html=True)