// pages/wordtest/wordtest.js
var app = getApp();
Page({
  jumpBtn:function(options){
    wx.navigateBack()
  },

  /**
   * 页面的初始数据
   */
  data: {
    wordType:"n.",
    //四个选项
    choose:[{
      id:0,
      c:"寻求者",
      bac:"white",
      col:"balck",
      img:""
    },
    {
      id:1,
      c:"下午",
      bac:"white",
      col:"balck",
      img:""
    },{id:2,c:"中午",bac:"white",col:"balck",img:""},{id:3,c:"晚上",bac:"white",col:"balck",img:""},],
    //正确答案id
    trueAnswer:1,
    //正确答案
    answer:"下午",
    //点击后按钮改变的背景色和字体色
    RCol:{
      bac:"white",
      col:"black",
    },
    ECol:{
      bac:"white",
      col:"black",
    },

    pronunciation:"[ˌɑːftəˈnuːn]",
    wordText:"afternoon",
  },
  onLoad(){
    wx.setNavigationBarTitle({ title:'单词100'})
  },
   //正确颜色
   RcolChange:function(e){
    var k=this.data.trueAnswer;
    var rb="choose["+k+"].bac";//正确答案背景色
    var rc="choose["+k+"].col"//正确答案字体色
    var rp="choose["+k+"].img"//正确答案图片

    this.setData({    
      [rb]:"#43caac",
      [rc]:"white",
      [rp]:"pic/right.png",
    });
    console.log(this.choose);
    setTimeout(function () {
      wx.reLaunch({
      url: '../doHomework/doHomework'
      })
      }, 1500)
   },
   //错误颜色
   
  EcolChange(e){
    console.log(e);
    var fal=e.currentTarget.dataset.operaction;//获取选错答案的id
    console.log(fal);
    var k=this.data.trueAnswer;//获取正确答案的id
    var rb="choose["+k+"].bac";//正确答案背景色
    var rc="choose["+k+"].col";//正确答案字体色
    var rp="choose["+k+"].img"//正确答案图片
    var eb="choose["+fal+"].bac";//错误答案背景色
    var ec="choose["+fal+"].col";//错误答案字体色
    var ep="choose["+fal+"].img"//正确答案图片

    this.setData({    
      [rb]:"#43caac",
      [rc]:"white",
      [rp]:"pic/right.png",
      [eb]:"#ff4d5e",
      [ec]:"white",
      [ep]:"pic/error.png"
    });

    setTimeout(function () {
      wx.reLaunch({
      url: '../doHomework/doHomework'
      })
      }, 1500)    
   },
   tabClick(e){
     console.log(e);
      this.setData(
        {
          click:true,
        }
      )      
   },
})