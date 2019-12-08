import {
	baseUrl
} from './env'

//import axios from 'axios'

export default async(url = '', data = {}, type = 'POST', method = '', headerConfig = {withCredentials: true} ) => {
	type = type.toUpperCase();
	url = baseUrl + url;

	if (type == 'GET') {
		let dataStr = ''; //数据拼接字符串
		Object.keys(data).forEach(key => {
			dataStr += key + '=' + data[key] + '&';
		})

		if (dataStr !== '') {
			dataStr = dataStr.substr(0, dataStr.lastIndexOf('&'));
			url = url + '?' + dataStr;
		}
	}

	if (window.fetch && method == 'fetch') {
		let requestConfig = {
			credentials: 'include',
			method: type,
			headers: {
				'Content-Type': 'application/json'
				//'Accept': '*/*',
				//'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			},
			mode: "cors",
			cache: "force-cache",
		}

		if (type == 'POST') {
			Object.defineProperty(requestConfig, 'body', {
				value: JSON.stringify(data)
			})
		}

		try {
			const response = await fetch(url, requestConfig);
			const responseJson = await response.json();
			return responseJson
		} catch (error) {
			throw new Error(error)
		}
	} else {
			return new Promise((resolve, reject) => {
				let requestObj;
				if (window.XMLHttpRequest) {
					requestObj = new XMLHttpRequest();
				} else {
					requestObj = new ActiveXObject;
				}
				let sendData = data;
				if (type == 'POST') {
					let ret = ''
					for (let it in data) {
					  ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
					}
					if ( ret.length > 0){
						sendData = ret.substr(0,ret.length-1);
					}else{
						sendData = '';
					}
				}
				requestObj.open(type, url, true);
				//requestObj.withCredentials = true; //支持跨域cookie
				requestObj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
				requestObj.send(sendData);

				requestObj.onreadystatechange = () => {
					if (requestObj.readyState == 4) {
						if (requestObj.status == 200) {
							let obj = requestObj.response
							if (typeof obj !== 'object') {
								obj = JSON.parse(obj);
							}
							resolve(obj)
						} else if(requestObj.status>=400 && requestObj.status<500){
						  let msg = '网络异常';
						  let obj = requestObj.response
              try {
                obj = JSON.parse(obj);
                if (obj.m){
                  msg = obj.m
                }
              } catch (e) {
                msg = obj
              }
              setTimeout(function () {
                alert(msg)
              },1);
              reject(msg)
            }
						else {
							reject(requestObj)
						}
					}
				}

				// 发送 POST 请求
				/*axios({
				  method: type,
				  url: url,
				  data: data,
			      withCredentials: true, // default
				  transformRequest: [function (data) {
					// Do whatever you want to transform the data
					let ret = ''
					for (let it in data) {
					  ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
					}
					return ret
				  }],
				  headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				  }
				}).then(function (response) {
					let obj = response.data;
					if (typeof obj !== 'object') {
						obj = JSON.parse(obj);
					}
					resolve(obj)
				}).catch(function (error) {
					reject(error)
				})*/
			})

	}
}