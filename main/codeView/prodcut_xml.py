from xml.etree.ElementTree import Element, SubElement, dump, ElementTree

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render

from main.query import *


def product_xml_page(request):
    prd_code1 = request.GET.get('product[0][id]', "")
    prd_code2 = request.GET.get('product[1][id]', "")

    return make_xml(prd_code1, prd_code2)


def indent(elem, level=0):
    i = "\n" + level*" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            for elem in elem:
                indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



def make_xml(prd_code1, prd_code2):
    # Create XML
    root = Element("products")

    if prd_code1 is not None:
        prd_detail = select_prd(prd_code1)
        if prd_detail.count() > 0:
            # Set product
            x_product = Element("product")

            # Set id
            x_id = SubElement(x_product, "id")
            x_id.text = prd_detail[0].prd_code

            # Set name
            x_name = SubElement(x_product, "name")
            x_name.text = prd_detail[0].title

            x_basePrice = SubElement(x_product, "basePrice")
            x_basePrice.text = str(prd_detail[0].price)

            # Set infoUrl
            x_infoUrl = SubElement(x_product, "infoUrl")
            x_infoUrl.text = "http://runcoding.co.kr/detail_prd/?prd_code=" + prd_detail[0].prd_code

            x_imageUrl = SubElement(x_product, "imageUrl")
            x_imageUrl.text = "http://runcoding.co.kr" + prd_detail[0].img

            x_status = SubElement(x_product, "status")
            x_status.text = "ON_SALE"

            x_option_support = SubElement(x_product, "optionSupport")
            x_option_support.text = "true"

            #options - 추가옵션구매
            x_option = SubElement(x_product, "option")

            x_quanItem = SubElement(x_option, "optionItem")

            x_option_type = SubElement(x_quanItem, "type")
            x_option_type.text = 'SELECT'

            x_option_name = SubElement(x_quanItem, "name")
            x_option_name.text = '추가부품'

            x_option_value = SubElement(x_quanItem, "value")

            x_option_value_id = SubElement(x_option_value, "id")
            x_option_value_id.text = 'arduino'

            x_option_value_txt = SubElement(x_option_value, "text")
            x_option_value_txt.text = prd_detail[0].option1

            x_option_value_1 = SubElement(x_quanItem, "value")

            x_option_value_id_1 = SubElement(x_option_value_1, "id")
            x_option_value_id_1.text = 'noOption'

            x_option_value_txt_1 = SubElement(x_option_value_1, "text")
            x_option_value_txt_1.text = '선택없음'

            #shipping
            x_shippingPolicy = SubElement(x_product, "shippingPolicy")

            SubElement(x_shippingPolicy, "groupId")

            x_sip_method = SubElement(x_shippingPolicy, "method")
            x_sip_method.text = "DELIVERY"

            x_sip_feeType = SubElement(x_shippingPolicy, "feeType")
            x_sip_feeType.text = "CHARGE"

            x_sip_feePayType = SubElement(x_shippingPolicy, "feePayType")
            x_sip_feePayType.text = "PREPAYED"

            x_sip_feePrice = SubElement(x_shippingPolicy, "feePrice")
            x_sip_feePrice.text = "3000"

            root.append(x_product)

        if prd_code2 is not None:
            prd_detail = select_prd(prd_code2)
            if prd_detail.count() > 0:
                # Set product
                x_product = Element("product")

                # Set id
                x_id = SubElement(x_product, "id")
                x_id.text = prd_detail[0].prd_code

                # Set name
                x_name = SubElement(x_product, "name")
                x_name.text = prd_detail[0].title

                x_basePrice = SubElement(x_product, "basePrice")
                x_basePrice.text = str(prd_detail[0].price)

                # Set infoUrl
                x_infoUrl = SubElement(x_product, "infoUrl")
                x_infoUrl.text = "http://runcoding.co.kr/detail_prd/?prd_code=" + prd_detail[0].prd_code

                x_imageUrl = SubElement(x_product, "imageUrl")
                x_imageUrl.text = "http://runcoding.co.kr" + prd_detail[0].img

                x_status = SubElement(x_product, "status")
                x_status.text = "ON_SALE"

                x_option_support = SubElement(x_product, "optionSupport")
                x_option_support.text = "true"

                # options - 추가옵션구매
                x_option = SubElement(x_product, "option")

                x_quanItem = SubElement(x_option, "optionItem")

                x_option_type = SubElement(x_quanItem, "type")
                x_option_type.text = 'SELECT'

                x_option_name = SubElement(x_quanItem, "name")
                x_option_name.text = '추가부품'

                x_option_value = SubElement(x_quanItem, "value")

                x_option_value_id = SubElement(x_option_value, "id")
                x_option_value_id.text = 'arduino'

                x_option_value_txt = SubElement(x_option_value, "text")
                x_option_value_txt.text = prd_detail[0].option1

                # shipping
                x_shippingPolicy = SubElement(x_product, "shippingPolicy")

                SubElement(x_shippingPolicy, "groupId")

                x_sip_method = SubElement(x_shippingPolicy, "method")
                x_sip_method.text = "DELIVERY"

                x_sip_feeType = SubElement(x_shippingPolicy, "feeType")
                x_sip_feeType.text = "CHARGE"

                x_sip_feePayType = SubElement(x_shippingPolicy, "feePayType")
                x_sip_feePayType.text = "PREPAYED"

                x_sip_feePrice = SubElement(x_shippingPolicy, "feePrice")
                x_sip_feePrice.text = "3000"

                root.append(x_product)

        indent(root)
        dump(root)

        ElementTree(root).write("runcoding.xml", encoding="utf-8", xml_declaration=True)


    return HttpResponse(open('runcoding.xml', encoding='UTF-8').read(), content_type="application/xml")


