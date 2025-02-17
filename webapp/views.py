import numpy as np
import os
from keras.preprocessing import image
from keras.models import load_model
from tensorflow.compat.v1 import Session
from tensorflow import Graph
model_graph = Graph()
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn import svm

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CreateUserForm


# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    total_customers = customers.count()
    return render(request, 'accounts/index.html')

@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html')


def productss(request):

    #Region_Id12 = int(request.GET['pclass'])
    import numpy as np
    from sklearn.neighbors import KNeighborsClassifier
    model1 = KNeighborsClassifier(n_neighbors=1)
    X1 = [[1, 2], [1, 1], [1, 3],[1, 4],[1,5]]
    y1 = ['2', '1', '3','4','5']
    model1.fit(X1, y1)
    Region_Id123 = int(request.POST.dict()['regionss'])
    Region_Id12=int(request.POST.dict()['regions'])

    print(Region_Id12)
    print(request.POST.dict()['regions'], 'This is post region')
    k = np.array([Region_Id123, Region_Id12])
    k1 = k.reshape(1, -1)
    predict1 = model1.predict(k1)
    print((predict1))

    if predict1 == "1":
        return render(request, "accounts/konk.html")

    elif predict1 == "2":
        return render(request, "accounts/marat.html")

    elif predict1 == "3":
        return render(request, "accounts/vidar.html")

    elif predict1 == "4":
        return render(request, "accounts/pune.html")

    elif predict1 == "5":
        return render(request, "accounts/nashik.html")

with model_graph.as_default():
	tf_session = Session()
	with tf_session.as_default():
		pass
		model = load_model("webapp/weights_crop.h5")

IMG_WIDTH = 224
IMG_HEIGHT = 224

X = [[3, 1], [1,1],[2,1],[0,1],[3,0],[1,0],[2,0],[0,0],[3,2],[1,2],[2,2],[0,2],[3,3],[1,3],[2,3],[0,3],[3,4],[1,4],[2,4],[0,4]]
y =['0', '1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19']

clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(X, y)

@login_required(login_url='login')
def predictImage(request):
    print(request.POST.dict(),'This is post')
    Region_Id=int(request.POST.dict()['region'])
    print(Region_Id, "this is my region number")
    print(request.POST.dict()['region'], 'This is post region')
    fileObj = request.FILES["document"]
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    test_image = "." + filePathName
    print(test_image)
    img = image.load_img(test_image, target_size=(IMG_WIDTH, IMG_HEIGHT, 3))
    img = img_to_array(img)
    img = img / 255
    x = img.reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
    region1 = (request.GET.dict())
    print(type(region1), "this is region")
    for item in region1:
        print("Key : {} , Value : {}".format(item, region1[item]))

    with model_graph.as_default():
        with tf_session.as_default():
            result = np.argmax(model.predict(x))
            print((result,"This is my cnn output it is nothing but soil color"))
            result1=clf.predict([[result, Region_Id]])
            print(result1)
            #print(type(result1))
            if result1 == "0":
                #print(classes["0"])
                print("Red.html/a1")
                return render(request, "accounts/a1.html")

            elif result1 == "1":
                #print(classes["1"])
                print("Black.html/b1")
                return render(request, "accounts/b1.html")

            elif result1 == "2":
                #print(classes["2"])
                print("Clay.html/c1")
                return render(request, "accounts/c1.html")

            elif result1 == "3":
                #print(classes["3"])
                print("Alluvial.html/d1")
                return render(request, "accounts/d1.html")

            elif result1 == "4":
                #print(classes["4"])
                print("Red.html/a2")
                return render(request, "accounts/a2.html")

            elif result1 == "5":
                #print(classes["5"])
                print("Black.html/b2")
                return render(request, "accounts/b2.html")

            elif result1 == "6":
                #print(classes["6"])
                print("Clay.html/c2")
                return render(request, "accounts/c2.html")

            elif result1 == "7":
                #print(classes["7"])
                print("Alluvial.html/d2")
                return render(request, "accounts/d2.html")

            elif result1 == "8":
                #print(classes["8"])
                print("Red.html/a3")
                return render(request, "accounts/a3.html")

            elif result1 == "9":
                #print(classes["9"])
                print("Black.html/b3")
                return render(request, "accounts/b3.html")

            elif result1 == "10":
                #print(classes["10"])
                print("Clay.html/c3")
                return render(request, "accounts/c3.html")

            elif result1 == "11":
                #print(classes["11"])
                print("Alluvial.html/d3")
                return render(request, "accounts/d3.html")

            elif result1 == "12":
                #print(classes["8"])
                print("Red.html/a4")
                return render(request, "accounts/a4.html")

            elif result1 == "13":
                #print(classes["9"])
                print("Black.html/b4")
                return render(request, "accounts/b4.html")

            elif result1 == "14":
                #print(classes["14"])
                print("Clay.html/c4")
                return render(request, "accounts/c4.html")

            elif result1 == "15":
                #print(classes["15"])
                print("Alluvial.html/d4")
                return render(request, "accounts/d4.html")

            elif result1 == "16":
                #print(classes["16"])
                print("Red.html/a5")
                return render(request, "accounts/a5.html")

            elif result1 == "17":
                #print(classes["17"])
                print("Black.html/b5")
                return render(request, "accounts/b5.html")

            elif result1 == "18":
                #print(classes["19"])
                print("Clay.html/c5")
                return render(request, "accounts/c5.html")

            elif result1 == "19":
                #print(classes["19"])
                print("Alluvial.html/d5")
                return render(request, "accounts/d5.html")
