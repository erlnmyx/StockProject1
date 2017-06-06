clear
clc
input=importdata(fullfile('D:','database','input2.txt'));
%input每列含义： 代码\股票名称\交易日期\交易时间\买入价格\买入数量\买入金额\卖出价格\卖出数量\卖出金额
namelist  = ls('D:\database\dayK_no\*.txt');
txtnameS=namelist(:,1:6);   %取txt文件名字符串前6位（代码）
txtnameD=str2num(txtnameS);  %把string转double
L1=length(input);
for i=1:L1
    if input(i,4)==0 %区分买入和卖出，买入的mark==0,卖出的mark==1
        mark(i)=1;
        continue
    end
    position1=find(input(i,1)==txtnameD);  %找到对应的股票文件名
    A1=importdata(fullfile('D:','database','dayK_no',namelist(position1,:))); %导入对应股票的数据
    position2=find(input(i,2)==A1(:,1)); %找到对应的股票的交易日期
    if input(i,4)>=A1(position2,4) && input(i,4)<=A1(position2,3) %交易价是否在当天最高价和最低价之间，纠错用
        flag(i)=0;
    else
        flag(i)=1;
    end
end
