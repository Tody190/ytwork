call C:\Users\zhangwenfeng\Desktop\setenv.bat
call Y:\pipeline_studio\config\base_env_dev.bat

"C:\pipeline_user\rez-2.111.3-py3.10\rez.exe" env maya-2023 proj_as24y_stun-1.0 -- "C:\Program Files\Autodesk\Maya2023\bin\mayapy.exe" "D:\yangtao\ytwork\runner\wlf\as24y\batch_export_abc.py" %*

pause