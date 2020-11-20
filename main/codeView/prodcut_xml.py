from xml import etree
from xml.etree.ElementTree import Element, SubElement, dump

from django.shortcuts import render

from main.query import *


def product_xml_page(request):
    prd_code1 = request.GET.get('product[0][id]', "")

    # if prd_code1 is not None:
    #     xml_file = "all"

    prd_code2 = request.GET.get('product[1][id]', "")
    xml_file = ""

    if prd_code1 is not "" and prd_code2 is not "":
        xml_file = "all"
    elif prd_code1 is not None:
        xml_file = prd_code1
    elif prd_code2 is not None:
        xml_file = prd_code2

    context = {
        "xml_file": xml_file,
    }

    return render(request, 'product/xml.html', context)

def make_xml(order_info):
    # Create XML
    root = Element("products")

    for order in order_info:
        prd_code = order.prd.prd_code
        print(prd_code)
        prd_detail = select_prd(prd_code)
        if prd_detail.count() > 0 :

            x_merchantId = Element("merchantId")  # 상품 ID. 네이버페이에 가입 승인될 때 정해진다.
            x_merchantId.text = ''

            x_certiKey = Element("certiKey")  # 인증키. 네이버페이에 가입 승인될 때 정해진다.
            x_certiKey.text = ''


            # Set product
            x_product = Element("product")

            # Set id
            x_id = SubElement(x_product, "id")
            x_id.text = prd_detail[0].prd_code

            # Set name
            x_name = SubElement(x_product, "name")
            x_name.text = prd_detail[0].title

            # Set basePrice
            x_basePrice = SubElement(x_product, "basePrice")
            x_basePrice.text = str(prd_detail[0].price)

            # Set infoUrl
            x_infoUrl = SubElement(x_product, "infoUrl")
            x_infoUrl.text = "http://runcoding.co.kr/detail_prd/?prd_code=" + prd_detail[0].prd_code

            x_imageUrl = SubElement(x_product, "imageUrl")
            x_imageUrl.text = "http://runcoding.co.kr/" + prd_detail[0].img

            # x_status = SubElement(x_product, "status")
            # x_status.text = "ON_SALE"

            #supplement - 추가옵션구매
            x_supplement = SubElement(x_product, "supplement")

            x_groupId = SubElement(x_supplement, "groupId")
            x_groupId.text = prd_detail[0].prd_code + "_1"

            x_supp_name = SubElement(x_supplement, "name")
            x_supp_name.text = prd_detail[0].option1

            if prd_detail[0].option1_price > 0 :
                x_supp_price = SubElement(x_supplement, "price")
                x_supp_price.text = str(prd_detail[0].option1_price)

            x_supp_quantity = SubElement(x_supplement, "quantity")
            x_supp_quantity.text = str(order.count)

            #shipping
            x_shippingPolicy = SubElement(x_product, "shippingPolicy")

            x_sip_groupId = SubElement(x_shippingPolicy, "groupId")
            x_sip_groupId.text = "sipping_" + order.pay_num

            x_sip_method = SubElement(x_shippingPolicy, "method")
            x_sip_method.text = "DELIVERY"

            x_sip_feeType = SubElement(x_shippingPolicy, "feeType")
            x_sip_feeType.text = "CHARGE"

            x_sip_feePayType = SubElement(x_shippingPolicy, "feePayType")
            x_sip_feePayType.text = "PREPAYED"

            x_sip_feePrice = SubElement(x_shippingPolicy, "feePrice")
            x_sip_feePrice.text = str(order.delivery_price)

            #backUrl
            x_backUrl  = SubElement(x_product, "backUrl")
            x_backUrl.text = "http://runcoding.co.kr/order/"

            root.append(x_product)



    # Print
    # x_output = etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True)
    dump(root)
    # ff = open('static/resource/data/xml/sample.xml', 'w', encoding='UTF-8')
    # ff.write(x_output.decode('utf-8'))

    return root


