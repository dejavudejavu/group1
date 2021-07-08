// pages/myPlan/myPlan.js
var app = getApp();
import Toast from '@vant/weapp/toast/toast';
Page({
  data: {
    total:"",
    book_cover:'',
    book_name:"",
    learnNum:[10,20,30,40,50,60,70],
    reviewNum:[0,10,20,30,40,50,60,70],
    nowPlan:{learn:0,review:3},//当前计划,数字为对应索引
    lastPlan:{learn:0,review:0},//修改后的计划,数字为对应索引
    spend:{lmin:5,rmin:15,total:20,day:500},//学习所需时间
  },
  onLoad:function(){
    var that=this
    wx.request({
      url: app.globalData.baseUrl+'/myPlan/getPlan', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
        console.log("data",data)
        // var nowPlan={
        //   learn:data.daily_learn,
        //   review:data.daily_review,
        // }
        that.setData({
          daily_learn: data.daily_learn,
          daily_review: data.daily_review,
          book_cover:app.globalData.baseUrl+data.book_cover,
          total:data.total,
          book_name:data.book_name,          
        })
        // console.log("nowPlan",that.data.nowPlan)
      }
    })  
  },
  saveBtr(e){
    this.setData({
      "nowPlan":this.data.lastPlan,
    })//此为需要保存的数据
    console.log(this.data.nowPlan)  
    wx.showToast({
      title: '保存成功！', 
      icon: 'success', 
      duration: 1500,
    })
   setTimeout(function(){
     wx:wx.reLaunch({
       url: '../myPlan/myPlan',//此处修改为主页地址
     })
   },1500)
  },
  LCli(e){
    const{picjer,value,index}=e.detail;
    Toast(`当前值:${value},当前索引:${index})`);
    this.setData({
      "lastPlan.learn":index,
      "spend.lmin":this.data.learnNum[index]/2,//学习花费时间
      "spend.day":Math.ceil(this.data.bookInfo.vocabulary/this.data.learnNum[index]),//学习花费天数
    })
    this.setData({"spend.total":Math.ceil(this.data.spend.lmin+this.data.spend.rmin),})
  },
  RCli(e){
    const{picjer,value,index}=e.detail;
    Toast(`当前值:${value},当前索引:${index})`);
    this.setData({
      "lastPlan.review":index,
      "spend.rmin":this.data.reviewNum[index]/2,
    })
    this.setData({
      "spend.total":Math.ceil(this.data.spend.lmin+this.data.spend.rmin),
    })
    //两个赋值需要分开，不然会出bug
  },

})