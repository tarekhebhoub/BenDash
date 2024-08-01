# views.py
from rest_framework import viewsets
from .models import Customer, Product, Invoice, Payment,InvoiceItem
from .serializers import CustomerSerializer, ProductSerializer, InvoiceSerializer, PaymentSerializer,InvoiceItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from datetime import datetime
from dateutil.relativedelta import relativedelta



# Input date string
def changeDate(date_str):

# Parse the input string to a datetime object
# Note: The 'Z' at the end of the string indicates UTC time
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

# Format the datetime object to the desired string format
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


def increment_date_by_months(date_str, months):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    # Parse the input date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Add the specified number of months to the date object
    new_date = date_obj + relativedelta(months=months)
    
    # Return the new date as a string in the desired format
    return new_date.strftime("%Y-%m-%d")
# Example usage




@api_view(['Get'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def GetVentes(request):
    invoices=Invoice.objects.all()
    ventes=InvoiceSerializer(invoices,many=True)
    data=[]
    for invoice in ventes.data:
        date_dub=datetime.strptime(invoice['date_dub'], "%Y-%m-%dT%H:%M:%SZ")
        date_dub=date_dub.strftime("%Y-%m-%d")
        date_fin = increment_date_by_months(date_dub, int(invoice['installment_period'])-1)
        invoice["date_fin"]=date_fin
        invoice["date_dub"]=date_dub
        created_at=datetime.strptime(invoice['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        created_at=created_at.strftime("%Y-%m-%d")
        invoice['created_at']=created_at
        customer=Customer.objects.get(id=invoice['customer'])
        invoice['customer_Name']=customer.name
        invoice['customer_CCP']=customer.ccp

        payments=Payment.objects.filter(invoice=invoice['id'])
        paymentSerializer=PaymentSerializer(payments,many=True)
        
        prix_Vente=0
        invoiceItems=InvoiceItem.objects.filter(invoice=invoice['id'])
        Items_Serializer=InvoiceItemSerializer(invoiceItems,many=True)
        for item in Items_Serializer.data:
            prix_Vente=prix_Vente+float(item['total_price'])
        invoice['prix_Vente']="{:.2f}".format(prix_Vente)
        prix_Vente=prix_Vente-(float(invoice['remise'])+float(invoice['init_amount']))
        invoice['prix_Final']="{:.2f}".format(prix_Vente)
        mententPrelvement=prix_Vente/int(invoice['installment_period'])
        invoice['mententPrelvement']="{:.2f}".format(mententPrelvement)
        total=0
        for payment in paymentSerializer.data:
            total=total+float(payment['amount'])
        rest=prix_Vente-total
        invoice["rest"]="{:.2f}".format(rest)
        data.append(invoice)    
    return Response(data)





@api_view(['Get'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def GetVenteDetails(request,pk):
    invoices=Invoice.objects.get(id=pk)
    vente=InvoiceSerializer(invoices)
    invoice=vente.data
    date_dub=datetime.strptime(invoice['date_dub'], "%Y-%m-%dT%H:%M:%SZ")
    date_dub=date_dub.strftime("%Y-%m-%d")
    date_fin = increment_date_by_months(date_dub, int(invoice['installment_period']))
    invoice["date_fin"]=date_fin
    invoice["date_dub"]=date_dub
    created_at=datetime.strptime(invoice['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    created_at=created_at.strftime("%Y-%m-%d")
    invoice['created_at']=created_at
    customer=Customer.objects.get(id=invoice['customer'])
    invoice['customer_Name']=customer.name
    invoice['customer_CCP']=customer.ccp

    payments=Payment.objects.filter(invoice=invoice['id'])
    paymentSerializer=PaymentSerializer(payments,many=True)
    
    
    prix_Vente=0
    invoiceItems=InvoiceItem.objects.filter(invoice=invoice['id'])
    Items_Serializer=InvoiceItemSerializer(invoiceItems,many=True)
    for item in Items_Serializer.data:
        prix_Vente=prix_Vente+float(item['total_price'])
    invoice['prix_Vente']="{:.2f}".format(prix_Vente)
    prix_Vente=prix_Vente-(float(invoice['remise'])+float(invoice['init_amount']))

    invoice['prix_Final']="{:.2f}".format(prix_Vente)
    mententPrelvement=prix_Vente/int(invoice['installment_period'])
    mententPrelvement="{:.2f}".format(mententPrelvement)
    invoice['mententPrelvement']=mententPrelvement
    total=0
    for payment in paymentSerializer.data:
        total=total+float(payment['amount'])
    rest=float(invoice['prix_Final'])- float(total)
    invoice["rest"]="{:.2f}".format(rest)
    products=InvoiceItem.objects.filter(invoice=invoice['id'])
    products=InvoiceItemSerializer(products,many=True)
    invoice['products']=products.data

    installments=[]
    i=0
    for payment in paymentSerializer.data:
        payment['mententPrelvement']=mententPrelvement
        payment['dateVente']=increment_date_by_months(invoice['date_dub'],i)
        payment['payment_date']=changeDate(payment['payment_date'])
        i+=1
        installments.append(payment)
    # print(installments)
    if len(installments)<int(invoice['installment_period']):
        x=int(invoice['installment_period'])-len(installments)
        for j in range(x):
            payment = {
                'invoice': invoice['id'],
                'mententPrelvement': mententPrelvement,
                'amount': None,
                'payment_date': None,
                'dateVente': increment_date_by_months(date_dub, i + j)
            }
            installments.append(payment)


    invoice['installments']=installments
    # print(installments)

    return Response(invoice)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Create_invoice_with_products(request):
    """
    Create a new invoice and add products to it, all from a single request.
    """
    invoice_data = request.data

    # Extract the products data from the request
    products_data = invoice_data.pop('products', [])
    print(invoice_data)
    # # Remove 'total_price' from each product data
    # for product_data in products_data:
    #     if 'total_price' in product_data:
    #         del product_data['total_price']
    # print(products_data)

    # Create the invoice
    invoice_serializer = InvoiceSerializer(data=invoice_data)
    if invoice_serializer.is_valid():
        invoice = invoice_serializer.save()  # Save the invoice and get the instance
        print("-------this done--------------")
        # Process the products
        for product_data in products_data:
            product_id = product_data.get('product_id')
            quantity = product_data.get('quantity', 1)
            total_price=product_data.get('total_price')

            if not product_id:
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create the InvoiceItem
            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                total_price=total_price
            )

        # Serialize the updated invoice
        updated_invoice_serializer = InvoiceSerializer(invoice)
        return Response(updated_invoice_serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(invoice_serializer.errors)
        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def postPaiment(request):
#     serializer=PaymentSerializer(request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return {"Done"}
#     else:
#         return serializer.error

@api_view(['Get'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def tryToken(request):
    return Response({'tarek'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Get the user's token
        token = Token.objects.get(user=request.user)
        # Delete the token to effectively log out the user
        token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)

