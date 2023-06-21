import traceback
import modules.sd_samplers
import modules.scripts as scripts
import gradio as gr
import numpy as np
from PIL import Image
import base64
import json
import os
import platform
import subprocess as sp


BASEDIR = scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path
CONFIG_TXT2IMG_FILE_NAME = "config-txt2img.json"
CONFIG_IMG2IMG_FILE_NAME = "config-img2img.json"

#fields_checkboxgroup = None


class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.txt2img_config_preset_dropdown = None
        self.img2img_image_ids = [
            "img2img_image",
            "img2img_sketch",
            "img2maskimg"
            "inpaint_sketch",
            "img_inpaint_base",
            "img_inpaint_mask"
        ]

        # These are the settings from the UI that are saved for each preset
        self.txt2img_component_ids = [   # mirrors the config_preset_dropdown.change(output) events and config_preset_dropdown_change()
            # "txt2img_prompt",
            # "txt2img_neg_prompt",
            # "txt2img_sampling",
            # "txt2img_steps",
            # "txt2img_width",
            # "txt2img_height",
            # "txt2img_batch_count",
            # "txt2img_batch_size",
            # "txt2img_restore_faces",
            # "txt2img_enable_hr",
            # "txt2img_hr_scale",
            # "txt2img_hr_upscaler",
            # "txt2img_hires_steps",
            # "txt2img_denoising_strength",
            # "txt2img_cfg_scale",
            # "txt2img_gallery",
            # "ext_ctl_enabled",
            # "ext_ctl_scribble_mode",
            # "ext_ctl_rgbbgr_mode",
            # "ext_ctl_lowvram",
            # "ext_ctl_guess_mode",
            # "ext_ctl_module",
            # "ext_ctl_model",
            # "ext_ctl_weight",
            # "ext_ctl_guidance_start",
            # "ext_ctl_guidance_end",
            # "ext_ctl_processor_res",
            # "ext_ctl_threshold_a",
            # "ext_ctl_threshold_b",
            # "ext_ctl_resize_mode",
            # "ext_ctl_canvas_width",
            # "ext_ctl_canvas_height",
           # "component-1285",
        ]
        self.img2img_component_ids = [   # mirrors the config_preset_dropdown.change(output) events and config_preset_dropdown_change()
            "resize_mode"
            # "img2img_prompt",
            # "img2img_neg_prompt",
            # "img2img_sampling",
            # "resize_mode",
            # "img2img_steps",
            # "img2img_width",
            # "img2img_height",
            # "img2img_batch_count",
            # "img2img_batch_size",
            # "img2img_cfg_scale",
            # "img2img_denoising_strength",
            # "img2img_restore_faces",
            # "ext_ctl_enabled",
            # "ext_ctl_scribble_mode",
            # "ext_ctl_rgbbgr_mode",
            # "ext_ctl_lowvram",
            # "ext_ctl_guess_mode",
            # "ext_ctl_module",
            # "ext_ctl_model",
            # "ext_ctl_weight",
            # "ext_ctl_guidance_start",
            # "ext_ctl_guidance_end",
            # "ext_ctl_processor_res",
            # "ext_ctl_threshold_a",
            # "ext_ctl_threshold_b",
            # "ext_ctl_resize_mode",
            # "ext_ctl_canvas_width",
            # "ext_ctl_canvas_height",
            # "ext_ctl_image",
        ]


        # Mapping between component labels and the actual components in ui.py
        self.txt2img_component_map = {k: None for k in self.txt2img_component_ids}  # gets filled up in the after_component() method
        self.img2img_component_map = {k: None for k in self.img2img_component_ids}  # gets filled up in the after_component() method

        # Load txt2img and img2img config files
        try:
            with open(f"{BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}") as file:
                self.txt2img_config_presets = json.load(file)

            # #print("self.config_presets loaded:")
            # for preset_name, values_dict in self.txt2img_config_presets.items():
            #     #print(preset_name,values_dict)
            #     if "steps" in values_dict.keys():
            #         print("[ERROR][Config-Presets] Your config.json file is using an outdated format, so the Config Presets dropdown will not work. You need to delete /extensions/Config-Presets/config.json so it can be recreated with the new updated format.")
            #         break


        except FileNotFoundError:
            # txt2img config file not found
            # First time running the extension or it was deleted, so fill it with default values
            self.txt2img_config_presets = {}

            write_config_presets_to_file(self.txt2img_config_presets, CONFIG_TXT2IMG_FILE_NAME)
            print(f"[Config Presets] txt2img config file not found, created default config at {BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}")


        try:
            with open(f"{BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}") as file:
                self.img2img_config_presets = json.load(file)

        except FileNotFoundError:
            # img2img config file not found
            # First time running the extension or it was deleted, so fill it with default values
            self.img2img_config_presets = {}

            write_config_presets_to_file(self.img2img_config_presets, CONFIG_IMG2IMG_FILE_NAME)
            print(f"[Config Presets] img2img config file not found, created default config at {BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}")


    def title(self):
        return "Config Presets"

    def show(self, is_img2img):
        #return True
        return scripts.AlwaysVisible    # hide this script in the Scripts dropdown
    # def before_component(self, component, **kwargs):
    #     print(kwargs)
    #     print("111111111111")

    def after_component(self, component, **kwargs):
        # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
        # so we can use the same code for both tabs
        # if not getattr(component, 'elem_id', None):
        #     component.elem_id = component.label
        component_map = None
        component_ids = None
        config_file_name = None
        if self.is_txt2img:
            component_map = self.txt2img_component_map
            component_ids = self.txt2img_component_ids
            config_file_name = CONFIG_TXT2IMG_FILE_NAME
        else:
            component_map = self.img2img_component_map
            component_ids = self.img2img_component_ids
            config_file_name = CONFIG_IMG2IMG_FILE_NAME
        # print(component_map)
        #if component.label in self.component_map:
        if component.elem_id in component_map:
            component_map[component.elem_id] = component
        if component.elem_id is not None and (component.elem_id.startswith("txt2img") or component.elem_id.startswith("img2img") or component.elem_id.startswith("script_")):
            component_map[component.elem_id] = component
            component_ids.append(component.elem_id)
            #print(f"[Config-Presets][DEBUG]: found component: {component.elem_id} {component}")

        #if component.elem_id == "script_list": #bottom of the script dropdown
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        #if component.elem_id == "open_folder": #bottom of the image gallery
        if component.elem_id == "txt2img_generation_info_button" or component.elem_id == "img2img_generation_info_button": #very bottom of the txt2img/img2img image gallery
            #print("Creating dropdown values...")
            #print("key/value pairs in component_map:")
            # before we create the dropdown, we need to check if each component was found successfully to prevent errors from bricking the Web UI
            for component_name, component in component_map.items():
                #print(component_name, component_type)
                if component is None:
                    print(f"[ERROR][Config-Presets] The component '{component_name}' no longer exists in the Web UI. Try updating the Config-Presets extension. This extension will not work until this issue is resolved.")
                    return

            # Mark components with type "index" to be transform
            index_type_components = []
            for component in component_map.values():
                #print(component)
                if getattr(component, "type", "No type attr") == "index":
                    # print(component.elem_id)
                    index_type_components.append(component.elem_id)

            preset_values = []
            config_presets = None
            if self.is_txt2img:
                config_presets = self.txt2img_config_presets
            else:
                config_presets = self.img2img_config_presets

            for dropdownValue in config_presets:
                preset_values.append(dropdownValue)
                print(f"Config Presets: added \"{dropdownValue}\"")

            fields_checkboxgroup = gr.CheckboxGroup(choices=component_ids,
                                                    value=component_ids,    #check all checkboxes by default
                                                    label="Fields to save",
                                                    show_label=True,
                                                    interactive=True,
                                                    elem_id="config_preset_fields_to_save",
                                                    ).unrender() #we need to define this early on so that it can be used as an input for another function

            with gr.Column(min_width=600, elem_id="config_preset_wrapper_txt2img" if self.is_txt2img else "config_preset_wrapper_img2img"):  # pushes our stuff onto a new row at 1080p screen resolution
                with gr.Row():
                    with gr.Column(scale=8, min_width=100) as dropdown_column:


                        def config_preset_dropdown_change(dropdown_value, *components_value):
                            config_preset = config_presets[dropdown_value]
                            print(f"[Config-Presets] Changed to: {dropdown_value}")

                            # update component values with user preset
                            current_components = dict(zip(component_map.keys(),components_value))
                            #print("Components before:", current_components)
                            current_components.update(config_preset)

                            # transform necessary components from index to value
                            for component_name, component_value in current_components.items():
                                #print(component_name, component_value)
                                if component_name in index_type_components and type(component_value) == int:
                                    current_components[component_name] = comxponent_map[component_name].choices[component_value]



                            return list(current_components.values())

                        config_preset_dropdown = gr.Dropdown(
                            label="Config Presets",
                            choices=preset_values,
                            elem_id="config_preset_txt2img_dropdown" if self.is_txt2img else "config_preset_img2img_dropdown",
                        )
                        config_preset_dropdown.style(container=False) #set to True to give it a white box to sit in

                        config_preset_json = gr.Textbox(elem_id="config_preset_json" if self.is_txt2img else "config_preset_img2img_json" ,visible=False)


                        #self.txt2img_config_preset_dropdown = config_preset_dropdown


                        try:
                            components = list(component_map.values())
                            config_preset_dropdown.change(
                                fn=config_preset_dropdown_change,
                                show_progress=False,
                                inputs=[config_preset_dropdown, *components],
                                outputs=components
                                )
                        except AttributeError:
                            print(traceback.format_exc())   # prints the exception stacktrace
                            print("[ERROR][CRITICAL][Config-Presets] The Config-Presets extension encountered a fatal error. A component required by this extension no longer exists in the Web UI. This is most likely due to the A1111 Web UI being updated. Try updating the Config-Presets extension. If that doesn't work, please post a bug report at https://github.com/Zyin055/Config-Presets/issues and delete your extensions/Config-Presets folder until an update is published.")

                        config_preset_dropdown.change(
                            fn=None,
                            inputs=[],
                            outputs=[],
                            _js="function() { config_preset_dropdown_change() }",   # JS is used to update the Hires fix row to show/hide it
                        )


                        export_button = gr.Button(
                            value="export",
                            variant="primary",
                            elem_id="config_preset_export_button" if self.is_txt2img else "config_preset_export_img2img_dropdown",
                        )

                        export_button.click(
                            fn=export_config(component_map,self.img2img_image_ids),
                            inputs=list(
                                [fields_checkboxgroup] + [component_map[comp_name] for comp_name in
                                                                           component_ids if
                                                                           component_map[comp_name] is not None]),
                            outputs=[config_preset_json]
                            # _js="exportData()"
                        )
                        js="function() { exportData() }"  if self.is_txt2img else "function() { exportImg2ImgData() }"
                        export_button.click(  # need this to runa after save_config()
                            fn=None,
                            _js=js,  # restart Gradio
                        )
                    with gr.Column(scale=8, min_width=100, visible=False) as collapsable_column:
                        with gr.Row():
                            with gr.Column(scale=1, min_width=10):

                                def delete_selected_preset(config_preset_name):
                                    if config_preset_name in config_presets.keys():
                                        del config_presets[config_preset_name]
                                        print(f'Config Presets: deleted "{config_preset_name}"')

                                        write_config_presets_to_file(config_presets, config_file_name)

                                        preset_keys = list(config_presets.keys())
                                        return config_preset_dropdown.update(value=preset_keys[len(preset_keys)-1], choices=preset_keys)
                                    return gr.Dropdown.update() # do nothing if no value is selected

                                trash_button = gr.Button(
                                    value="\U0001F5D1",
                                    elem_id="config_preset_trash_button",
                                )
                                trash_button.click(
                                    fn=delete_selected_preset,
                                    inputs=[config_preset_dropdown],
                                    outputs=[config_preset_dropdown],
                                )
                                trash_button.click(
                                    fn=None,
                                    _js="function() { config_preset_settings_restart_gradio()}",  # restart Gradio
                                )

                            # with gr.Column(scale=2, min_width=55):
                            #     def open_file(f):
                            #         path = os.path.normpath(f)
                            #
                            #         if not os.path.exists(path):
                            #             print(f'Config Presets: The file at "{path}" does not exist.')
                            #             return
                            #
                            #         # copied from ui.py:538
                            #         if platform.system() == "Windows":
                            #             os.startfile(path)
                            #         elif platform.system() == "Darwin":
                            #             sp.Popen(["open", path])
                            #         else:
                            #             sp.Popen(["xdg-open", path])

                                # open_config_file_button = gr.Button(
                                #     value="Open config file...",
                                #     elem_id="config_presets_open_config_file_button",
                                # )
                                # open_config_file_button.click(
                                #     fn=lambda: open_file(f"{BASEDIR}/{config_file_name}"),
                                #     inputs=[],
                                #     outputs=[],
                                # )

                            with gr.Column(scale=2, min_width=50):
                                cancel_button = gr.Button(
                                    value="Cancel",
                                    elem_id="config_preset_cancel_save_button",
                                )

                    with gr.Column(scale=1, min_width=120, visible=True) as add_remove_button_column:
                        add_remove_button = gr.Button(
                            value="Add/Remove...",
                            elem_id="config_preset_add_button",
                        )

                with gr.Row() as collapsable_row:
                    collapsable_row.visible = False
                    with gr.Column():
                        with gr.Row():
                            with gr.Column(scale=10, min_width=100):
                                save_textbox = gr.Textbox(
                                    label="New preset name",
                                    placeholder="Ex: Low quality",
                                    # value="My Preset",
                                    max_lines=1,
                                    elem_id="config_preset_save_textbox",
                                )
                            with gr.Column(scale=2, min_width=60):
                                save_button = gr.Button(
                                    # value="Create",
                                    value="Save & Restart",
                                    variant="primary",
                                    elem_id="config_preset_save_button",
                                )

                                save_button.click(
                                    fn=save_config(config_presets, component_map, config_file_name),
                                    inputs=list(
                                        [save_textbox] + [fields_checkboxgroup] + [component_map[comp_name] for comp_name in
                                                                                   component_ids if
                                                                                   component_map[comp_name] is not None]),
                                    outputs=[config_preset_dropdown, save_textbox,config_preset_json],
                                    # _js="exportData()"
                                )
                                save_button.click(  # need this to runa after save_config()
                                    fn=None,
                                    _js="config_preset_settings_restart_gradio()",  # restart Gradio
                                )



                                def add_remove_button_click():
                                    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)

                                # def save_button_click(save_text):
                                #     if save_text == "":
                                #         return gr.update(), gr.update()
                                #     return gr.update(visible=True), gr.update(visible=False)

                                def cancel_button_click():
                                    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

                                add_remove_button.click(
                                    fn=add_remove_button_click,
                                    inputs=[],
                                    outputs=[collapsable_column, collapsable_row, add_remove_button_column],
                                )
                                # save_button.click(
                                #     fn=save_button_click,
                                #     inputs=[save_textbox],
                                #     outputs=[add_remove_button_column, collapsable_column],
                                # )
                                cancel_button.click(
                                    fn=cancel_button_click,
                                    inputs=[],
                                    outputs=[collapsable_column, collapsable_row, add_remove_button_column],
                                )

                        with gr.Row():
                            fields_checkboxgroup.render()


    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass


# Save the current values on the UI to a new entry in the config file
def save_config(config_presets, component_map, config_file_name):
    # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
    def func(new_setting_name, fields_to_save_list, *new_setting):
        if new_setting_name == "":
            return gr.Dropdown.update(), "" # do nothing if no label entered in textbox

        new_setting_map = {}    # dict[str, Any]    {"txt2img_steps": 10, ...}

        #print(f"component_map={component_map}")
        #print(f"new_setting={new_setting}")

        for i, component_id in enumerate(component_map.keys()):

            if component_id not in fields_to_save_list:
                #print(f"[Config-Presets] New preset '{new_setting_name}' will not include {component_id}")
                continue

            if component_map[component_id] is not None:
                new_value = new_setting[i]  # this gives the index when the component is a dropdown
                if component_id == "txt2img_sampling":
                    new_setting_map[component_id] = modules.sd_samplers.samplers[new_value].name
                elif component_id == "img2img_sampling":
                    new_setting_map[component_id] = modules.sd_samplers.samplers_for_img2img[new_value].name
                else:
                    # if component_id == "ext_ctl_image":
                    #     ndarray_to_list(new_value)
                    if component_id.startswith("txt2img_ControlNet-") or component_id.startswith("img2img_ControlNet-"):
                        if component_id.endswith("ext_ctl_image"):
                            continue
                        new_setting_map[component_id] = new_value
                        # ctl[component_id] = new_value
                    elif component_id.startswith("txt2img_ext_an_") or component_id.startswith("img2img_ext_an_"):
                        if component_id.endswith("ext_an_mask_image"):
                            continue
                        new_setting_map[component_id] = new_value
                    elif component_id.startswith("script_txt2img_") or component_id.startswith("script_img2img_"):
                        new_setting_map[component_id] = new_value
                    else:
                        new_setting_map[component_id] = new_value

                #print(f"Saving '{component_id}' as: {new_setting_map[component_id]} ({new_value})")

        #print(f"new_setting_map = {new_setting_map}")

        config_presets[new_setting_name]=new_setting_map
        write_config_presets_to_file(config_presets, config_file_name)

        # print(f"self.txt2img_config_preset_dropdown.choices before =\n{self.txt2img_config_preset_dropdown.choices}")
        # self.txt2img_config_preset_dropdown.choices = list(config_presets.keys())
        # print(f"self.txt2img_config_preset_dropdown.choices after =\n{self.txt2img_config_preset_dropdown.choices}")

        print(f"[Config-Presets] Added new preset: {new_setting_name}")
        print(f"[Config-Presets] Restarting UI...") # done in _js
        # update the dropdown with the new config preset, and clear the 'new preset name' textbox

        return gr.Dropdown.update(value=new_setting_name, choices=list(config_presets.keys())), "",new_setting_map

        # this errors when adding a 2nd config preset
        # the solution is supposed to be updating the backend Gradio object to reflect the frontend dropdown values, but it doesn't work. still throws: "ValueError: 0 is not in list"
        # workaround is to restart the whole UI after creating a new config preset by clicking the "Restart Gradio and Refresh Components" button in javascript
        # https://github.com/gradio-app/gradio/discussions/2848

    return func



# Save the current values on the UI to a new entry in the config file
def export_config(component_map,img2img_image_ids):
    # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
    def func(fields_to_save_list, *new_setting):


        new_setting_map = {}    # dict[str, Any]    {"txt2img_steps": 10, ...}
        ctls = {}
        an = {}
        for i, component_id in enumerate(component_map.keys()):
            # if component_id not in fields_to_save_list:
            #     #print(f"[Config-Presets] New preset '{new_setting_name}' will not include {component_id}")
            #     continue

            if component_map[component_id] is not None:
                new_value = new_setting[i]  # this gives the index when the component is a dropdown
                if component_id == "txt2img_sampling":
                    new_setting_map[component_id] = modules.sd_samplers.samplers[new_value].name
                elif component_id == "img2img_sampling":
                    new_setting_map[component_id] = modules.sd_samplers.samplers_for_img2img[new_value].name
                else:
                    # if component_id == "ext_ctl_image":
                    #     ndarray_to_list(new_value)
                    if component_id.startswith("txt2img_ControlNet-") or component_id.startswith("img2img_ControlNet-"):
                        if component_id.endswith("ext_ctl_image"):
                            continue

                        if component_id[19] not in ctls:
                            ctls[component_id[19]] = {}
                        ctls[component_id[19]][component_id[21:]]=new_value
                        # ctl[component_id] = new_value
                    elif component_id.startswith("txt2img_ext_an_") or component_id.startswith("img2img_ext_an_"):
                        if component_id.endswith("ext_an_mask_image"):
                            continue
                        an[component_id[8:]]=new_value
                    elif component_id.startswith("script_txt2img_") or component_id.startswith("script_img2img_"):
                        an[component_id[15:]]=new_value
                    elif component_id in img2img_image_ids:
                        continue
                    else:
                        new_setting_map[component_id] = new_value
        ext_arr = [None] * len(ctls)
        for key, value in ctls.items():
            ext_arr[int(key)]=value
        ext_arr.append(an)
        new_setting_map["ext"]=ext_arr

        aa=json.dumps(new_setting_map)
        return aa
    return func


def write_config_presets_to_file(config_presets, config_file_name: str):
    json_object = json.dumps(config_presets, indent=4)
    with open(f"{BASEDIR}/{config_file_name}", "w") as outfile:
        outfile.write(json_object)

def ndarray_to_list(d):
    if isinstance(d, np.ndarray):
        return d.tolist()
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = ndarray_to_list(v)
        elif isinstance(v, np.ndarray):
            d[k] = v.tolist()
        else:
            pass  # do nothing
    return d

