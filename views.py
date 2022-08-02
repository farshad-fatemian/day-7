from django.shortcuts import get_object_or_404, render , redirect
from .models import Product , Comments
# Create your views here.
from .forms import Buy , CommentForm , ProductForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    
    context = {
        "products" : list(products),
    }
    return render(request,"product/furn-master/List_final.html",context)






def product_detail(request,id):
    
    selected_product = get_object_or_404(Product,id=id)
    
    AllComments = list(selected_product.comments.all())
    
    if selected_product.available :
        buy_form = Buy(quantity_m = selected_product.number)
    else :
        buy_form = False    
        
    #comment part
    
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.writer = request.user
            obj.product = selected_product
            obj.save()
            return HttpResponseRedirect(request.path_info)
    else :
        form = CommentForm()
        
        
        
    
    context = {
        "s_product" : selected_product ,
        "buy_form1" : buy_form ,
        "s_comments" : AllComments,
        "form" : form ,
    }
    return render(request,"product/product_detail.html",context)

#edit product part

@login_required
def product_update(request,id):
    selected_product = get_object_or_404(Product,id=id)
    if request.user == selected_product.seller:
        form = ProductForm(request.POST or None,instance=selected_product)
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                # return HttpResponseRedirect("/"+"product/"+str(id))
                return redirect('product:product_list')
        else:
            form = ProductForm(instance=selected_product)
        context ={
            "form":form,
            "product":selected_product
        }
        return render(request,"product/product_update.html",context)
    else:
        HttpResponseForbidden
        
        
@login_required
def comment_update(request,id):
    selected_comment = get_object_or_404(Comments,id=id)
    if request.user == selected_comment.writer:
        form = CommentForm(request.POST or None,instance=selected_comment)
        if request.method == "POST" :
            if form.is_valid():
                form.save()
                # return HttpResponseRedirect("/"+"product/"+str(id))
                return redirect('product:product_list')
        else:
            form = CommentForm(instance=selected_comment)
        context ={
            "form":form,
            "comment":selected_comment
        }
        return render(request,"product/comment_update.html",context)
    else:
        HttpResponseForbidden
            
    
    