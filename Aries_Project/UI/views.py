from django.shortcuts import render

# Create your views here.

  
from django.http import HttpResponse  
from UI.functions.functions import handle_uploaded_file  
from UI.forms import DataForm
from mindee import Client, documents
import os
import mimetypes
extension = ""
file_name=""
def Base_UI(request):
    return render(request, "baseindex.html")
def Show_UI(request):
    return render(request, "index2.html")
def home(request):
    return render(request,"home.html")
def index(request):  
    global extension,file_name
    if request.method == 'POST':  
        data= DataForm(request.POST, request.FILES)  
        if data.is_valid():  
           
            extension = os.path.splitext(str(request.FILES['file']))[1]
            
            request.FILES['file'].name="invoice"+extension
            file_name=request.FILES['file'].name
            #filename= request.FILES['file'].name
            handle_uploaded_file(request.FILES['file']) 
            context={
                "extension":request.FILES['file'].name,
                "file_name":file_name}
            #os.renames("F:/Machine Learning/Django/Aries_Project/UI/static/upload/","invoice" )
            return render(request, "post_upload.html")  
           

            
            
    else:  
        data = DataForm()  
        return render(request,"index1.html",{'form':data}) 
def Show_data(request):
    mindee_client = Client(api_key="82fa11cd92e7d188119aa313957022a4")
    #input_data = mindee_client.doc_from_path("F:/Machine Learning/Django/Aries_Project/UI/static/upload/invoice.jpg")
    if file_name=="invoice.jpg":
        input_data = mindee_client.doc_from_path("F:/Machine Learning/Django/Aries_Project/UI/static/upload/invoice.jpg")
    #input_data = mindee_client.doc_from_path("C:/Users/A Kumar/Downloads/invoice.jpg")
    if file_name=="invoice.pdf":
        input_data = mindee_client.doc_from_path("F:/Machine Learning/Django/Aries_Project/UI/static/upload/invoice.pdf")
    invoice_data = input_data.parse(documents.TypeInvoiceV4)
    #print(invoice_data.http_response)
    #print(invoice_data.document)
    #customer_name = invoice_data.document.customer_name.value
    #result=invoice_data.document
    invoice_number=invoice_data.document.invoice_number
    customer_name = invoice_data.document.customer_name.value
    customer_company_registrations = invoice_data.document.customer_company_registrations
    if customer_company_registrations:
       customer_company_registrations=customer_company_registrations
    else:
       customer_company_registrations="Unknown"
    language = invoice_data.document.locale.value
    if language:
        language=language
    else:
        language="Unknown"
        
    currency = invoice_data.document.locale.currency
    supplier_company_registrations = invoice_data.document.supplier_company_registrations
    if supplier_company_registrations:
       supplier_company_registrations=supplier_company_registrations
    else:
       supplier_company_registrations="Unknown"
    supplier_name = invoice_data.document.supplier_name.value   
    if  supplier_name:
        supplier_name= supplier_name
    else:
        supplier_name="Unknown"
    customer_address = invoice_data.document.customer_address.value  
    invoice_date = invoice_data.document.invoice_date.value
    due_date = invoice_data.document.due_date.value
    """payment_details = invoice_data.document.payment_details
      # Loop on each object
    for payment_detail in payment_details:
        # To get the IBAN
        iban = payment_detail.iban

        # To get the swift
        swift = payment_detail.swift

        # To get the routing number
        routing_number = payment_detail.routing_number

        # To get the account_number
        account_number = payment_detail.account_number"""
    reference_numbers = invoice_data.document.reference_numbers
    list1=[]
    for i in reference_numbers:
        list1.append(i.value)
        
    # To get the list of taxes
    taxes = invoice_data.document.taxes

    # Loop on each Tax 
    if taxes:
        for tax in taxes:
            # To get the tax amount
            tax_amount = tax.value

            # To get the tax code for from a tax object
            tax_code = tax.code

            # To get the tax rate
            tax_rate = tax.rate
    else:
        tax_amount=None
        tax_code=None
        tax_rate=None
        
        
                
    total_amount = invoice_data.document.total_amount.value  
    total_net = invoice_data.document.total_net.value
    total_tax = invoice_data.document.total_tax.value
    line_item= invoice_data.document.line_items
    list2=[]
    line_item_dict={}
    for line_item in invoice_data.document.line_items:
       # Show just the description
       list2.append(line_item.description)
       line_item_dict[line_item.description]=line_item


    context={
        "invoice_number":invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "Customer_name":customer_name,
        "customer_company_registrations":customer_company_registrations,
        "customer_address": customer_address,
        "language":language,
        "currency":currency,
        "supplier_name": supplier_name,
        "supplier_company_registrations":supplier_company_registrations,
        "reference_numbers": list1,
        "tax_amount":tax_amount,
        "tax_code":tax_code,
        "tax_rate":tax_rate,
        "total_amount":total_amount,
        "total_net":total_net,
        "total_tax":total_tax,
        "line_item":list2,
        
        }
    
    
    with open("F:/Machine Learning/Django/Aries_Project/UI/download/download.txt", 'w') as f: 
        for key, value in context.items(): 
            f.write('%s:%s\n' % (key, value))       
        for key,value in line_item_dict.items():
            f.write('%s:%s\n' % (key, value)) 
            
    
    
    return render(request, 'index.html', context=context)


    



def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'download.txt'
    # Define the full file path
    filepath = BASE_DIR + '/UI/download/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


