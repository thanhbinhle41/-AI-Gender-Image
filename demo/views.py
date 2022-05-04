from django.shortcuts import render
from django.forms import ModelForm
from .models import ImageHolder
from django.views.generic import View
from predict import predict


class ImageForm(ModelForm):
    class Meta:
        model = ImageHolder
        fields = ['img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update({"id":"file", "type":"file", "onchange":"previewFile(this);","required":True})

# Create your views here.

class IndexView(View):
    def get(self, request):
        form = ImageForm()
        msg ="OK"
        return render(request, "index.html", {"form": form, "msg": msg, "img":"media/unknow.jpg","predict":"media/unknow.jpg"})
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        msg ="OK"

        if form.is_valid():
            img = form.cleaned_data.get("img")
            imageHolder = ImageHolder.objects.create(img = img)
            imageHolder.save()
            predict(imageHolder.img.name)

            msg ="predict.jpg"

        return render(request, "index.html", {"form": form, "msg": msg, "img": "media/"+imageHolder.img.name ,"predict":"media/predict.jpg"})
