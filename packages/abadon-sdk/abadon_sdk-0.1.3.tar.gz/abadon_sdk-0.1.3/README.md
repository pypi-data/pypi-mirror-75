# Ｗeb可视化自启工具
**部署步骤**
```bash
cd ~
git clone https://gitlab.momenta.works/msquare/abadon
```

**启动步骤**
```bash
cd ~/abadon/script && source init.sh
```

**使用说明**

`注意：需自行确认 ros-dev 分支` 

![avatar](doc/1.png)


**以下为各步骤具体执行:**
###### pcstart
```bash
~/ros-dev/script/pcstart.sh
```

###### run_dev
```bash
~/ros-dev/script/run_dev.py clean &&  ~/ros-dev/script/run_dev.py pull_all update_all
```

###### repo_manager
```bash
repom -u you_username -p you_password --reset-hard
cd ~/catkin_ws/src/online_pipeline/lidar_common && ./gen_launch.py
```

###### 编译代码库
```bash
cd ~/boot
./clear_all.sh && ./build_all.sh
```

###### boot_diag
```bash
cd ~/boot
./boot_diag.sh
```

###### boot_all
```bash
cd ~/boot
./boot_all.sh
```

###### kill_all
```bash
cd ~/boot
./kill_all.sh
```