import random


json_Save={"activityName":"activityName",
                 "activityImg":"http://yjdf-oss-uat.oss-cn-shanghai.aliyuncs.com/uat/2020/7/30/1596073329456.jpg",
                 "startTime":"2020-07-30 00:00:00",
                 "endTime":"2020-08-25 00:00:00",
                 "applyEndTime":"2020-08-15 09:41:30",
                 "approveStartTime":"2020-07-30 08:00:00",
                 "approveEndTime":"2020-08-20 00:00:00",
                 "orderStartTime":"2020-07-30 08:02:00",
                 "orderEndTime":"2020-08-18 00:00:00",
                 "goodsList":[
                     {"goodsId":13,"goodsImg":"https://img.alicdn.com/imgextra/i1/4009987183/O1CN01uobtcz22vrYHmEvV1_!!0-item_pic.jpg","goodsName":"防晒小晶钻","skuId":13,"skuNo":"DEV20200729001","num":1,"freightPrice":1,"sequence":1},
                     {"goodsId":1,"goodsImg":"http://qiniu-dev.yjdfmall.com//Public/Uploads/ueditor/php/upload/image/Common/20200416/1587016974147277.jpg","goodsName":"商品1号","skuId":1,"skuNo":"0001","num":1,"freightPrice":1,"sequence":2},
                     {"goodsId":9,"goodsImg":"http://qiniu-uat.yjdfmall.com//Public/Uploads/ueditor/php/upload/image/Common/20200703/1593747815717914.jpg","goodsName":"姬存希轻透炫彩气垫BB霜（1+1）","skuId":9,"skuNo":"BB123","num":1,"freightPrice":1,"sequence":3}
                 ],
                 "approveCodeList":[],
                 "levelList":[{"bizId":8,"bizName":"一级经销商","canApply":True},
                              {"bizId":7,"bizName":"二级经销商","canApply":True},
                              {"bizId":6,"bizName":"优秀省代","canApply":True},
                              {"bizId":5,"bizName":"省代","canApply":True},
                              {"bizId":9,"bizName":"准省代","canApply":True},
                              {"bizId":4,"bizName":"市级","canApply":True},
                              {"bizId":3,"bizName":"县级","canApply":True},
                              {"bizId":2,"bizName":"团购","canApply":True}],
                 "groupList":[{"bizId":1,"bizName":"1群"},
                              {"bizId":2,"bizName":"2群"},
                              {"bizId":3,"bizName":"3群"},
                              {"bizId":4,"bizName":"4群"},
                              {"bizId":5,"bizName":"5群"},
                              {"bizId":6,"bizName":"6群"},
                              {"bizId":7,"bizName":"7群"},
                              {"bizId":8,"bizName":"8群"},
                              {"bizId":9,"bizName":"9群"},
                              {"bizId":10,"bizName":"10群"},
                              {"bizId":11,"bizName":"11群"},
                              {"bizId":12,"bizName":"12群"},
                              {"bizId":13,"bizName":"13群"},
                              {"bizId":14,"bizName":"14群"},
                              {"bizId":15,"bizName":"15群"},
                              {"bizId":16,"bizName":"16群"},
                              {"bizId":17,"bizName":"17群"},
                              {"bizId":18,"bizName":"18群"},
                              {"bizId":19,"bizName":"19群"},
                              {"bizId":20,"bizName":"20群"},
                              {"bizId":21,"bizName":"21群"},
                              {"bizId":1000,"bizName":"其他群"}],
                 "approveList":[{"code":"PROVINCIAL_AGENT","description":"上级这条线上最近的省代","sequence":1},
                                {"code":"SECOND_AGENT","description":"上级这条线上最近的二级","sequence":2}],
                 "approveIncludeSelf":True}

json_apply = {"activityId":"86",
              "addressDetail":"131313131313",
              "provinceId":"130000",
              "provinceName":"河北省",
              "cityId":"130400",
              "cityName":"邯郸市",
              "countyId":"130423",
              "countyName":"临漳县",
              "receiverName":"tester",
              "receiverPhone":"13444444444",
              "expressAmount":3,
              "totalAmount":341,
              "skus":[
                  {"goodsId":13,"goodsImg":"https://img.alicdn.com/imgextra/i1/4009987183/O1CN01uobtcz22vrYHmEvV1_!!0-item_pic.jpg","goodsName":"防晒小晶钻","price":180,"quantity":1,"quantityOptional":False,"skuId":13},
                  {"goodsId":1,"goodsImg":"http://qiniu-dev.yjdfmall.com//Public/Uploads/ueditor/php/upload/image/Common/20200416/1587016974147277.jpg","goodsName":"商品1号","price":8,"quantity":1,"quantityOptional":False,"skuId":1},
                  {"goodsId":9,"goodsImg":"http://qiniu-uat.yjdfmall.com//Public/Uploads/ueditor/php/upload/image/Common/20200703/1593747815717914.jpg","goodsName":"姬存希轻透炫彩气垫BB霜（1+1）","price":150,"quantity":1,"quantityOptional":False,"skuId":9}
              ]
              }

json_agree ={
    "activityId":"107",
    "applyUserId":"46087",
    "applyNumbers":1
             }

json_Two={
    "activityId":"141",
    "applyUserId":"46086",
    "applyNumbers":1
    }
json_generate = {
    "activityId":"143",
    "totalUserNum":1
}

json_page = {"status":"","pageNo":1,"pageSize":10}

json_saveVoucher = {
    "id":"89",
    "voucherList":["http://yjdf-oss-uat.oss-cn-shanghai.aliyuncs.com/uat/2020/7/31/veer-151707721.jpg"]
}

json_operate = {"type":1,"orderIdList":[93]}
json_operate['orderIdList'][0]=88
