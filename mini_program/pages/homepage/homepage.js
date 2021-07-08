// pages/homepage/homepage.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    avatar:"",
    user_name:"",
    book_cover:"",
    book_name:"",
    days:"",
    left_days:"",
    to_learn: "",
    words: "" ,
    total:"",
    learned:""   
  },
  toWrongCollection(){
    wx.navigateTo({
      url: '../wrongSet/wrongSet',
    })
  },
  toSetPlan(){
    wx.navigateTo({
      url: '../myPlan/myPlan'
    })    
  },
  toStart(){
    wx.navigateTo({
      url: '../doHomework/doHomework'
    })
  },
  toPersonal(){
    wx.navigateTo({
      url: '../personal/personal'
    })    
  },
  toChooseBook(){
    wx.navigateTo({
      url: '../myBook/myBook'
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if(app.globalData.userInfo==null){
      var that=this
      wx.login({
        success: res => {
          console.log("res",res) 
          var code=res.code  
          wx.getSetting({
            success (res){
              if (res.authSetting['scope.userInfo']) {
                console.log("已授权")
                wx.getUserInfo({
                  success: function (res) {
                    var userInfo=JSON.parse(res.rawData)
                    console.log("userInfo",userInfo)
                    app.globalData.userInfo= {
                      user_name:userInfo.nickName,
                      user_id:code,
                      avatar:userInfo.avatarUrl
                    }
                    wx.request({
                      url: app.globalData.baseUrl+'/login/', 
                      method:"POST",
                      data: app.globalData.userInfo,
                      header: {
                        "Content-Type": "application/x-www-form-urlencoded"// 默认值
                      },
                      success (res) {     
                        var data=res.data             
                        console.log(data)
                        app.globalData.userInfo.user_id=data.user_id
                        console.log("app.globalData.userInfo",app.globalData.userInfo)
                        that.setData({
                          avatar:app.globalData.userInfo.avatar,
                          user_name:app.globalData.userInfo.user_name
                        })  
                        wx.request({
                          url: app.globalData.baseUrl+'/homepage/', 
                          method:"POST",
                          data: {
                            user_id:app.globalData.userInfo.user_id,
                          },
                          header: {
                            "Content-Type": "application/x-www-form-urlencoded"// 默认值
                          },
                          success (res) { 
                            console.log(res)
                            var data=res.data
                            that.setData({
                              book_cover:app.globalData.baseUrl+data.book_cover,
                              book_name:data.book_name,
                              days:data.days,
                              left_days:data.left_days,
                              to_learn: data.to_learn,
                              words: data.words,
                              total:data.total,
                              learned:data.learned
                            })
                            if(res.data.days==null){
                              wx.navigateTo({
                                url: '../chooseBook/chooseBook',
                              })                         
                            }
                          }
                        })                             
                      },
                      fail(err) {
                        console.log(err)
                      }
                    })                 
                  },
                })                
              }else{
                console.log("未授权")
              }
            }
          })         

        }
      })        
    }
    else{
      this.setData({
        avatar:app.globalData.userInfo.avatarUrl,
        user_name:app.globalData.userInfo.nickName
      })  
    }
    // 登录
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
 
})
