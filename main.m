clear
clc
input=importdata(fullfile('D:','database','input2.txt'));
% input formatting: 
% stock code/stock name/trade date/trade time/
% buying price/buying quantity/buying amount/
% selling price/selling quantity/selling amount
namelist  = ls('D:\database\dayK_no\*.txt');
txtnameS=namelist(:,1:6);       % first 6 letters of the name string
txtnameD=str2num(txtnameS);     % convert string to number
L1=length(input);
for i=1:L1
    if input(i,4)==0            % mark buying 0; selling 1
        mark(i)=1;
        continue
    end
    position1=find(input(i,1)==txtnameD);   % search corresponding stock name
    A1=importdata(fullfile('D:','database','dayK_no',namelist(position1,:))); % import corresponding data
    position2=find(input(i,2)==A1(:,1));    % search corresponding trade date
    if input(i,4)>=A1(position2,4) && input(i,4)<=A1(position2,3) % if transaction price between the highest and lowest, for correction purpose
        flag(i)=0;
    else
        flag(i)=1;
    end
end
