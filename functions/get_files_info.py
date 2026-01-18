import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        target_items = os.listdir(target_dir)
        files_info = []
        for i in target_items:
            filepath = os.path.join(target_dir, i)
            file_size = os.path.getsize(filepath)
            is_file = os.path.isdir(filepath)

            files_info.append(
              f"- {i}: file_size={file_size}, is_dir={is_file}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"