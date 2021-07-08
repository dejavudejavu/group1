// pages/wrongSet/wrongSet.js
var app = getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    wrongWords:[
      {word:"afternoon1",symbol:"[ɑ:ftnu:n]",meaning:"下午1",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon2",symbol:"[ɑ:ftnu:n]",meaning:"下午2",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon3",symbol:"[ɑ:ftnu:n]",meaning:"下午3",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon3",symbol:"[ɑ:ftnu:n]",meaning:"下午3",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon3",symbol:"[ɑ:ftnu:n]",meaning:"下午3",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon3",symbol:"[ɑ:ftnu:n]",meaning:"下午3",type:"n",status:true,exSrc:"pic/open.png"},
      {word:"afternoon3",symbol:"[ɑ:ftnu:n]",meaning:"下午3",type:"n",status:true,exSrc:"pic/open.png"},
    ],
    exSrc:"pic/open.png",//查看释义右侧图标
    exStatus:false,//展开状态，true为展开，false为关闭
    checked:false,
  },
  onLoad:function(){
    wx.request({
      url: app.globalData.baseUrl+'/practice/getWords', 
      method:"POST",
      data: {
        user_id:app.globalData.userInfo.user_id,
        source:2
      },      
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) {
        var data=res.data
        console.log("words",data)
      }    
    })
  },
  interpretationCli(e){
    const id=e.currentTarget.dataset.id;
    console.log(e);
    if(this.data.wrongWords[id].status==true){
      this.setData({
        ["wrongWords["+id+"].exSrc"]:"pic/back.png",
        ["wrongWords["+id+"].status"]:false,
    })}else{
      this.setData({
        ["wrongWords["+id+"].exSrc"]:"pic/open.png",
        ["wrongWords["+id+"].status"]:true,
      })
    }
  },

  switchCli(e){
    const len=this.data.wrongWords.length;
    console.log(e);
    if(this.data.checked==false){
    for(var i=0;i<len;i++){
      this.setData({
        ["wrongWords["+i+"].status"]:false,
        checked:true,
      })
    }}else{
      for(var i=0;i<len;i++){
        this.setData({
          ["wrongWords["+i+"].status"]:true,
          checked:false,
        })
      }
    }

  }
})