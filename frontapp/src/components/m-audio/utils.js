/**
 * Created by jie on 2018/3/28.
 */

export const copy = (target, source) => {
    if (typeof target != 'object'){
        target = {}
    }
    if (typeof source == 'object'){
        for(let key in source){
            if(source.hasOwnProperty(key)){
                target[key] = source[key]
            }
        }
    }
    return target
}
