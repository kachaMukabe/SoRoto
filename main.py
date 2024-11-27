import dearpygui.dearpygui as dpg
import cv2
import numpy as np


def convert_cv_to_dpg(image, width, height):
    resized_image = cv2.resize(image, (width, height))

    data = np.flip(resized_image, 2)
    data = data.ravel()
    data = np.asarray(data, dtype="f")

    texture_data = np.true_divide(data, 255.0)

    return texture_data


def click_callback():
    print("Button clicked")


def file_picker_callback(sender, app_data):
    video_path = app_data["file_path_name"]
    print(video_path)
    display_video(video_path)


def display_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with dpg.texture_registry():
        texture_id = dpg.add_dynamic_texture(
            width, height, np.zeros((height, width, 3), dtype=np.float32)
        )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        texture_data = convert_cv_to_dpg(frame, width, height)
        dpg.set_value(texture_id, texture_data)
        dpg.render_dearpygui_frame()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    dpg.delete_item(texture_id)


dpg.create_context()
dpg.create_viewport(title="Dear PyGui Demo")
dpg.setup_dearpygui()


with dpg.file_dialog(
    directory_selector=False,
    show=False,
    callback=file_picker_callback,
    file_count=1,
    id="file_dialog_id",
    width=800,
    height=400,
):
    dpg.add_file_extension(".mp4")
    dpg.add_file_extension(".avi")
    dpg.add_file_extension(".mov")

with dpg.window(label="Tutorial"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Press me", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(label="Text")
    dpg.add_slider_float(label="Slider")


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
