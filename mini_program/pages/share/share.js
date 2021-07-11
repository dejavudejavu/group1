// pages/share/share.js
Page({

  data: {
    head:"pic/head.png",//头像地址
    sentence:"除了tks，如何花式说“谢谢”",
    example:{eng:"i own you big time",chi:"我欠你一个人情"},
    week:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    month:["January","February","March","April","May","June","July","August","September","October","November","December"],
    date:{week:3,month:7,day:7},
    wxSym:"pic/wx.png",
  },
  onLoad(){
    wx.setNavigationBarTitle({ title:'分享'})
    const date=new Date();
    const week=date.getDay();
    const month=date.getMonth();
    const day=date.getDate();
    console.log(date);
    this.setData({
      "date.week":week,
      "date.month":month,
      "date.day":day,
    })
  },
  onShareAppMessage: function( options ){
    　　var that = this;
    　　// 设置菜单中的转发按钮触发转发事件时的转发内容
    　　var shareObj = {
    　　　　title: "转发的标题",        // 默认是小程序的名称(可以写slogan等)
    　　　　path: '/pages/share/share',        // 默认是当前页面，必须是以‘/’开头的完整路径
    　　　　imgUrl: '',     //自定义图片路径，可以是本地文件路径、代码包文件路径或者网络图片路径，支持PNG及JPG，不传入 imageUrl 则使用默认截图。显示图片长宽比是 5:4
    　　　　success: function(res){
    　　　　　　// 转发成功之后的回调
    　　　　　　if(res.errMsg == 'shareAppMessage:ok'){
    　　　　　　}
    　　　　},
    　　　　fail: function(){
    　　　　　　// 转发失败之后的回调
    　　　　　　if(res.errMsg == 'shareAppMessage:fail cancel'){
    　　　　　　　　// 用户取消转发
    　　　　　　}else if(res.errMsg == 'shareAppMessage:fail'){
    　　　　　　　　// 转发失败，其中 detail message 为详细失败信息
    　　　　　　}
    　　　　}
      }
    　　// 来自页面内的按钮的转发
    　　if( options.from == 'button' ){
    　　　　var eData = options.target.dataset;
    　　　　console.log( eData.name );     // shareBtn
    　　　　// 此处可以修改 shareObj 中的内容
    　　　　shareObj.path = '/pages/btnname/btnname?btn_name='+eData.name;
    　　}
    　　// 返回shareObj
    　　return shareObj;
    }
})