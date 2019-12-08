



//显示文字toast
export const showTextToast =(context,str) =>{
  let showTip = 'Loading';
  if(str){
    showTip = str;
  }
  context.$vux.toast.show({
    type: 'text',
    text: showTip
  })
}


//显示文字loading
export const showTextLoading =(context,str)=>{
  let showTip = 'Loading';
  if(str){
    showTip = str;
  }
  context.$vux.loading.show({
    text:showTip
  })
}

//隐藏文字loading
export const hideTextLoading = (context)=>{
  context.$vux.loading.hide()
}
