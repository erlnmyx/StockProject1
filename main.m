clear
clc
input=importdata(fullfile('D:','database','input2.txt'));
%inputÿ�к��壺 ����\��Ʊ����\��������\����ʱ��\����۸�\��������\������\�����۸�\��������\�������
namelist  = ls('D:\database\dayK_no\*.txt');
txtnameS=namelist(:,1:6);   %ȡtxt�ļ����ַ���ǰ6λ�����룩
txtnameD=str2num(txtnameS);  %��stringתdouble
L1=length(input);
for i=1:L1
    if input(i,4)==0 %��������������������mark==0,������mark==1
        mark(i)=1;
        continue
    end
    position1=find(input(i,1)==txtnameD);  %�ҵ���Ӧ�Ĺ�Ʊ�ļ���
    A1=importdata(fullfile('D:','database','dayK_no',namelist(position1,:))); %�����Ӧ��Ʊ������
    position2=find(input(i,2)==A1(:,1)); %�ҵ���Ӧ�Ĺ�Ʊ�Ľ�������
    if input(i,4)>=A1(position2,4) && input(i,4)<=A1(position2,3) %���׼��Ƿ��ڵ�����߼ۺ���ͼ�֮�䣬������
        flag(i)=0;
    else
        flag(i)=1;
    end
end
