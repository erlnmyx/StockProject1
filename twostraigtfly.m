clear
clc
namelist  = ls('D:\database\dayK_yes\*.txt');
info = importdata('D:\database\extrainfo.txt');
txtnameS=namelist(:,1:6);   %取txt文件名字符串前6位（代码）
txtnameD=str2num(txtnameS);  %把string转double
