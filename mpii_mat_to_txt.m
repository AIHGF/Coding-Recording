
clear
load('./mpii_human_pose_v1_u12_1/mpii_human_pose_v1_u12_1.mat');

%dlmwrite('a.txt',a,'-append','delimiter', '');

annName = {'PELVIS','THORAX','NECK','HEAD','R_ANKLE','R_KNEE','R_HIP','L_HIP','L_KNEE','L_ANKLE','R_WRIST','R_ELBOW','R_SHOULDER','L_SHOULDER','L_ELBOW','L_WRIST'};
annID = [6,7,8,9,0,1,2,3,4,5,10,11,12,13,14,15];
count = 0;
for j = 1:length(RELEASE.annolist)
    if isfield((RELEASE.annolist(j).annorect),'annopoints')&&length(RELEASE.annolist(j).annorect)==1
        
        ImageData = RELEASE.annolist(j).annorect.annopoints.point;
        PoseData = [];
        for i = 1:length(ImageData)
            id = ImageData(i).id;
            if find(annID == id)
                tempData = [num2str(ImageData(i).x),',',num2str(ImageData(i).y)];
                jointName = char(annName(i));
                jointName = ['"',jointName,'"'];
                temp =[jointName,': [',tempData,'], '];
                PoseData = [PoseData, temp];
            end
        end
        PoseData = PoseData(1:end-2);
        imageName = RELEASE.annolist(j).image.name;
        imageNameAndData = [imageName,'|{',PoseData, '}'];
        dlmwrite('mpii.txt',imageNameAndData,'-append','delimiter', '');
        
        count = count+1
    end
end

