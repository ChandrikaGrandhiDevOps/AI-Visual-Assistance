from google import genai
from google.genai import types
from PIL import Image
import pyautogui
import pygetwindow as gw
import win32gui
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Initialize the GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def capture_screen():
    pyautogui.hotkey("alt", "tab")
    hwnd = win32gui.GetForegroundWindow()  # Get handle of the active window
    target_window_title = win32gui.GetWindowText(hwnd)  # Get window title

    # Get the target window object
    window = gw.getWindowsWithTitle(target_window_title)

    if window:
        window = window[0]

        # Get window position and size
        x, y, width, height = window.left, window.top, window.width, window.height

        # Take a screenshot
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Save the screenshot
        screenshot.save("picture.png")
        print("Screenshot saved")


def load_and_resize_image(image_path):
    with Image.open(image_path) as img:
        aspect_ratio = img.height / img.width
        new_height = int(img.width * aspect_ratio)
        return img.resize((img.width, new_height), Image.Resampling.LANCZOS)


def get_genai_response(prompt, image):
    image = "picture.png"
    screen = load_and_resize_image(image)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, screen],
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant with expertise in image analysis.",
        ),
    )
    return response.text


def main():
    html_temp = """
    <div style="background-color:rgb(100, 100, 255);padding:8px">
    <h2 style="color:white;text-align:center;">AI Visual Assistant Multimodal Application with Python & Gemini 2.0 Flash Model</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.image("logo.jpg", width=300)

    st.markdown("""

        <style>
            .stFileUploader label {
                font-size: 10px; /* Adjust font size as needed */
            }

        </style>

    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color: purple; font-size: 18px; font-weight: bold;'>Upload Image</p>",
        unsafe_allow_html=True
    )

    img_file = st.file_uploader("", type=["jpg", "png"])
    #    img_file = st.file_uploader("**Upload Image**", type=["jpg", "png"])

    if ((img_file is not None) and (('jpg' in str(img_file)) or ('png' in str(img_file)))):
        st.image(load_and_resize_image(img_file))
        img = load_and_resize_image(img_file)
        img.save("picture.png")

    st.markdown("""

        <style>
            .stFileUploader label {
                font-size: 30px; /* Adjust font size as needed */
            }

        </style>

    """, unsafe_allow_html=True)

    st.text("Or")

    if st.button("Capture Screenshot Image"):
        capture_screen()
        st.image(load_and_resize_image("picture.png"))

    query = st.text_input("**Query**", "")

    st.markdown("""

        <style>
            .stFileUploader label {
                font-size: 30px; /* Adjust font size as needed */
            }

        </style>

    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #DD3300;
        color:#eeffee;
    }
    </style>""", unsafe_allow_html=True)

    if st.button("Analyze Image"):
        st.image(load_and_resize_image("picture.png"))
        prompt = query
        results = get_genai_response(prompt, img_file)
        st.success('Results: {}'.format(results))


if __name__ == "__main__":
    main()

