


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

function exportData() {
    data = gradioApp().getElementById("setting_sd_model_checkpoint").innerText;


  const blob = new Blob([data], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.download = 'data.json';
  link.href = url;
  link.click();
}
