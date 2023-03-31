


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
    const data2 = JSON.parse(data2Str);
    let data = {
      "model_name": dataStr,
      "params": data2,
    };
    const json = JSON.stringify(data);
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
    const data2 = JSON.parse(data2Str);
    let data = {
      "model_name": dataStr,
      "params": data2,
    };
    const json = JSON.stringify(data);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'style-'+getDate();
    link.href = url;
    link.click();
  });
}
