# SmartBuilding

* floor_5_step.py用来对5层每个房间做阶跃响应，主要执行的步骤是：把所有房间风阀开度设置为70，过五个小时后风阀开度阶跃到80，再过五个小时程序终止。记录的数据保存在floor_5_step文件夹中。
* daily_temp_record.py用来记录6层每个房间全天的温度变化。1、2、3号房间风阀开度设置为100；4、5、6设置为60；7、8、9设置为30；10、11、12设置为10。记录的数据保存在daily_temp_record文件夹中。
* PIDControl.py用来对5层所有房间进行PID控制。记录的数据保存在control_record文件夹中。
* auto-plot.py用于对上述三个文件夹内的数据进行可视化绘图。设置为每10分钟更新一次，绘制的图表保存在realtime_figure文件夹内。