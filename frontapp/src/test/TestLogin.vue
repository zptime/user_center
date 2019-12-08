<template>
    <div class="Login">
        <input v-model="username" placeholder="用户名">
        <input v-model="password" type="password" placeholder="密码">
        <div>
            <button @click="testLogin" class="weui_btn weui_btn_primary">登录</button>
        </div>
    </div>
</template>

<script type="text/ecmascript-6">
    import {mapState, mapMutations } from 'vuex'
    import {testLogin} from '../service/getData'

    export default ({
        data (){
            return {
                username: 'fenghuo',
                password: 'fhuo_03'
            }
        },

        methods: {
            ...mapMutations([
                'ACCOUNT'
            ]),

            //初始化获取数据
            async testLogin(){
                //获取 choice 列表
                let res = await testLogin( this.username , this.password);
                if (res.c == 0){
                    this.ACCOUNT({name:this.username});
                    window.NonetestLogin = false;
                    this.$router.push('/m')
                }else{
                    alert(res.m);
                }
            },
        }

    })
</script>

<style>
    .Login{
        position: fixed;
        left: 50%;
        top: 50%;
        transform: translate(-50%,-50%);
        font-size: 1rem;
        color: #9b9b9b;
        letter-spacing: 0.05rem;
        width: 100%;
        text-align: center;
    }

    .Login input{
        height: 2rem;
        width: 60%;
        margin: 0.5rem auto;
        border: 1px solid #9b9b9b;
        border-radius: 4px;
        padding: 8px;
        font-size: 0.7rem;
        outline: none;
    }

    .Login button{
        width: 60%;
        height: 2rem;
        margin: 1.5rem auto;
    }

</style>
