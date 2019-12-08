

## Issues 

1、和平常调用一般组件一样，声明，调用。
2、data里面保证几个数据，例子如下:
      data () {
        return {
          counter : 1, //默认已经显示出15条数据 count等于一是让从16条开始加载
          num : 15,  // 一次显示多少条
          pageStart : 0, // 开始页数
          pageEnd : 0, // 结束页数
          listdata: [], // 下拉更新数据存放数组
          downdata: []  // 上拉更多的数据存放数组
        }
     }
3、html需要迭代更新的代码写两次，例如:
       <v-scroll :on-refresh="onRefresh" :on-infinite="onInfinite">
           <ul>
             <li v-for="(item,index) in listdata" >{{item.name}}</li>
             <li v-for="(item,index) in downdata" >{{item.name}}</li>
           </ul>
        </v-scroll>
    一次用于刷新，一次用于加载
4、引用的标签放在需要更新的标签外面，例上面的 <v-scroll></v-scroll>,下拉刷新回调函数绑定 :on-refresh
   上拉加载回调函数绑定 :on-infinite
5、on-refresh(done),on-infinite(done)函数回调里面传入一个done,表示此处下拉刷新或上拉加载动作已经完成，可以执行下一次操作。




