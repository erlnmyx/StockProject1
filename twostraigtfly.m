clear
clc
namelist  = ls('D:\database\dayK_yes\*.txt');
info = importdata('D:\database\extrainfo.txt');
txtnameS=namelist(:,1:6);   %ȡtxt�ļ����ַ���ǰ6λ�����룩
txtnameD=str2num(txtnameS);  %��stringתdouble
