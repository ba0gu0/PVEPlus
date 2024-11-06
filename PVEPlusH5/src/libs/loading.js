import {ElLoading} from 'element-plus';
import {isDark} from "@/libs/dark";
export const loadingFun = (loadText,  loadTarget = 'body') => {
    if (isDark.value){
        return ElLoading.service({
            target: loadTarget,
            lock: true,
            text: loadText,
            background: 'rgba(0, 0, 0, 1)',
        })
    }else {
        return ElLoading.service({
            target: loadTarget,
            lock: true,
            text: loadText,
            background: 'rgba(256, 256, 256, 1)',
        })
    }
}