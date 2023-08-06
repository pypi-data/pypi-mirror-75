fastwork
========
致力于让你繁琐的工作自动化，让你有更多的精力和时间去提升自己的认知和影响力。
欢迎关注我的微信公众号：人文互联网。



安装
------------

    pip install china-district

依赖库
---------

`requests=2.22.0`

## 基础使用示例

基础使用，默认使用作者自己的高德地图开发者key，每天上限调用30万次。超过这个限制将无法使用。


    >>> In [1]: from china_district import District
    # 初始化District,默认只返回下一级行政区，不返回行政区边界坐标点
    >>> In [2]: d=District()
    
    >>> In [3]: d.get("武侯区")
    {'status': '1',
     'info': 'OK',
     'infocode': '10000',
     'count': '1',
     'suggestion': {'keywords': [], 'cities': []},
     'districts': [{'citycode': '028',
       'adcode': '510107',
       'name': '武侯区',
       'center': '104.05167,30.630862',
       'level': 'district',
       'districts': [{'citycode': '028',
         'adcode': '510107',
         'name': '金花桥街道',
         'center': '103.973,30.6029',
         'level': 'street',
         'districts': []},
    ……}
    # 将当前搜索结果(json对象)写入到当前目录，默认文件名"搜索关键词.json"
    >>> d.to_json("武侯区")
    	写入本地完成...

高级使用示例
------------------

``` d.get("武侯区")
>>> In [1]: from china_district import District
# 初始化District,key为高德地图开发者key,subdistrict设置显示下级行政区级数，extensions设置行政区信息中是否返回行政区边界坐标点，”base"不返回，“all"返回

>>> In [5]:d = District(key="182ad5d7061ed1e421091c22089c3677",subdistrict=3,extensions="all")

Out[6]: 
{'status': '1',
 'info': 'OK',
 'infocode': '10000',
 'count': '1',
 'suggestion': {'keywords': [], 'cities': []},
 'districts': [{'citycode': '028',
   'adcode': '510107',
   'name': '武侯区',
   'polyline': '103.949841,30.658586;103.949928,30.658864;103.950137,30.659044;103.950415,30.659121;103.950667,30.6591;103.952425,30.658587;103.952869,30.658525;103.95333,30.658589;103.953
687,30.658726;103.953966,30.658948;103.954261,30.659335;103.954984,30.660906;103.955149,30.661113;103.955472,30.661348;103.95575,30.661423;103.956107,30.661436;103.957439,30.661364;103.957……```}

```

## 请求参数说明




## 了解更多

高德地图行政区域查询接口：https://lbs.amap.com/api/webservice/guide/api/district

License
-------
Licensed under the MIT License.



