clear
clc
% namelist  = dir('D:\database\1_yes\*.txt');                             % ��ȡ���������������ļ���
% %namelist  = dir('D:\database\1_no\*.txt'); 
% total = length(namelist);
%  for i=1:total
%     txtname{i}=namelist(i).name;
%     fidin=fopen(fullfile('D:','database','1_yes',txtname{i}));          % ��txt�ļ�   
%     %fidin=fopen(fullfile('D:','database','1_yes',txtname{i}));
%     fidout=fopen(fullfile('D:','database','dayK_yes',txtname{i}),'w');  % ������txt�ļ�
%     %fidout=fopen(fullfile('D:','database','dayK_yes',txtname{i}),'w')
%     while ~feof(fidin)                                                  % �ж��Ƿ�Ϊ�ļ�ĩβ               
%         tline=fgetl(fidin);                                             % ���ļ�����   
%         if double(tline(1))>=48&&double(tline(1))<=57                   % �ж����ַ��Ƿ�����ֵ
%            fprintf(fidout,'%s\n\n',tline);                              % ����������У��Ѵ�������д��txt�ļ�
%            continue                                                     % ����Ƿ����ּ�����һ��ѭ��
%         end
%     end
%     fclose('all');
%  end