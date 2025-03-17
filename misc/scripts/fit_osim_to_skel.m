%% CREATE AN OPENSIM MODEL THAT IS SCALED AND POSED ACCORDING TO SKEL JOINTS

% The first section scales and poses the input OSIM model according to
% input locations of SKEL joints. The second section then, using the scaled
% and posed OSIM model, writes its bone structure and hierarchy to file so
% that it can be used in Blender to generate the armature inside the SKEL
% skin mesh.

% Because the OpenSim models are fitted to SKEL poses, the OpenSim models
% are not in their original default poses, and (assumedly) the transforms
% of bodies vary. Hence, the bones generated in Blender for rotating and
% transforming the bodies have wrong coordinate axes unless rotated. To
% solve this, the second section reads bone rotations in Ground and saves
% them, and they are then used in Blender to rotate the tails of bones in
% the Blender armature.

clc;clear;close all;
import org.opensim.modeling.*

% path to the outputs of the SKEL model
path_skel = 'C:\Users\JohnDoe\Documents\Godosim-assets\skel_outputs';

path_opensim_configs = 'C:\Users\JohnDoe\Documents\Godosim-assets\opensim_configs';
path_opensim_models = 'C:\Users\JohnDoe\Documents\Godosim-assets\opensim_models';

model_name = 'Hamner';

cd(path_skel)
bone_name_file = fopen('bone_names.txt','r');
bone_names = textscan(bone_name_file,'%s');
bone_names = bone_names{1};
fclose(bone_name_file);
    
% read joint translations (obtained from SKEL) into a matrix that will later be used to scale and fit the OpenSim model
joint_translation_files = dir('joint_translations_*');
joint_translation_files = {joint_translation_files(:).name};

for i_morphology = 1:numel(joint_translation_files)

    clearvars -except path_* i_morphology joint_translation_files bone_names model_name
    
    cd(path_skel)

    current_joint_translation_file = joint_translation_files{i_morphology};
    % get the name of current morphology, e.g., "female_plus_2"
    morphology_name = extractBefore(extractAfter(current_joint_translation_file,'joint_translations_'),'.txt');

    joint_translations = readmatrix(current_joint_translation_file);
    
    % add pinky and index markers
    hand_r_location = joint_translations(find(strcmp(bone_names,'hand_r')),:);
    index_finger_r = hand_r_location + [-0.1, 0, 0.03];
    pinky_finger_r = hand_r_location + [-0.1, 0, -0.03];
    hand_l_location = joint_translations(find(strcmp(bone_names,'hand_l')),:);
    index_finger_l = hand_l_location + [0.1, 0, 0.03];
    pinky_finger_l = hand_l_location + [0.1, 0, -0.03];

    % organize joint translations into a struct where each joint has a field
    joint_translations_struct = struct();
    joint_translations_struct.time = [0.0; 0.1];
    for i_label = 1:numel(bone_names)
        current_label = bone_names{i_label};
        joint_translations_struct.(current_label) = [repmat(joint_translations(i_label,:),2,1)];
    end

    joint_translations_struct.index_finger_r = repmat(index_finger_r,2,1);
    joint_translations_struct.pinky_finger_r = repmat(pinky_finger_r,2,1);
    joint_translations_struct.index_finger_l = repmat(index_finger_l,2,1);
    joint_translations_struct.pinky_finger_l = repmat(pinky_finger_l,2,1);

    % rotate joint translations, if necessary, because OpenSim and SKEL global axes are aligned differently
    % this rotation matrix rotates points 90 degrees around the vertical axis (y-axis)
    R = [0, 0, 1;
         0, 1, 0;
         -1, 0, 0];
    marker_names = fieldnames(joint_translations_struct);
    for i_markers = 2:numel(marker_names)
        joint_translations_struct.(marker_names{i_markers}) = [R*joint_translations_struct.(marker_names{i_markers})']';
    end

    % construct a time series file mimicking marker trajectory TRC of SKEL joint translations
    
    tst = osimTableFromStruct(joint_translations_struct);
    tst.addTableMetaDataString("DataRate","100.00");
    tst.addTableMetaDataString("Units","m");
    tst.addTableMetaDataString("OrigDataStartFrame","1")

    cd(path_opensim_configs)

    TRCFileAdapter().write(tst,'marker_trajectories.trc');

    % scale model
    cd(path_opensim_configs)
    
    % load the scale tool from setup file and run it
    scale_tool = ScaleTool(fullfile(path_opensim_configs,['scale_setup_' model_name '.xml']));
    scale_tool.run();

    % this generated two important files: scale factors and static pose IK,
    % which we still have to apply on the model

    % load the scaled model (which is still in original default pose)
    scaled_model = Model([model_name '_Godosim_scaled_step_2.osim']);
    % load IK pose from the IK marker task part of scaling
    static_pose = TimeSeriesTable('static_pose.mot');
    static_pose_struct = osimTableToStruct(static_pose);
    fns = fieldnames(static_pose_struct);
    column_labels = static_pose.getColumnLabels();

    % loop through labels in the IK file to get names of coordinates and their default values
    keys = {};
    values = [];
    for i_label = 0:column_labels.size()-1
        current_column_label = char(column_labels.get(i_label));
        if startsWith(current_column_label,'/jointset/') && endsWith(current_column_label,'value')
            slashes = strfind(current_column_label,'/');
            coordinate_name = current_column_label(slashes(end-1)+1:slashes(end)-1);
            coordinate_value = static_pose_struct.(fns{i_label+1});
            keys{numel(keys)+1} = coordinate_name;
            values = [values; coordinate_value];
        end
    end

    % construct a dictionary of coordinate names and their values
    coordinate_values = dictionary(keys',values);


    model = Model([model_name '_Godosim_scaled_step_2.osim']);
    coordinate_set = model.updCoordinateSet();
    n_coordinates = coordinate_set.getSize();
    % loop through model coordinates and assign the values as default values
    for i = 0:n_coordinates-1
        coordinate = coordinate_set.get(i);
        name = coordinate.getName();
        value = coordinate_values(name);
        coordinate.set_default_value(value);
    end

    % print the final scaled and posed model
    model.print([model_name '_Godosim_scaled_step_3.osim']);

    % rename marker trajectory files according to morphology
    movefile('marker_trajectories.trc', ['marker_trajectories_' morphology_name '.trc'])
    % finally, move the final scaled and posed model to the correct folder
    % and remove other models
    movefile([model_name '_Godosim_scaled_step_3.osim'], ['../opensim_models/Godosim_' model_name '_' morphology_name '.osim']);
    delete *_Godosim_scale_factors.xml *_Godosim_scaled_step_1.osim *_Godosim_scaled_step_2.osim static_pose.mot 
    

end


%% SECTION 2: PARSE THE NEWLY CREATED OPENSIM MODELS

clc;clear;close all;
import org.opensim.modeling.*
% path to the BSM OpenSim model
path_models = 'C:\Users\JohnDoe\Documents\Godosim-assets\opensim_models';
% path to the outputs of the SKEL model
path_skel = 'C:\Users\JohnDoe\Documents\Godosim-assets\skel_outputs';

cd(path_skel)
bone_name_file = fopen('bone_names.txt','r');
bone_names = textscan(bone_name_file,'%s');
bone_names = bone_names{1};
fclose(bone_name_file);

model_name = 'Hamner';

% read bone scales (obtained from SKEL) into a matrix that will later be used to scale the BodySet of the OpenSim Model object
bone_scale_files = dir('bone_scales_*');
bone_scale_files = {bone_scale_files(:).name};



for i_morphology = 1:numel(bone_scale_files)

    clearvars -except path_* i_morphology bone_scale_files bone_scale_files bone_names model_name
    
    cd(path_skel)

    current_scale_file = bone_scale_files{i_morphology};
    morphology_name = extractBefore(extractAfter(current_scale_file,'bone_scales_'),'.txt');


    body_positions_in_ground = containers.Map;
    body_rotations_in_ground = containers.Map;
    
    
    model = Model(fullfile(path_models,['Godosim_' model_name '_' morphology_name '.osim']));
    s = model.initSystem();
    % get a value type BodySet and its size
    body_set = model.getBodySet();
    n_bodies = body_set.getSize();
    % initialize an array of the names of bodies, and add ground (which technically isn't a body, but is part of the model)
    body_names = {"ground"};

    % for each body in the model, get its name and position and rotation in ground
    for i = 0:n_bodies-1
        body = body_set.get(i);
        name = string(body.getName());
        body_names = {body_names{:}, string(name)};
        body_position_in_ground = body.getPositionInGround(s);
        body_positions_in_ground(name) = [body_position_in_ground.get(0), body_position_in_ground.get(1), body_position_in_ground.get(2)];
        body_rotation_in_ground = body.getRotationInGround(s);
        body_rotations_in_ground(name) = [body_rotation_in_ground.get(0,0), body_rotation_in_ground.get(0,1), body_rotation_in_ground.get(0,2), ...
             body_rotation_in_ground.get(1,0), body_rotation_in_ground.get(1,1), body_rotation_in_ground.get(1,2), ...
             body_rotation_in_ground.get(2,0), body_rotation_in_ground.get(2,1), body_rotation_in_ground.get(2,2)];
        disp(['Body: ', char(name)])
        disp(['   Position : ' char(body_position_in_ground)])

    end
    
    
    % get joints and their parents and children
    
    origins_joint = containers.Map;
    
    % get a value type JointSet and the number of joints from the model
    joint_set = model.getJointSet();
    n_joints = joint_set.getSize();
    % initialize an array of joint names
    joint_names = {};
    % initialize dictionaries that will map joint names (key) to the joints' parent body names (value)
    joint_to_body = configureDictionary('string','string');
    % and similarly, names of child bodies of joints (key) to the names of joints (value)
    body_to_joint = configureDictionary('string','string');
    
    % for each coordinate in the model, get its name, range, whether it's locked, and default value
    for i = 0:n_joints-1
        joint = joint_set.get(i);
        name = string(joint.getName());
        joint_names = {joint_names{:}, name};
        parent_frame = joint.getParentFrame();
        child_frame = joint.getChildFrame();
    
        parent_body_name = string(parent_frame.getPropertyByName('socket_parent').toString());
        parent_body_name = split(parent_body_name,'/');
        parent_body_name = parent_body_name(end);
        child_body_name = string(child_frame.getPropertyByName('socket_parent').toString());
        child_body_name = split(child_body_name,'/');
        child_body_name = child_body_name(end);
    
        parent_in_ground = parent_frame.getPositionInGround(s);
        child_in_ground = child_frame.getPositionInGround(s);
    
        disp(['Joint: ', char(name)])
        disp(['   Parent: ' char(parent_frame.getName())])
        disp(['   Child: ' char(child_frame.getName())])
        disp(['   Parent position: ' char(parent_in_ground)])
        disp(['   Child position: ' char(child_in_ground)])
    
    
        joint_to_body(name) = parent_body_name;
        body_to_joint(child_body_name) = name;
        %joint_to_parent(name) = parent_body_name;
        %joint_to_child(name) = child_body_name;
    
        origins_joint(name) = [child_in_ground.get(0), child_in_ground.get(1), child_in_ground.get(2)];
    
    end
    
    
    
    %%
    
    % calculate hierarchy
    btj = entries(body_to_joint);
    jtb = entries(joint_to_body);
    hierarchy = dictionary([btj{:,1}; jtb{:,1}], [btj{:,2}; jtb{:,2}]);
    
    parents = values(joint_to_body);
    joints = keys(joint_to_body);
    
    bone_endpoints = containers.Map;
    
    % calculate Blender bone end points (heads and tails)
    for i = 1:n_bodies+1
        current_body_name = body_names{i};
        
        % find parent joint and child joints, first parent joint
        parent_joint = [];
        try
            parent_joint = body_to_joint(current_body_name);
        catch
            parent_joint = [];
        end
        % then child joints
        child_joints = [];
        for j = 1:numel(parents)
            if strcmp(parents(j), current_body_name)
                child_joints = [child_joints; joints(j)];
            end
        end
    
        num_child_joints = numel(child_joints);
        disp(strjoin(['Body ', current_body_name, ' has ', num2str(num_child_joints), ' children and ', num2str(numel(parent_joint)), ' parents']))
    
    
        % if the body has no parent, the head is (0,0,0)
        if numel(parent_joint) == 0
            head = [0, 0, 0];
        else
            head = origins_joint(parent_joint);
        end
        
        % if the body has no children, set the tail 10 cm superior to the head
        if numel(child_joints) == 0
            tail = [head(1), head(2)+0.1, head(3)];
        % if the body has several children, set the tail 10 cm inferior to
        % the head OR to the mean position of two of its child joints, whichever results in a greater head-to-tail distance
        elseif num_child_joints > 1
            tail = [head(1), head(2)-0.1, head(3)];
            combinations = nchoosek(1:num_child_joints,2);
            for i_perm = 1:height(combinations)
                current_combination = combinations(i_perm,:);
                mean_tail = mean([origins_joint(child_joints(current_combination(1))); origins_joint(child_joints(current_combination(2)))]);
                if norm(mean_tail-head) > norm(tail-head)
                    tail = mean_tail;
                end
            end
        % otherwise, set the tail as the position of the child joint
        elseif numel(child_joints) == 1
            tail = origins_joint(child_joints(1));
        end
    
        headtail = containers.Map({'head', 'tail'}, {head, tail});
    
        bone_endpoints(current_body_name) = headtail;

        %if strcmp(current_body_name,'femur_r')
        %    w=waitforbuttonpress;
        %end
    
    end
    
    %% save files
    
    cd('C:\Users\JohnDoe\Documents\Godosim-assets\matlab_outputs')
    
    bone_rotations_json = jsonencode(body_rotations_in_ground, 'PrettyPrint', true);

    bone_endpoints_json = jsonencode(bone_endpoints, 'PrettyPrint', true);
    hierarchy_json = jsonencode(containers.Map(keys(hierarchy), values(hierarchy)), 'PrettyPrint', true);
    origins_joint_json = jsonencode(origins_joint, 'PrettyPrint', true);
    
    fid = fopen(['bone_endpoints_' morphology_name '.json'],'w');
    fprintf(fid,'%s',bone_endpoints_json);
    fclose(fid);
    
    fid = fopen(['hierarchy.json'],'w');
    fprintf(fid,'%s',hierarchy_json);
    fclose(fid);
    
    fid = fopen(['translations_global_' morphology_name '.json'],'w');
    fprintf(fid,'%s',origins_joint_json);
    fclose(fid);

    fid = fopen(['bone_rotations_' morphology_name '.json'],'w');
    fprintf(fid,'%s',bone_rotations_json);
    fclose(fid);
    
end

