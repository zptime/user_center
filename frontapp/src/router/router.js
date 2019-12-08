const home = r => require.ensure([], () => r(require('../page/Home')), 'home')
const testLogin = r => require.ensure([], () => r(require('../test/TestLogin.vue')), 'testLogin')
const defaultPath = () =>  process.env.NODE_ENV == 'development'? 'homePage': 'homePage'

/*扫码注册*/
const registerScan = r => require.ensure([], () => r(require('../page/register/Scan.vue')), 'registerScan')
const enrollParent = r => require.ensure([], () => r(require('../page/register/EnrollParent.vue')), 'enrollParent')
const enrollTeacher = r => require.ensure([], () => r(require('../page/register/EnrollTeacher.vue')), 'enrollTeacher')
const verify = r => require.ensure([], () => r(require('../page/register/Verify.vue')), 'verify')
const identify = r => require.ensure([], () => r(require('../page/register/Identify.vue')), 'identify')

const homePage = r => require.ensure([], () => r(require('../page/home/HomePage')), 'homePage')

/*个人中心*/
//教师端个人中心
const personalHome = r => require.ensure([], () => r(require('../page/personal/teacher/home')), 'personaHome')
const personalSwitch = r => require.ensure([], () => r(require('../page/personal/teacher/switch')), 'personalSwitch')
const personalInformation = r => require.ensure([], () => r(require('../page/personal/teacher/information')), 'personalInformation')

//家长端个人中心
const parentPersonalHome = r => require.ensure([], () => r(require('../page/personal/parent/home')), 'parentPersonalHome')
const parentPersonalFamily = r => require.ensure([], () => r(require('../page/personal/parent/family')), 'parentPersonalFamily')
const parentPersonalInformation = r => require.ensure([], () => r(require('../page/personal/parent/information')), 'parentPersonalInformation')
const parentPersonalInvite = r => require.ensure([], () => r(require('../page/personal/parent/invite')), 'parentPersonalInvite')
const addChild = r => require.ensure([], () => r(require('../page/personal/parent/addChild')), 'addChild')
const addParent = r => require.ensure([], () => r(require('../page/personal/parent/addParent')), 'addParent')
const teachClasses = r => require.ensure([], () => r(require('../page/personal/teacher/TeachClasses')), 'teachClasses')
const addClasses = r => require.ensure([], () => r(require('../page/personal/teacher/AddClasses')), 'addClasses')
const classCode = r => require.ensure([], () => r(require('../page/personal/teacher/TeachClassMsg')), 'classCode')


const m = {
  template: `<div>
        <keep-alive>
            <router-view v-if="$route.meta.keepAlive">
            </router-view>
        </keep-alive>
        <router-view v-if="!$route.meta.keepAlive"></router-view>
    </div>`
}

export default [
    {
        path: '',
        redirect:  '/m'
    },
    {
        path: '/m',
        component: m,
        children: [
            //地址为空时跳转home页面
            {
                path: '',
                redirect: defaultPath
            },
            //home页
            {
                name: 'home',
                path: 'home',
                component: home
            },
            //扫码注册
            {
              path: 'register',
              component: m,
              children: [
                {
                  path: '',
                  redirect: 'registerScan'
                },
                {//扫码页
                  name:'registerScan',
                  path: 'registerScan',
                  component: registerScan
                },
                {//家长注册页
                  name:'enrollParent',
                  path: 'enrollParent',
                  component: enrollParent
                },
                {//老师注册页
                  name:'enrollTeacher',
                  path: 'enrollTeacher',
                  component: enrollTeacher
                },
                {//短信验证页
                  name:'verify',
                  path: 'verify',
                  component: verify
                },
                {//身份选择页
                  name:'identify',
                  path: 'identify',
                  component: identify
                },
              ]
            },
            //个人中心教师端
            {
              path: 'personal',
              component: m,
              children: [
                  //教师端
                {
                  path: '',
                  redirect: 'teacher/home'
                },
                {//主页
                  name:'personalHome',
                  path: 'teacher/home',
                  component: personalHome
                },
                {//切换角色
                  name:'personalSwitch',
                  path: 'teacher/switch',
                  component: personalSwitch
                },
                {//个人信息
                  name:'personalInformation',
                  path: 'teacher/information',
                  component: personalInformation
                },
                //家长端
                {//主页
                  name:'parentPersonalHome',
                  path: 'parent/home',
                  component: parentPersonalHome
                },
                {//我的家庭
                  name:'parentPersonalFamily',
                  path: 'parent/family',
                  component: parentPersonalFamily
                },
                {//邀请家庭成员
                  name:'parentPersonalInvite',
                  path: 'parent/invite',
                  component: parentPersonalInvite
                },
                {//我的信息
                  name:'parentPersonalInformation',
                  path: 'parent/information',
                  component: parentPersonalInformation
                },
                {//添加孩子
                  name:'addChild',
                  path: 'parent/addChild',
                  component: addChild
                },
               {//添加家长
                  name:'addParent',
                  path: 'parent/addParent',
                  component: addParent
                },

                {
                  name:'addClasses',
                  path: 'addClasses',
                  component: addClasses
                },
                {//任教班级
                  name:'teachClasses',
                  path: 'teacher/teachClasses',
                  component: teachClasses
                },
                {//班级二维码
                  name:'classCode',
                  path: 'teacher/classCode',
                  component: classCode,
                },
              ]
            },
            //个人中心家长端
            {
              path: 'personal_parent',
              component: m,
              children  :[
                {
                  path: '',
                  redirect: '/m/personal/parent/home'
                },
              ]
            },
            //登录测试页
            {
              name: 'homePage',
              path: 'homePage',
              component: homePage
            },
            {
                path: 'test',
                component: m,
                children: [
                    {
                        path: '',
                        redirect: 'testLogin'
                    },
                    {
                        path: 'testLogin',
                        component: testLogin
                    }
                ]
            }
        ]
    }
]
