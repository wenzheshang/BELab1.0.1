import numpy as np
import matplotlib.pyplot as plt

from fluent_corba import CORBA

import numpy as np
import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
import tkinter as tk
import time
import pathlib
import os, sys
import subprocess
import shutil
import csv

#print('hello world')
# 获取根目录，定义Fluent工作目录
now_time = time.strftime('%Y-%m-%d_%H-%M', time.localtime())
cur_path =  os.path.abspath(os.path.dirname(__file__))
root_path = cur_path
workPath =pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time)
r1wp = pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time+"/room1")#r1wp means room1 workpath
r2wp = pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time+"/room2")#r2wp means room2 wprkpath
folder1 = os.path.exists(workPath)
folder2 = os.path.exists(r1wp)
folder3 = os.path.exists(r2wp)
if not folder1:
    os.makedirs(pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time))
if not folder2:
    os.makedirs(r1wp)
if not folder3:
    os.makedirs(r2wp)

#定义Modelica工作目录
dir_result =root_path+"/Workdata/Dymola_python/"+now_time
folder = os.path.exists(dir_result)
if not folder:
    os.makedirs(dir_result)

# 清除之前存在的aaS*.txt文件
aasFilePath = workPath/"aaS_FluentId.txt"
for file in workPath.glob("aaS*.txt"):
    file.unlink()

#fluent设置
root_name = ["AWP_ROOT222","AWP_ROOT221","AWP_ROOT212","AWP_ROOT211","AWP_ROOT202","AWP_ROOT201","AWP_ROOT192","AWP_ROOT191",
                "AWP_ROOT182","AWP_ROOT181","AWP_ROOT172","AWP_ROOT171","AWP_ROOT162","AWP_ROOT161","AWP_ROOT152","AWP_ROOT151"]
fluent_exist = False
for rn in root_name:
    env_exist = os.getenv(rn,'null')
    if env_exist != 'null':
        ansysPath = pathlib.Path(os.environ[str(rn)])
        fluent_exist = True
        break

fluentExe = str(ansysPath/"fluent"/"ntbin"/"win64"/"fluent.exe")

# 启动Fluent软件,使用-hidden可以隐藏fluent的GUI界面
if fluent_exist:
    fluentProcess = subprocess.Popen(f'"{fluentExe}" 3ddp -aas', shell=True, cwd=str(workPath))#-hidden
else:
    error = 'no right fluent verison exist on this machine'
    starterror =  open(os.path.join(workPath,'startError.txt'),'w')
    starterror.write(error)
    starterror.close()
    sys.exit()

# 监控aaS_FluentId.txt文件生成，等待corba连接
while True:
    try:
        if not aasFilePath.exists():
            time.sleep(0.2)
            continue
        else:
            if "IOR:" in aasFilePath.open("r").read():
                break
    except KeyboardInterrupt:
        sys.exit()
# 初始化orb环境
orb = CORBA.ORB_init()
# 获得Fluent实例单元
fluentUnit = orb.string_to_object(aasFilePath.open("r").read())
scheme = fluentUnit.getSchemeControllerInstance()

Filepath = 'F:/Thinking/CFD_study/case3/case3_files/dp0/FFF/Fluent/FFF-10.cas' #'F:/Thinking/mesh/vadilation/roomesh.msh' 
scheme.execScheme(f'(read-case "{Filepath}")')#?
print('1')
#scheme.execScheme("/file/read-cas "+str(cas_loc))


#可以把这里做成一个class的形式，进行调用，或者干脆也集成到main里面

# Tstart = 0 # The start time.
# Tend = 500

# model = load_fmu('FMU/Buildings_EasyPressure_EasyPressure.fmu')

# # res = model.simulate(final_time = 100)
# # x1 = res['CFD_roo.heaPorAir.T']
# # t = res['time']
# # plt.plot(t, x1)
# # plt.show()

# # result_dict = model.get_model_variables()
# # result = list(result_dict.keys())
# # print(result[0:10])
# # ms =  open(('FMU/variable_list.txt'),'w')

# model.set(['fixedTemperature.T'], [298.15])
# model.setup_experiment(start_time = Tstart) # Set the start time to Tstart
# model.enter_initialization_mode()
# model.exit_initialization_mode()
# eInfo = model.get_event_info()
# eInfo.newDiscreteStatesNeeded = True
# #Event iteration
# # while eInfo.newDiscreteStatesNeeded == True:
# #     model.enter_event_mode()
# #     model.event_update()
# #     eInfo = model.get_event_info() #这一部分似乎没啥用处

# model.enter_continuous_time_mode()

# # Get Continuous States
# x = model.continuous_states
# # Get the Nominal Values
# x_nominal = model.nominal_continuous_states
# # Get the Event Indicators
# event_ind = model.get_event_indicators()
# # dt = 0.1
# # Tnext = Tend
# # time = Tstart
# # number = 0
# # communicate_time = 100


# # while time < Tend and not model.get_event_info().terminateSimulation:
# #         #set progress bar
# #         #Compute the derivative of the previous step f(x(n), t(n))
# #         dx = model.get_derivatives()
        
# #         # Advance
# #         h = min(dt, Tnext-time)
# #         time = time + h
        
# #         # Set the time
# #         model.time = time
        
# #         # Set the inputs at the current time (if any)
# #         #model.set(vref, value)
        
# #         # Set the states at t = time (Perform the step using x(n+1)=x(n)+hf(x(n), t(n))
# #         # x = x + h*dx 
# #         # model.continuous_states = x
# #         event_ind_new = model.get_event_indicators()
                
# #         # Inform the model about an accepted step and check for step events
# #         step_event = model.completed_integrator_step()
        
# #         # Check for time and state events
# #         time_event = abs(time-Tnext) <= 1.e-10
# #         state_event = True if True in ((event_ind_new>0.0) != (event_ind>0.0)) else False


# #         if step_event or time_event or state_event:
# #                 model.enter_event_mode()
# #                 eInfo = model.get_event_info()
# #                 eInfo.newDiscreteStatesNeeded = True

# #                 if number >= communicate_time:
# #                    a = model.get_real([model.get_variable_valueref('SupplyAirVelocity')])[0]
# #                    b = 1

# #                 number = number + 0.01

# # Values for the solution
# # Retrieve the valureferences for the values 'CFD_roo.Room_MeanT'

# # vref = [model.get_variable_valueref('ori3.dp')]+ \
# #      [model.get_variable_valueref('returnR.m_flow')]
# t_sol = [Tstart]
# #sol = [model.get_real(vref)]
# #a = model.get_real(vref)#[0]
# time = Tstart
# Tnext = Tend # Used for time events
# dt = 0.001
# #value = {1:283.15,-1:303.15}
# #iii = 1
# number = 0

# while time < Tend and not model.get_event_info().terminateSimulation:
#     #Compute the derivative of the previous step f(x(n), t(n))
#     dx = model.get_derivatives()
    
#     # Advance
#     h = min(dt, Tnext-time)
#     time = time + h
    
#     # Set the time
#     model.time = time
    
#     # Set the inputs at the current time (if any)
#     #model.set(vref, value)
    
#     # Set the states at t = time (Perform the step using x(n+1)=x(n)+hf(x(n), t(n))
#     x = x + h*dx 
#     model.continuous_states = x

#     # Get the event indicators at t = time
#     event_ind_new = model.get_event_indicators()
    
#     # Inform the model about an accepted step and check for step events
#     step_event = model.completed_integrator_step()
    
#     # Check for time and state events
#     time_event = abs(time-Tnext) <= 1.e-10
#     state_event = True if True in ((event_ind_new>0.0) != (event_ind>0.0)) else False

#     # Event handling
#     if step_event or time_event or state_event:
#         model.enter_event_mode()
#         eInfo = model.get_event_info()
#         eInfo.newDiscreteStatesNeeded = True

#         if number >= 100:
#             a = model.get_real([model.get_variable_valueref('ori3.dp')])[0]
#             b = 1
#             number = 0

#         number = number + 0.001

#         # Event iteration
#         while eInfo.newDiscreteStatesNeeded:
#             model.event_update('0') # Stops at each event iteration
#             eInfo = model.get_event_info()
#         # Retrieve solutions (if needed)
#     if eInfo.newDiscreteStatesNeeded:
#         pass
    
#     # Check if the event affected the state values and if so sets them
#     if eInfo.valuesOfContinuousStatesChanged:
#         x = model.continuous_states
    
#     # Get new nominal values.
#     # if eInfo.nominalsOfContinuousStatesChanged:
#     #     atol = 0.01*rtol*model.nominal_continuous_states
    
#     # Check for new time event
#     if eInfo.nextEventTimeDefined:
#         Tnext = min(eInfo.nextEventTime, Tend)
#     else:
#         Tnext = Tend
#     model.enter_continuous_time_mode()

#     event_ind = event_ind_new

#     # Retrieve solutions at t=time for outputs
#     # bouncing_fmu.get_real,get_integer,get_boolean,get_string (valueref)

# #     t_sol += [time]
# #     sol += [model.get_real(vref)]


# # # model.get_model_variables()
# # # res = model.simulate(final_time=720)
# # # t = res['time']
# # # x1 = res['SupplyAir.T_in']
# # plt.subplot(211)
# # plt.plot(t_sol,np.array(sol)[:,0])
# # plt.subplot(212)
# # plt.plot(t_sol,np.array(sol)[:,1])
# # plt.show()


# dir_result = 'F:\\Thinking\\modelica+CFD\\Vadilation'
# result_path = os.path.join(dir_result,'vadilation.mat')
# r = Reader(result_path,'dymola')
# (time,RoomMeanT) = r.values('CFD_roo.air.heaPorAir.T')
# (time_2,SupplyT) = r.values('SupplyAir.T_in')
# mydataframe = pd.DataFrame({'time_roo':time, 'RoomMeanT':RoomMeanT, 'time_Sup':time_2, 'SupplyT': SupplyT})
# mydataframe.to_csv(os.path.join(dir_result, 'data/result.csv'))
# signal_simu_time = [1]
# dymola = DymolaInterface()
# smash_signal = [0]


# def simulate(value, name):

#     dir_result = 'F:\\Thinking\\modelica+CFD\\Vadilation\\data'
#     result_path = os.path.join(dir_result,'vadilation.mat')
#     modelicaPath = pathlib.Path(os.environ["DymolaPath"])
#     #Library import
#     dirBuilding = os.path.join(modelicaPath,"Modelica/Library/Buildings-v8.0.0/Buildings 8.0.0")
#     #open Library
#     dymola.openModel(path=os.path.join(dirBuilding, 'package.mo'))
#     dymola.openModel(path='F:\\Thinking\\modelica+CFD\\Vadilation\\Vadilation.mo')
#     problemName = 'Vadilation.vadilation'#'Plant.plant_rectify_0105_correct'
#     ResultValue = []
#     demo_name = 'demo_results'+str(signal_simu_time[0])
#     (dymola_setName, dymola_setValue) = fluent_to_dymola(value, name)
#     print(dymola_setName, dymola_setValue)
#     try:
#         result = dymola.simulateExtendedModel(
#                     problem= problemName,
#                     startTime=0,
#                     stopTime=180,
#                     numberOfIntervals=0,
#                     outputInterval=0.0,
#                     method="Dassl",
#                     tolerance=0.0001,
#                     fixedstepsize=0.0,
#                     resultFile=os.path.join(dir_result,demo_name),
#                     initialNames=dymola_setName,
#                     initialValues=dymola_setValue,
#                     autoLoad=True
#                     )
#     except:
#         print('error')
#         log = dymola.getLastError()
#         f =  open(os.path.join(dir_result,'error.txt'),'w')
#         f.write(log)
#         f.close()
#         return
#     result_path = os.path.join(dir_result,demo_name+'.mat')
#     r = Reader(result_path,'dymola')

#     result_name = 'reslut'+str(signal_simu_time[0])
#     signal_simu_time[0] = signal_simu_time[0] + 1

#     ResultVarName = r.varNames() #获取所有结果变量名
#     for i in range(len(ResultVarName)):
#         (t,r_ser) = r.values(ResultVarName[i])
#         ResultValue.append(r_ser[-1])
#     mydataframe = pd.DataFrame({'VarName':ResultVarName,'Value':ResultValue})
#     mydataframe.to_csv(os.path.join(dir_result, result_name+'.csv'))#将所有结果保存到.csv文件中，以备下次读取

# def fluent_to_dymola(value, name):
#     Exchange_data_value = [value]
#     Exchange_data_name = [name]
#     return Exchange_data_name, Exchange_data_value

# for i in range(5):
#     value = 283.15+10*i
#     name = 'CFD_roo.Room_MeanT'
#     simulate(value, name)



# dymola = DymolaInterface()
# ResultValue = []

# result_path = 'C:\\Users\\Administrator\\Desktop\\result.csv'
# Exchange_data_name = []
# Exchange_data_value = []
# with open(result_path) as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:      
#         Exchange_data_name.append(row['VarName'])
#         Exchange_data_value.append(float(row['Value']))#将csv中结果读入列表

# modelicaPath = pathlib.Path(os.environ["DymolaPath"])
# #Library import
# dirBuilding = os.path.join(modelicaPath,"Modelica/Library/Buildings-v8.0.0/Buildings 8.0.0")
# #open Library
# dymola.openModel(path=os.path.join(dirBuilding, 'package.mo'))
# dymola.openModel(path='F:/Thinking/modelica+CFD/Plant.mo')
# problemName = 'Plant.plant_rectify_0105_correct'#'vadilation'


# dymola_setName = Exchange_data_name
# dymola_setValue = Exchange_data_value
# endT = 1800
# intervals = 10
# step_time = endT/intervals


# result = dymola.simulateExtendedModel(
#     problem= problemName,
#     startTime=0,
#     stopTime=step_time,
#     numberOfIntervals=0,
#     outputInterval=0.0,
#     method="Dassl",
#     tolerance=0.0001,
#     fixedstepsize=0.0,
#     resultFile=os.path.join('/test_result','demo_results'),
#     initialNames=dymola_setName,
#     initialValues=dymola_setValue,
#     autoLoad=True
#     )

# status = result[0]
# if not status:
#     print('error')
#     log = dymola.getLastError()
#     f =  open(os.path.join('C:\\Users\\Administrator\\Desktop\\error.txt'),'w')
#     f.write(log)
#     f.close()

# else:
#     #成功模拟后输出结果部分,加保存excel功能
#     #以下代码保存excel文件
#     result_path = os.path.join('/test_result','demo_results.mat')
#     r = Reader(result_path,'dymola')

#     result_name = 'reslut.csv'
    

#     ResultVarName = r.varNames() #获取所有结果变量名
#     for i in range(len(ResultVarName)):
#         (t,r_ser) = r.values(ResultVarName[i])
#         ResultValue.append(r_ser[-1])
#     mydataframe = pd.DataFrame({'VarName':ResultVarName,'Value':ResultValue})
#     mydataframe.to_csv(os.path.join('/test_result', result_name))#将所有结果保存到.csv文件中，以备下次读取