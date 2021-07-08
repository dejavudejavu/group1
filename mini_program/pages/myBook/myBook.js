// pages/myBook/myBook.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    picSrc:"pic/icon.png",
    nowBook:{title:"中考必背初升高必备英语单词500词汇精简版",vocabulary:300,pic:"pic/book.png",learned:100},
    allBooks:[
      {title:"中考必背初升高必备英语单词500词汇精简版第二版",vocabulary:300,pic:"pic/book.png",learned:0},
      {title:"中考必背2",vocabulary:300,pic:"pic/book.png",learned:50},
      {title:"中考必背3",vocabulary:300,pic:"pic/book.png",learned:90},
      {title:"中考必背4",vocabulary:300,pic:"pic/book.png",learned:200},
      {title:"中考必背5",vocabulary:300,pic:"pic/book.png",learned:100},
      {title:"中考必背6",vocabulary:300,pic:"pic/book.png",learned:100},
    ],
  },
  onLoad:function(){
    wx.request({
      url: app.globalData.baseUrl+'/changeBook/getMyBooks', 
      method:"POST",
      data:{
        user_id:app.globalData.userInfo.user_id
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"// 默认值
      },
      success (res) { 
        var data=res.data
      }
    })    
  },
  addBook(e){
    wx:wx.navigateTo({
      url: '../chooseBook/chooseBook',
    })
  },
  //正在学习的词书清空进度
  flashN(e){
    this.setData({
      "nowBook.learned":0,
    })
  },
  //其他词书清空进度
  flashO(e){
    console.log(e);
    const id=e.currentTarget.dataset.id;
    this.setData({
      ["allBooks["+id+"].learned"]:0,
    })

  },
  //更换当前正在学习的词书
  changeBook(e){
    var book=this.data.nowBook;
    const id=e.currentTarget.dataset.id;
    
    wx:wx.showToast({
      title: '替换成功',
      duration: 1000,
      icon: 'success',
    })
    this.setData({
      nowBook:this.data.allBooks[id],
      ["allBooks["+id+"]"]:book,
    });
  },
  //删除当前正在学习的词书
  deleteN(e){
    var id=e.currentTarget.dataset.id;
    const that=this;
    var book=that.data.allBooks[0];
    wx.showModal({
      content: '确认删除该书？',
      success: function (res) {
        if (res.confirm) {
          that.data.allBooks.splice(0,1);
          that.setData({
            allBooks:that.data.allBooks,
            nowBook:book,
          });
          console.log(that.data.allBooks);
        } else {//这里是点击了取消以后
          console.log(that.data.allBooks);
        }
      }
    })
  },
  //删除其他词书
  deleteO(e){
    var id=e.currentTarget.dataset.id;
    const that=this;
    wx.showModal({
      content: '确认删除该书？',
      success: function (res) {
        if (res.confirm) {
          that.data.allBooks.splice(id,1);
          that.setData({
            allBooks:that.data.allBooks,
          })
          console.log(that.data.allBooks);
        } else {//这里是点击了取消以后
          console.log(that.data.allBooks);
        }
      }
    })
  }

})