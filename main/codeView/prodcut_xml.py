from django.shortcuts import render

def product_xml_page(request):
    prd_code1 = request.GET.get('product[0][id]')
    #prd_code2 = request.GET.get('product[1][id]')
    xml_file = ""
    #
    # if prd_code1 is not None and prd_code2 is not None and prd_code1 is not prd_code2:
    #     xml_file = "all"
    if prd_code1 is not None:
        xml_file = prd_code1
    # elif prd_code1 is not None:
    #     xml_file = prd_code2

    context = {
        "xml_file": xml_file,
    }

    return render(request, 'product/xml.html', context)
    # # Create XML
    # root = etree.Element("products")
    #
    # if prd_code is not None:
    #     prd_detail = select_class(prd_code)
    #     if prd_detail.count() > 0 :
    #         # Set product
    #         x_product = etree.Element("product")
    #
    #         # Set id
    #         x_id = etree.SubElement(x_product, "id")
    #         x_id.text = prd_detail[0].prd_code
    #
    #         # Set name
    #         x_name = etree.SubElement(x_product, "name")
    #         x_name.text = prd_detail[0].title
    #
    #         # Set basePrice
    #         x_basePrice = etree.SubElement(x_product, "basePrice")
    #         x_basePrice.text = str(prd_detail[0].price)
    #
    #         # Set taxType
    #         x_taxType = etree.SubElement(x_product, "taxType")
    #
    #         # Set infoUrl
    #         x_infoUrl = etree.SubElement(x_product, "infoUrl")
    #         x_infoUrl.text = "http://runcoding.co.kr/detail_prd/?prd_code=" + prd_detail[0].prd_code
    #
    #         x_imageUrl = etree.SubElement(x_product, "imageUrl")
    #         x_imageUrl.text = "http://runcoding.co.kr/" + prd_detail[0].img
    #
    #         x_status = etree.SubElement(x_product, "status")
    #         x_status.text = "ON_SALE"
    #
    #         x_supplement = etree.SubElement(x_product, "supplement")
    #         x_groupId = etree.SubElement(x_supplement, "groupId")
    #         x_groupId.text = prd_detail[0].prd_code + "_1"
    #
    #         x_supp_name = etree.SubElement(x_supplement, "name")
    #         x_supp_name.text = prd_detail[0].option1
    #
    #         x_supp_price = etree.SubElement(x_supplement, "price")
    #         x_supp_price.text = str(prd_detail[0].option1_price)
    #
    #         x_supp_stockQuantity = etree.SubElement(x_supplement, "stockQuantity")
    #         x_supp_stockQuantity.text = "1"
    #
    #         x_supp_status = etree.SubElement(x_supplement, "status")
    #         x_supp_status.text = "1"
    #
    #         x_shippingPolicy = etree.SubElement(x_product, "shippingPolicy")
    #         x_sip_groupId = etree.SubElement(x_shippingPolicy, "groupId")
    #
    #         x_sip_method = etree.SubElement(x_shippingPolicy, "method")
    #         x_sip_method.text = "DELIVERY"
    #
    #         x_sip_feeType = etree.SubElement(x_shippingPolicy, "feeType")
    #         x_sip_feeType.text = "CHARGE"
    #
    #         x_sip_feePayType = etree.SubElement(x_shippingPolicy, "feePayType")
    #         x_sip_feePayType.text = "PREPAYED"
    #
    #         x_sip_feePrice = etree.SubElement(x_shippingPolicy, "feePrice")
    #         x_sip_feePrice.text = "3000"
    #
    #         root.append(x_product)
    #
    #
    # if prd_code2 is not None:
    #     prd_detail = select_class(prd_code2)
    #     if prd_detail.count() > 0:
    #         # Set product
    #         x_product2 = etree.Element("product")
    #
    #         # Set id
    #         x_id = etree.SubElement(x_product2, "id")
    #         x_id.text = prd_detail[0].prd_code
    #
    #         # Set name
    #         x_name = etree.SubElement(x_product2, "name")
    #         x_name.text = prd_detail[0].title
    #
    #         # Set basePrice
    #         x_basePrice = etree.SubElement(x_product2, "basePrice")
    #         x_basePrice.text = str(prd_detail[0].price)
    #
    #         # Set taxType
    #         x_taxType = etree.SubElement(x_product2, "taxType")
    #
    #         # Set infoUrl
    #         x_infoUrl = etree.SubElement(x_product2, "infoUrl")
    #         x_infoUrl.text = "http://runcoding.co.kr/detail_prd/?prd_code=" + prd_detail[0].prd_code
    #
    #         x_imageUrl = etree.SubElement(x_product2, "imageUrl")
    #         x_imageUrl.text = "http://runcoding.co.kr/" + prd_detail[0].img
    #
    #         x_status = etree.SubElement(x_product2, "status")
    #         x_status.text = "ON_SALE"
    #
    #         x_supplement = etree.SubElement(x_product2, "supplement")
    #         x_groupId = etree.SubElement(x_supplement, "groupId")
    #         x_groupId.text = prd_detail[0].prd_code + "_1"
    #
    #         x_supp_name = etree.SubElement(x_supplement, "name")
    #         x_supp_name.text = prd_detail[0].option1
    #
    #         x_supp_price = etree.SubElement(x_supplement, "price")
    #         x_supp_price.text = str(prd_detail[0].option1_price)
    #
    #         x_supp_stockQuantity = etree.SubElement(x_supplement, "stockQuantity")
    #         x_supp_stockQuantity.text = "1"
    #
    #         x_supp_status = etree.SubElement(x_supplement, "status")
    #         x_supp_status.text = "1"
    #
    #         x_shippingPolicy = etree.SubElement(x_product2, "shippingPolicy")
    #         x_sip_groupId = etree.SubElement(x_shippingPolicy, "groupId")
    #
    #         x_sip_method = etree.SubElement(x_shippingPolicy, "method")
    #         x_sip_method.text = "DELIVERY"
    #
    #         x_sip_feeType = etree.SubElement(x_shippingPolicy, "feeType")
    #         x_sip_feeType.text = "CHARGE"
    #
    #         x_sip_feePayType = etree.SubElement(x_shippingPolicy, "feePayType")
    #         x_sip_feePayType.text = "PREPAYED"
    #
    #         x_sip_feePrice = etree.SubElement(x_shippingPolicy, "feePrice")
    #         x_sip_feePrice.text = "3000"
    #
    #         root.append(x_product2)
    #
    #
    # # Print
    # x_output = etree.tostring(root, pretty_print=True, encoding='UTF-8', xml_declaration=True)
    # # ff = open('static/resource/data/xml/sample.xml', 'w', encoding='UTF-8')
    # # ff.write(x_output.decode('utf-8'))
    #
    #
    # return HttpResponse(x_output)
