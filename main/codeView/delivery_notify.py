import pandas as pd
from django.shortcuts import render

from main.query import *

#pip3 install xlrd
#pip3 install pandas
#pip3 install openpyxl
from pandas import DataFrame

#email 추가
from main.codeView.bizMsg import send_msg_at


def get_delivery_list(request):
    delivery_info = select_deliveryList()

    if delivery_info.count() > 0:
        server_static = 'static/resource/delivery_list/' + delivery_info[0].filename
        print(server_static)

        df = pd.read_excel(server_static, engine='openpyxl')

        print(len(df.columns)) #행 - 세로
        print(len(df.index)) #열 - 가로

        row = len(df.index)

        for data in range(0, row):
            name = (df['name'][data:data+1].item())
            number = (df['number'][data:data + 1].item())
            phone = '0' + str(number)

            email = (df['email'][data:data + 1].item())
            delivery_number = (df['delivery_number'][data:data + 1].item())

            print(name, email, phone, delivery_number)

            send_msg_at(name, email, phone, delivery_number)


        ch_delivery_info = delivery_info[0]
        ch_delivery_info.dbstat = 'D'
        ch_delivery_info.save()

    context = {
        "txt": "",
    }
    return render(request, 'runAdmin/upload_file.html', context)

