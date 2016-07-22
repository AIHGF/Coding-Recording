function [DD_scale_adaption,DD_scale_fixed,ddparams] = dd_pose_read( )

annName = {'PELVIS','THORAX','NECK','HEAD','R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','R_WRIST','R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST'};
annID = [6,7,8,9,0,1,2,3,4,5,10,11,12,13,14,15]';%'

data = importdata('ddmpiipose.txt');
not_image = [ ];
m = 0; n=0;
for i = 1:numel(data)
    disp(['Processing the image: ', num2str(i)])

    temp = char(data(i,1));
    S1=regexp(temp,'.jpg','split');
    DD.annolist(i).image.name = [char(S1(1)),'.jpg'];
    
    DD.annolist(i).annorect.scale = 1;
    
    orig_img_names = [char(S1(1)),'.jpg'];
    
    cache_image = ['./dd_pose/' orig_img_names];
    if exist(cache_image, 'file')
        orig_img = imread(['./dd_pose/' orig_img_names]);
        m = m+1;
        m
    else
        not_image = [not_image, cache_image];
        n = n+1;
        n
    end
        
    
    DD.annolist(i).annorect.objpos.x = 0.5 * size(orig_img,2);
    DD.annolist(i).annorect.objpos.y = 0.5 * size(orig_img,1);

    %--------------------------------
    points_data = char(S1(2));
    points_data = points_data(3:end-1);
    S2 = regexp(points_data,'], "','split');
    joints_info = [];
    for j = 1:numel(S2)
    	S3 =regexp(S2(j),'": [','split');
    	joints_info = [joints_info; S3{1}];
    end
    trans_data{i} = joints_info;

    b = char(joints_info(1));
    b = b(2:end);
    trans_data{i}(1) = {b};

    c = char(joints_info(end));
    c = c(1:end-1);
    trans_data{i}(end) = {c};
    %--------------------------------
     
    d = trans_data{i};
    for s = 1:numel(annName)
	    for t = 1:size(d,1)
	        if isequal(annName(s),d(t,1))
                S4 =regexp(d(t,2),', ','split');
                dd_temp = str2num(char(S4{1,1}));
                DD.annolist(i).annorect.annopoints.point(s).x=dd_temp(1);
                DD.annolist(i).annorect.annopoints.point(s).y=dd_temp(2);
                  
                DD.annolist(i).annorect.annopoints.point(s).is_visible=1;
            end
        end
        DD.annolist(i).annorect.annopoints.point(s).id = annID(s);
    end   
end

DD.img_train = ones(1,numel(DD.annolist));

 %ddparams.train = [1:numel(DD.annolist)];
 %rtrain = randperm(numel(ddparams.train));
 %ddparams.val = rtrain(1:fix(numel(DD.annolist)/10));

DD_scale_fixed = DD;
save DD_scale_fixed DD_scale_fixed

%Scale
orig_img_names = [DD.annolist.image];
for h = 1:numel(orig_img_names)
    h
    
    for i=1:numel(DD.annolist(h).annorect)
        i
        ann = DD.annolist(h).annorect(i);
        
        for t = 1:numel(ann.annopoints.point)
            if isequal(ann.annopoints.point(t).id, 0)
                rankle.x = ann.annopoints.point(t).x;
                rankle.y = ann.annopoints.point(t).y;
            end
            if isequal(ann.annopoints.point(t).id, 5)
                lankle.x = ann.annopoints.point(t).x;
                lankle.y = ann.annopoints.point(t).y;
            end
            if isequal(ann.annopoints.point(t).id, 9)
                head.x = ann.annopoints.point(t).x;
                head.y = ann.annopoints.point(t).y;
            end
        end
        if ~isequal(rankle.y, [ ]) || ~isequal(lankle.y, [ ])
            %ankelx = max([rankle.x, lankle.x]);
            ankely = max([rankle.y, lankle.y]);
        else
            ankely = size(orig_img,1);
        end
        
        if ~isequal(head.y, [ ])
            DD.annolist(h).annorect.scale = abs(head.y - ankely)/200;
        else
            DD.annolist(h).annorect.scale = size(orig_img,1)/200;
        end
    end
end
DD_scale_adaption = DD;
%save DD_scale_adaption DD_scale_adaption ddparams
save DD_scale_adaption DD_scale_adaption
end
