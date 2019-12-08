export const uploadBlobImageInner = async(url,key, base64Str,type) =>{
  //alert("uploadBlobImageInner run");
  let blob = b64toBlob(base64Str,'image/png');

  return new Promise((resolve, reject) => {
    var formData = new FormData();
    formData.append(key, new File([blob], new Date().getTime().toString() + '.jpg'));
    var xhr = new XMLHttpRequest();
    // 开始上传
    xhr.open(type, url , true);
    // 发送数据
    xhr.send(formData);
    xhr.onreadystatechange = () => {
      //alert("readyState=" + xhr.readyState +",status=" + xhr.status + ",response=" + xhr.response);
      if (xhr.readyState == 4) {
        if (xhr.status == 200) {
          let obj = xhr.response
          if (typeof obj !== 'object') {
            obj = JSON.parse(obj);
          }

          resolve(obj)
        } else if (xhr.status >= 400 && xhr.status < 500) {
          let msg = '网络异常';
          let obj = xhr.response
          try {
            obj = JSON.parse(obj);
            if (obj.m) {
              msg = obj.m
            }
          } catch (e) {
            msg = obj
          }

          setTimeout(function () {
            alert(msg)
          }, 1);

          reject(msg)
        }
        else {
          reject(xhr)
        }
      }
    }
  });
}

export const b64toBlob = (b64Data, contentType, sliceSize) =>{
  contentType = contentType || '';
  sliceSize = sliceSize || 512;
  var byteCharacters = atob(b64Data);
  var byteArrays = [];

  for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    var slice = byteCharacters.slice(offset, offset + sliceSize);
    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }

  var blob = new Blob(byteArrays, { type: contentType });
  return blob;
}

export const uploadFileInner = async(url,key, fileObj,type) =>{
  return new Promise((resolve, reject) => {
    var xhr = new XMLHttpRequest();
    var form = new FormData(); // FormData 对象
    form.append(key, fileObj); // 文件对象
    xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
    xhr.open(type, url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
    xhr.send(form); //开始上传，发送form数据
    xhr.onreadystatechange = () => {
      if (xhr.readyState == 4) {
        if (xhr.status == 200) {
          let obj = xhr.response
          if (typeof obj !== 'object') {
            obj = JSON.parse(obj);
          }

          resolve(obj)
        } else if (xhr.status >= 400 && xhr.status < 500) {
          let msg = '网络异常';
          let obj = xhr.response
          try {
            obj = JSON.parse(obj);
            if (obj.m) {
              msg = obj.m
            }
          } catch (e) {
            msg = obj
          }

          setTimeout(function () {
            alert(msg)
          }, 1);

          reject(msg)
        }
        else {
          reject(xhr)
        }
      }
    }
  });
}
