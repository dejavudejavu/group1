// pages/clockIn/clockIn.js

//打卡日历页面
//var util = require('../../utils/util.js');
//var Bmob = require('../../utils/bmob.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    days:[],//三个属性date-当前日，isSign-是否签到，thisMonth-是否本月
    appraise:"Good!",
    comment:"你刚学了10个单词，成功迈出第一步",
    today:{year:2021,month:1,day:1,isSign:false},
    choosedDay:{year:2021,month:1,day:1,isSign:false},
    weekW:["日","一","二","三","四","五","六"],
  },
  onLoad:function(options){
   const date=new Date();
   const cur_year=date.getFullYear();
   const cur_month=date.getMonth();//0代表1月
   const cur_day=date.getDate()//1-31
   const cur_week=date.getDay();//0代表周日

   this.setData({
    "today.year":cur_year,
     "today.month":cur_month+1,
     "today.day":cur_day,
     "choosedDay":this.data.today,
   });
   this.fullDays(cur_year,cur_month);//填充days
  },
// 获取当月共多少天
getThisMonthDays:function(year, month){
  return new Date(year, month+1, 0).getDate();
},
//获取上一月多少天
getLastMonthDays:function(year, month){
  if(month==7)
  return new Date(year, 12, 0).getDate();
  else
  return new Date(year, month, 0).getDate();
},
// 获取当月第一天星期几
getFirstDayOfWeek:function(year, month) {
  return new Date(year, month, 1).getDay();
},
// 获取当月最后一天星期几
getLastDayOfWeek:function(year, month) {
  var day=this.getThisMonthDays(year,month);
  return new Date(year, month,day).getDay();
},
//填充days
fullDays(year,month){
  var that=this;
  var lastMonthDays=this.getLastMonthDays(year,month);//上一月天数
  var thisMonthDays=this.getThisMonthDays(year,month);//本月天数
  that.setData({days:[]});
  const firstDayWeek=this.getFirstDayOfWeek(year,month);//第一天星期
  const lastDayWeek=this.getLastDayOfWeek(year,month);//最后一天星期

  //填充上一月天数
  for(let i=0;i<firstDayWeek;i++){
    var obj={
      date:lastMonthDays-firstDayWeek+1,
      isSign:false,
      thisMonth:false,
    }
    that.data.days.push(obj);
    lastMonthDays++;
  }
  //填充本月天数
  for(let i=1;i<=thisMonthDays;i++){
    var obj={
      date:i,
      isSign:false,
      thisMonth:true,
    }
    that.data.days.push(obj);
  }
  //填充下一月天数
  for(let i=1;i<7-lastDayWeek;i++){
    var obj={
      date:i,
      isSign:false,
      thisMonth:false,
    }
    that.data.days.push(obj);
  }
  this.setData({
    days:that.data.days
  });
},

  toL(e){
    var NowMonth=this.data.choosedDay.month-1;
    var NowYear=this.data.choosedDay.year;
    if(NowMonth<1){
      NowMonth=12;
      NowYear--;
    }
    this.setData({
      choosedDay:{year:NowYear,month:NowMonth,day:1},
    });
    this.fullDays(this.data.choosedDay.year,this.data.choosedDay.month-1);
  },
  toR(e){
    var NowMonth=this.data.choosedDay.month+1;
    var NowYear=this.data.choosedDay.year;
    if(NowMonth>12){
      NowMonth=1;
      NowYear++;
    }
    this.setData({
      choosedDay:{year:NowYear,month:NowMonth,day:1},
    });
    this.fullDays(this.data.choosedDay.year,this.data.choosedDay.month-1);
  },

  //当前日是否打卡改为true
  signBtr(e){
    var thisMonthDays=this.getThisMonthDays(this.data.today.year,this.data.today.month);//本月天数
    for(var i=0;i<thisMonthDays;i++){
      if(this.data.today.day==this.data.days[i].date&&this.data.today.month==this.data.choosedDay.month&&this.data.today.year==this.data.choosedDay.year)
          this.setData({
            ["days["+i+"].isSign"]:"true",
            "today.isSign":true,
          });
    }
    wx.showToast({
      title: '打卡成功',
      icon: 'success',
      duration: 2000//持续的时间
    })
    setTimeout(function () {
      wx.reLaunch({
      url: '../share/share'
      })
      }, 2000)
  },
  toIndex(e){
    wx:wx.navigateTo({
      url: '',//填写首页地址
    })
  }
})