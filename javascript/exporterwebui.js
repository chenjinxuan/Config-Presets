


// function attachGalleryListeners1(tab_name) {
//   gallery = gradioApp().querySelector('#'+tab_name+'_gallery')
//   gallery?.addEventListener('click', () => gradioApp().getElementById(tab_name+"_exporter_button").click());
//   // gallery?.addEventListener('keydown', (e) => {
//   //   if (e.keyCode == 37 || e.keyCode == 39) // left or right arrow
//   //     gradioApp().getElementById(tab_name+"_exporter_button").click()
//   // });
//
//
//   // 创建导出按钮
//   const exporterButton = document.createElement("button");
//   exporterButton.innerHTML = "Export";
//   exporterButton.id = tab_name+"_exporter_button";
//   exporterButton.style.display = "none";
// exporterButton.onclick = function() {
//   let prompt = gradioApp().querySelector("#txt2img_prompt > label > textarea");
//
//   let dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(prompt.value);
//   let dlAnchorElem = document.createElement('a');
//   dlAnchorElem.setAttribute("href", dataStr);
//   dlAnchorElem.setAttribute("download", "form-data.json");
//   dlAnchorElem.click();
//   console.log("hahaha")
//
// }
//   exporterButton.className = "gr-button gr-button-lg gr-button-secondary";
//   exporterButton.style = `padding-left: 0.1em; padding-right: 0em; margin: 0.1em 0;max-height: 2em; max-width: 6em`;
//
//   // 创建新的div
//   const actionsColumn = document.createElement("div");
//   actionsColumn.id = `${tab_name}_actions_column`;
//   actionsColumn.className = "flex-shrink-0 pl-3 pr-3 pt-2 pb-2 text-right overflow-hidden";
//   actionsColumn.appendChild(exporterButton);
//
//   // // 将新创建的div添加到页面上
//   const parent = gradioApp().querySelector('#'+tab_name+'_gallery');
//    parent.insertBefore(actionsColumn, parent.firstChild);
//
// // gallery.appendChild(exporterButton);
//   return gallery;
//
// }
function sleep(seconds) {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

function getDate(){
  let now = new Date();
  let year = now.getFullYear();
  let month = (now.getMonth() + 1).toString().padStart(2, '0');
  let day = now.getDate().toString().padStart(2, '0');
  let hour = now.getHours().toString().padStart(2, '0');
  let minute = now.getMinutes().toString().padStart(2, '0');
  let second = now.getSeconds().toString().padStart(2, '0');
  let formattedTime = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  return formattedTime
}
function exportData() {
// 调用 sleep() 函数来睡眠 3 秒钟
  sleep(1).then(() => {
    dataStr = gradioApp().querySelector("#setting_sd_model_checkpoint > label > select").value;
    data2Str = gradioApp().querySelector("#config_preset_json > label > textarea").value;
    vae = gradioApp().querySelector("#setting_sd_vae > label > select").value;
    clip = gradioApp().querySelector("#setting_CLIP_stop_at_last_layers > div.w-full.flex.flex-col > div > input")
    const data2 = JSON.parse(data2Str);
    data2["model_name"]=dataStr;
    if (clip) {
      data2["CLIP_stop_at_last_layers"]=parseInt(clip.value, 10);
    }
    data2["vae"]=vae;

    const host = window.location.host;
    data2["host"]=host;

    const ext = []
    for (let i = 0; i < data2["ext"].length; i++) {
      console.log(data2["ext"][i]);
      if (data2["ext"][i]["ext_ctl_enabled"] == true) {
        ext_ctl_image = gradioApp().querySelector("#txt2img_ControlNet-"+i+"_ext_ctl_image > div.h-60.bg-gray-200 > div > img");
        if (ext_ctl_image){
          data2["ext"][i]["ext_ctl_image"]=ext_ctl_image.src;
        }
        ext.push(data2["ext"][i]);
      }
      if (data2["ext"][i]["ext_an_enabled"] == true) {
        ext_an_mask_image = gradioApp().querySelector("#txt2img_ext_an_mask_image > div.h-60.bg-gray-200 > div > img");
        if (ext_an_mask_image){
          data2["ext"][i]["ext_an_mask_image"]=ext_an_mask_image.src;
        }
        ext.push(data2["ext"][i]);
      }
      if (data2["ext"][i]["ad_enable"] == true) {
        ext.push(data2["ext"][i]);
      }
    };
    data2["ext"]=ext;
    const json = JSON.stringify(data2);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'style-'+getDate();
    link.href = url;
    link.click();
  });
}

function exportImg2ImgData() {
// 调用 sleep() 函数来睡眠 3 秒钟
  sleep(1).then(() => {
    dataStr = gradioApp().querySelector("#setting_sd_model_checkpoint > label > select").value;
    data2Str = gradioApp().querySelector("#config_preset_img2img_json > label > textarea").value;
    vae = gradioApp().querySelector("#setting_sd_vae > label > select").value;
    clip = gradioApp().querySelector("#setting_CLIP_stop_at_last_layers > div.w-full.flex.flex-col > div > input")
    const data2 = JSON.parse(data2Str);
    data2["model_name"]=dataStr;
    data2["vae"]=vae;
    if (clip) {
      data2["CLIP_stop_at_last_layers"]=parseInt(clip.value, 10);
    }
    const host = window.location.host;
    data2["host"]=host;
    const ext = []
    for (let i = 0; i < data2["ext"].length; i++) {
      if (data2["ext"][i]["ext_ctl_enabled"] == true) {
        ext_ctl_image = gradioApp().querySelector("#img2img_ControlNet-"+i+"_ext_ctl_image > div.h-60.bg-gray-200 > div > img");
        if (ext_ctl_image) {
          data2["ext"][i]["ext_ctl_image"]=ext_ctl_image.src;
        }
        ext.push(data2["ext"][i]);
      }
      if (data2["ext"][i]["ext_an_enabled"] == true) {
        ext_an_mask_image = gradioApp().querySelector("#img2img_ext_an_mask_image > div.h-60.bg-gray-200 > div > img");
        if (ext_an_mask_image) {
          data2["ext"][i]["ext_an_mask_image"]=ext_an_mask_image.src;
        }
        ext.push(data2["ext"][i]);
      }
      if (data2["ext"][i]["ad_enable"] == true) {
        ext.push(data2["ext"][i]);
      }
    }
    data2["ext"]=ext;
    //#img2img_image > div.h-60.bg-gray-200 > div > img
    img2img_image= gradioApp().querySelector("#img2img_image > div.h-60.bg-gray-200 > div > img");
    if (img2img_image) {
      data2["img2img_image"]=img2img_image.src;
    }
    img2img_sketch= gradioApp().querySelector("#img2img_sketch > div.h-60.bg-gray-200 > div > img");
    if (img2img_sketch) {
      data2["img2img_sketch"]=img2img_sketch.src;
    }
    img2maskimg= gradioApp().querySelector("#img2maskimg > div.h-60.bg-gray-200 > div > img");
    if (img2maskimg) {
      data2["img2maskimg"]=img2maskimg.src;
    }
    inpaint_sketch= gradioApp().querySelector("#inpaint_sketch > div.h-60.bg-gray-200 > div > img");
    if (inpaint_sketch) {
      data2["inpaint_sketch"]=inpaint_sketch.src;
    }
    img_inpaint_base= gradioApp().querySelector("#img_inpaint_base > div.h-60.bg-gray-200 > div > img");
    if (img_inpaint_base) {
      data2["img_inpaint_base"]=img_inpaint_base.src;
    }
    img_inpaint_mask= gradioApp().querySelector("#img_inpaint_mask > div.h-60.bg-gray-200 > div > img");
    if (img_inpaint_mask) {
      data2["img_inpaint_mask"]=img_inpaint_mask.src;
    }
    const json = JSON.stringify(data2);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'style-'+getDate();
    link.href = url;
    link.click();
  });
}
