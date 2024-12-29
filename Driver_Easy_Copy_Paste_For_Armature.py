# Code written by Ferhan Hacısalihoğlu:
# This script retrieves the existing animation drivers of an armature (named "Armature") in Blender,
# and creates mirrored drivers for the right side by copying the left side (L) drivers and adjusting them accordingly.
# It also copies each driver and its variables, modifying them to reflect the right side (R).

import bpy

def mirror_drivers(armatureName):
    # Get the armature
    armature = bpy.data.objects[armatureName]
    
    if not armature.animation_data or not armature.animation_data.drivers:
        print("No animation data or drivers found!")
        return
    
    # Get all existing drivers first
    existing_drivers = []
    for fc in armature.animation_data.drivers:
        if '.L' in fc.data_path and 'rotation' in fc.data_path:
            existing_drivers.append({
                'path': fc.data_path,
                'index': fc.array_index,
                'expression': fc.driver.expression,
                'variables': []
            })
            
            # Store variable information
            for var in fc.driver.variables:
                var_info = {
                    'name': var.name,
                    'type': var.type,
                    'targets': []
                }
                
                for target in var.targets:
                    target_info = {
                        'id': target.id,
                        'bone_target': target.bone_target,
                        'transform_type': target.transform_type,
                        'transform_space': target.transform_space,
                        'data_path': target.data_path if target.data_path else ''
                    }
                    var_info['targets'].append(target_info)
                    
                existing_drivers[-1]['variables'].append(var_info)
    
    print(f"Found {len(existing_drivers)} drivers to mirror")
    
    # Now create the right side drivers
    for driver_info in existing_drivers:
        # Create the right side path
        right_path = driver_info['path'].replace('.L', '.R')
        
        # Remove existing driver if it exists
        existing = [fc for fc in armature.animation_data.drivers if fc.data_path == right_path and fc.array_index == driver_info['index']]
        for fc in existing:
            armature.animation_data.drivers.remove(fc)
        
        # Create new driver
        new_driver = armature.animation_data.drivers.new(right_path)
        new_driver.array_index = driver_info['index']
        
        # Set up the driver
        drv = new_driver.driver
        drv.type = 'SCRIPTED'
        drv.expression = driver_info['expression'].replace('.L', '.R')
        
        # Set up variables
        for var_info in driver_info['variables']:
            new_var = drv.variables.new()
            new_var.name = var_info['name']
            new_var.type = var_info['type']
            
            # Set up targets
            for i, target_info in enumerate(var_info['targets']):
                if i < len(new_var.targets):
                    new_target = new_var.targets[i]
                    new_target.id = target_info['id']
                    if target_info['bone_target']:
                        new_target.bone_target = target_info['bone_target'].replace('.L', '.R')
                    new_target.transform_type = target_info['transform_type']
                    new_target.transform_space = target_info['transform_space']
                    if target_info['data_path']:
                        new_target.data_path = target_info['data_path'].replace('.L', '.R')
        
        print(f"Created driver for {right_path}[{driver_info['index']}]")

# Run the function
try:
    mirror_drivers("Armature")
    print("Driver mirroring completed successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
