from enum import Enum
import time
import requests
import os
import json

## Parameters
class ConvertType(Enum):
    PDF = "PDF"
    IMAGE = "IMAGE"
class ImageFormat(Enum):
    JPEG = "JPEG"
    PNG = "PNG"


# host = 'http://211.45.70.89/upstage'
# path = '/file/upload'
# #file_path = 'data/1.hwp'
# file_path = 'data/sin_1.hwp'
# files = {'file': open(file_path, 'rb')}
# # Use the enum instead of string literal
# data = {
#     'convertType': ConvertType.IMAGE.value,
#     'imageFormat': ImageFormat.JPEG.value,
# }

# response = requests.post(host + path, data=data, files=files)
# convert_request = response.json()

# if convert_request['success']:
#     convert_status_path = "/file/convert/" + convert_request['id']
#     while True:
#         print(f"Checking convert status of {convert_request['id']}...")
#         convert_status_response = requests.get(host + convert_status_path)
#         convert_status = convert_status_response.json()
#         if convert_status['status'] == 'S' or convert_status['status'] == 'F':
#             break
#         time.sleep(0.3)

#     '''
#     if convert_status['status'] == 'S':
#         download_path = "/file/download/" + convert_request['id'] + ".zip"
#         download_response = requests.post(host + download_path, data={'id':convert_request['id'] , 'stamp': convert_request['stamp']})
#         with open(f"converted/{convert_request['id']}.zip", "wb") as f:
#             f.write(download_response.content)
#     else:
#         print("Error to download converted file.", convert_status.dumps())
# 	'''

#     image_result_to_pdf_path = "/file/upload/imageResultToPdf"
#     image_result_to_pdf_data = {'ids': convert_request['id'], 'stamps': convert_request['stamp']}
#     image_result_to_pdf_request = requests.post(host + image_result_to_pdf_path, data=image_result_to_pdf_data)
    
#     image_result_to_pdf_response = image_result_to_pdf_request.json() 

#     convert_status_path = "/file/convert/" + image_result_to_pdf_response['id']
#     while True:
#         print(f"Checking PDF merge status of {image_result_to_pdf_response['id']}...")
#         convert_status_response = requests.get(host + convert_status_path)
#         convert_status = convert_status_response.json()
#         if convert_status['status'] == 'S' or convert_status['status'] == 'F':
#             break
#         time.sleep(0.3)

#     if convert_status['status'] == 'S':
#         download_path = "/file/download/" + image_result_to_pdf_response['id'] + ".pdf"
#         download_response = requests.post(host + download_path, data={'id': image_result_to_pdf_response['id'] , 'stamp': image_result_to_pdf_response['stamp']})
#         with open(f"converted/{image_result_to_pdf_response['id']}.pdf", "wb") as f:
#             f.write(download_response.content)
#     else:
#         print("Error to download PDF merge file.", convert_status.dumps())
# else:
#     print("Error to submit convert request.", convert_request.dumps())


# 1. convert to pdf
root_dir = '/Users/mncm/dev/polaris'

def find_hwp_files(root_dir):
    hwp_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.hwp', '.hwpx')):
                hwp_files.append(os.path.join(root, file))
    return hwp_files


def find_converted_pdf_files(file_path):
    # Replace /hwp/ with /pdf/ in the path and change extension to .pdf
    pdf_path = file_path.replace('/hwp/', '/pdf/').replace('.hwp', '.pdf').replace('.hwpx', '.pdf')
    # Check if the PDF file exists at the converted path
    return os.path.exists(pdf_path), pdf_path


def convert_hwp_to_image_pdf(file_path):
    host = 'http://211.45.70.89/upstage'
    files = {'file': open(file_path, 'rb')}
    upload_path = '/file/upload'
    data = {
        'convertType': ConvertType.IMAGE.value,
        'imageFormat': ImageFormat.JPEG.value,
    }

    # 이미지 변환 요청
    response = requests.post(host + upload_path, data=data, files=files)
    convert_request = response.json()

    if convert_request['success']:
        convert_status_path = "/file/convert/" + convert_request['id']
        while True:
            print(f"Checking convert status of {convert_request['id']}...")
            convert_status_response = requests.get(host + convert_status_path)
            convert_status = convert_status_response.json()
            if convert_status['status'] == 'S' or convert_status['status'] == 'F':
                break
            time.sleep(0.3)

        '''
        if convert_status['status'] == 'S':
            download_path = "/file/download/" + convert_request['id'] + ".zip"
            download_response = requests.post(host + download_path, data={'id':convert_request['id'] , 'stamp': convert_request['stamp']})
            with open(f"converted/{convert_request['id']}.zip", "wb") as f:
                f.write(download_response.content)
        else:
            print("Error to download converted file.", convert_status.dumps())
        '''

        # pdf 로 머지 변환 요청
        image_result_to_pdf_path = "/file/upload/imageResultToPdf"
        image_result_to_pdf_data = {'ids': convert_request['id'], 'stamps': convert_request['stamp']}
        image_result_to_pdf_request = requests.post(host + image_result_to_pdf_path, data=image_result_to_pdf_data)
        
        image_result_to_pdf_response = image_result_to_pdf_request.json() 

        convert_status_path = "/file/convert/" + image_result_to_pdf_response['id']
        while True:
            print(f"Checking PDF merge status of {image_result_to_pdf_response['id']}...")
            convert_status_response = requests.get(host + convert_status_path)
            convert_status = convert_status_response.json()
            if convert_status['status'] == 'S' or convert_status['status'] == 'F':
                break
            time.sleep(0.3)

        pdf_file_path = f"converted/{image_result_to_pdf_response['id']}.pdf"
        if convert_status['status'] == 'S':
            download_path = "/file/download/" + image_result_to_pdf_response['id'] + ".pdf"
            download_response = requests.post(host + download_path, data={'id': image_result_to_pdf_response['id'] , 'stamp': image_result_to_pdf_response['stamp']})
            with open(pdf_file_path, "wb") as f:
                f.write(download_response.content)

            return pdf_file_path
        else:
            print("Error to download PDF merge file.", convert_status.dumps())
            return ""
    else:
        print("Error to submit convert request.", convert_request.dumps())
        return ""



def convert_hwp_to_pdf(file_path):
    host = 'http://211.45.70.89/upstage'
    files = {'file': open(file_path, 'rb')}
    upload_path = '/file/upload'
    data = {
        'convertType': ConvertType.PDF.value,
    }

    # 이미지 변환 요청
    response = requests.post(host + upload_path, data=data, files=files)
    convert_request = response.json()

    if convert_request['success']:
        convert_status_path = "/file/convert/" + convert_request['id']
        while True:
            print(f"Checking convert status of {convert_request['id']}...")
            convert_status_response = requests.get(host + convert_status_path)
            convert_status = convert_status_response.json()
            if convert_status['status'] == 'S' or convert_status['status'] == 'F':
                break
            time.sleep(0.3)

        if convert_status['status'] == 'S':
            download_path = "/file/download/" + convert_request['id'] + ".pdf"
            pdf_path = f"converted/{convert_request['id']}.pdf"
            download_response = requests.post(host + download_path, data={'id':convert_request['id'] , 'stamp': convert_request['stamp']})
            with open(pdf_path, "wb") as f:
                f.write(download_response.content)
            return pdf_path
        else:
            print("Error to download converted file.", convert_status.dumps())
            return ""
    else:
        print("Error to submit convert request.", convert_request.dumps())
        return ""

# 2. dp inference
def dp_inference(pdf_path, ocr):
    api_key = "up_fe227fdMPlobX7RfYIEce61oWG4xB"  # ex: up_xxxYYYzzzAAAbbbCCC
    
    url = "https://api.upstage.ai/v1/document-ai/document-parse"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    files = {"document": open(pdf_path, "rb")}
    response = requests.post(url, headers=headers, files=files, data={"ocr": ocr, "output_formats": "['html', 'text']"})
    
    return response.json()

def save_result(result, name):
    with open(f"{root_dir}/benchmark/result/{name}.json", "w") as f:
        f.write(json.dumps(result, ensure_ascii=False))

# 3. text extraction. html extraction 

# 4. dp inference (pdf)

# 5. load inference result and compare

hwp_files = find_hwp_files(root_dir)
files = []
for hwp in hwp_files:
    has_pdf, hancom_pdf = find_converted_pdf_files(hwp)
    if has_pdf:
        polaris_image_pdf = convert_hwp_to_image_pdf(hwp)
        polaris_pdf = convert_hwp_to_pdf(hwp)
        if (polaris_image_pdf != "" and polaris_pdf != ""):
            files.append([hancom_pdf, polaris_image_pdf, polaris_pdf])
    else:
        print(f"No converted PDF found for {hwp}")

print (files)

for (hancom_pdf, polaris_image_pdf, polaris_pdf) in files:
    hancom_name = os.path.basename(hancom_pdf)
    polaris_name = os.path.basename(polaris_pdf)

    hancom_ocr_result = dp_inference(hancom_pdf, "force")
    save_result(hancom_ocr_result, polaris_name + ".ocr.hancom");

    polaris_ocr_result = dp_inference(polaris_image_pdf, "force")
    save_result(polaris_ocr_result, polaris_name + ".ocr.polaris");

    hancom_result = dp_inference(hancom_pdf, "auto")
    save_result(hancom_result, polaris_name + ".digital.hancom");
    polaris_result = dp_inference(polaris_pdf, "auto")
    save_result(polaris_result, polaris_name + "digital.polaris");

    f = open(f"{root_dir}/benchmark/result/{polaris_name}.{hancom_name}.result", "w")
    f.write("done")
    f.close()

    print(f"Saved results for {hancom_name} and {polaris_name}")