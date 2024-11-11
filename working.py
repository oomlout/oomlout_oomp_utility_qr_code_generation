import os
import yaml
import glob
import copy
import jinja2    
import time
import qrcode


# local oomp file
utility_name = os.path.dirname(__file__)
#grab last directry before filename in utility_name
utility_name = utility_name.split("\\")[-1]
test_filename = f"configuration\\{utility_name}_configuration.yaml"
if os.path.exists(test_filename):
    file_configuration = test_filename
else:
    #default config file
    folder_configuration = "configuration"
    #add this files current loaction to the folder
    folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
    file_configuration = os.path.join(folder_configuration, "configuration.yaml")
    #import templates
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)

pass   

 
    




def main(**kwargs):
    
    
    folder = kwargs.get("folder", f"os.path.dirname(__file__)/parts")
    folder = folder.replace("\\","/")
    
    kwargs["file_template_list"] = configuration
    print(f"oomlout_oomp_utility_label_generation for folder: {folder}")
    create_recursive(**kwargs)
    
def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    filter = kwargs.get("filter", "")
    count = 0
    for item in os.listdir(folder):
        if filter in item:
            item_absolute = os.path.join(folder, item)
            if os.path.isdir(item_absolute):
                #if working.yaml exists in the folder
                if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                    kwargs["directory"] = item_absolute
                    create(**kwargs)
                    count += 1
                    if count % 100 == 0:
                        print(f"count: {count}")

def create(**kwargs):
    directory = kwargs.get("directory", os.getcwd())    
    kwargs["directory"] = directory
    file_template_list = kwargs.get("configuration", configuration)
    kwargs["configuration"] = file_template_list
    generate_qr_code_generic(**kwargs)
    

def generate_qr_code_generic(**kwargs):
    import os
    directory = kwargs.get("directory",os.getcwd())    
    configuration = kwargs.get("configuration", "")
    
    pass 
    #load working.yaml from directory
    with open(os.path.join(directory, "working.yaml"), 'r') as stream:
        try:
            working = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)
    
    # qr code for each entry in configuration
    for item in configuration:
        tag_id = item["id"]
        tag_data = working.get(tag_id, "")
        web_link = item.get("web_link", "http://oom.lt")
        web_make = item.get("web", False)
        file_name_base = item.get("file_name", f"qr_code\\{tag_id}")
        if tag_data != "":
            file_name = f"{file_name_base}.png"
            file_name_web = f"{file_name_base}_web.png"
            #add directory to file_name
            file_name = os.path.join(directory, file_name)
            file_name_web = os.path.join(directory, file_name_web)

            codes = []
            codes.append([tag_data, file_name])
            if web_make:
                codes.append([f"{web_link}/{tag_data}", file_name_web])

            for code in codes:
                #generate qr code
                data = code[0]
                f_name = code[1]
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=0,
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                #make directory if it does not exist

                os.makedirs(os.path.dirname(f_name), exist_ok=True)
                img.save(f_name)
                pass
        else:
            print(f"tag_id: {tag_id} not found in working.yaml")
            #wait 10 seconds
            
            time.sleep(10)



        #print(item)
        #print(item["label"])
        #print(item["template





if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    #folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    folder = "Z:\\oomlout_oomp_current_version_fast_test\\parts"
    kwargs["folder"] = folder
    main(**kwargs)