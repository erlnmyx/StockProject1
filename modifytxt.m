clear
clc
% namelist  = dir('D:\database\1_yes\*.txt');                             % 读取并储存所有数据文件名
% %namelist  = dir('D:\database\1_no\*.txt'); 
% total = length(namelist);
%  for i=1:total
%     txtname{i}=namelist(i).name;
%     fidin=fopen(fullfile('D:','database','1_yes',txtname{i}));          % 打开txt文件   
%     %fidin=fopen(fullfile('D:','database','1_yes',txtname{i}));
%     fidout=fopen(fullfile('D:','database','dayK_yes',txtname{i}),'w');  % 创建新txt文件
%     %fidout=fopen(fullfile('D:','database','dayK_yes',txtname{i}),'w')
%     while ~feof(fidin)                                                  % 判断是否为文件末尾               
%         tline=fgetl(fidin);                                             % 从文件读行   
%         if double(tline(1))>=48&&double(tline(1))<=57                   % 判断首字符是否是数值
%            fprintf(fidout,'%s\n\n',tline);                              % 如果是数字行，把此行数据写入txt文件
%            continue                                                     % 如果是非数字继续下一次循环
%         end
%     end
%     fclose('all');
%  end