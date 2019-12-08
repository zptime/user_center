/**
 * Created by jie on 2016/11/14.
 */
!
//localStorage.setItem(key, value)    //���ü�¼
// localStorage.getItem(key)           //��ȡ��¼
// localStorage.removeItem(key)        //ɾ���������µ�����¼
// localStorage.clear()                //ɾ�������������м�¼

function(o) {
	"use strict";
    var t = {
        GRADE_LIST : [],
        CLASS_LIST : [],
        LOWER_LIMIT_YEAR: 2000,
        CURRENT_YEAR: new Date().getFullYear(),
        YEAR_LIST : [],
        get_current_year: function(){
            if (localStorage && localStorage.getItem('current_year')!=null){
                var str = localStorage.getItem('current_year');
                return str;
            }else{
                var res = '',defaults = new Date().getFullYear();
                myajax({
                    url: '/api/display/current_term',
                    async: false
                },function (data) {
                    if(data.c == 0)
                        res = data.d.substr(0,4);
                    else
                        res = defaults
                });
                localStorage.setItem('current_year', res);
                return res;
            }
        },
        get_year_list: function(start, end){
            if (localStorage && localStorage.getItem('year_list')!=null){
                var list_str = localStorage.getItem('year_list');
                return JSON.parse(list_str);
            }else{
                var res = [];
                if (start){
                    res[0] = start;
                } else{
                    res[0] = this.LOWER_LIMIT_YEAR;
                }
                if (end && end > start){
                    for(var i = 1; i<= end-start; i++){
                        res[i] = start+i;
                    }
                }
                res =  res.reverse();
                localStorage.setItem('year_list', JSON.stringify(res));
                return res;
            }
        },
        get_grade_list : function(){
            if (localStorage && localStorage.getItem('grade_list')!=null){
                var list_str = localStorage.getItem('grade_list');
                return JSON.parse(list_str);
            }else{
                var res = null,defaults = [];
                myajax({
                    url: URLs().Alistgrade,
                    async: false
                },function(data){
                    if (data.c == 0)
                        res = data.d
                    else
                        res = defaults
                });
                localStorage.setItem('grade_list', JSON.stringify(res));
                return res;
            }
        },
        get_class_list : function () {
            if (localStorage && localStorage.getItem('class_list')!=null ){
                var list_str = localStorage.getItem('class_list');
                return JSON.parse(list_str);
            }
            else{
                var res = null,defaults = [];
                myajax({
                    url: URLs().Alistclass,
                    async: false
                },function(data){
                    if (data.c == 0)
                        res = data.d
                    else
                        res = defaults
                });
                localStorage.setItem('class_list', JSON.stringify(res));
                return res;
            }
        },
        init : function () {
            this.GRADE_LIST = this.get_grade_list();
            this.CLASS_LIST = this.get_class_list();
            this.CURRENT_YEAR = this.get_current_year();
            this.YEAR_LIST = this.get_year_list(this.LOWER_LIMIT_YEAR, this.CURRENT_YEAR)
        },
        clear: function(){
            localStorage.removeItem('grade_list');
            localStorage.removeItem('class_list');
            localStorage.removeItem('current_year');
            localStorage.removeItem('year_list');
        },
        refresh : function () {
            this.clear();
            this.init();
        },
    };
    t.init(), o.HX_CACHE = t
}(window);