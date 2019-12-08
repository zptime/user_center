/**
 * Created by jie on 2016/10/26.
 */
function URLs(param1, param2, param3){
    var debug = true
    //var debug = false;
    var mockURLs = {
        /***************path************************/
        root: "/",
        PStudentmain: "/page/student",
        Pstudentadd: "/page/student/add",
        Pstudentmodify: "/page/student/modify",
        Pstudentview: "/page/student/view",
        Pteachermain: "/page/teacher",
        Pteacheradd: "/page/teacher/add",
        Pteachermodify: "/page/teacher/modify",
        Pteacherview: "/page/teacher/view",
        Pparentmain: "/page/parent",
        Pparentadd: "/page/parent/add",
        Pparentmodify: "/page/parent/modify",
        Pparentview: "/page/parent/view",

        /***************api************************/
        Aliststudent: "/api/list/student",
        Alistgrade: "/api/list/grade",
        Alistclass: "/api/list/class",
        Aimportstudent:"/api/import/student",
        //Adetailstudent: "/static/mock/student_detail.json"
    };
    var URLs = {
        /***************path************************/
        root: "/",
        PStudentmain: "/page/student",
        Pstudentadd: "/page/student/add",
        Pstudentmodify: "/page/student/modify",
        Pstudentview: "/page/student/view",
        Pteachermain: "/page/teacher",
        Pteacheradd: "/page/teacher/add",
        Pteachermodify: "/page/teacher/modify",
        Pteacherview: "/page/teacher/view",
        Pparentmain: "/page/parent",
        Pparentadd: "/page/parent/add",
        Pparentmodify: "/page/parent/modify",
        Pparentview: "/page/parent/view",
        /***************api************************/
        //学生
        Aliststudent: "/api/list/student",
        Alistgrade: "/api/list/grade",
        Alistclass: "/api/list/class",
        Aaddstudent: "/api/add/student",
        Aupdatestudet: "/api/update/student",
        Adeletestudent: "/api/delete/student",
        Adetailstudent: "/api/detail/student",
        Aimportstudent:"/api/import/student",
        //教师
        //家长
        //学校-年级-班级
        Alistgrade: "/api/list/grade",
        Alistclass: "/api/list/class",
        //模板工厂
        Pmodalfactory: "pages/modalfactory",
    };
    if(debug === true){
        return mockURLs;
    } else{
        return URLs;
    }
}