from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pojazdy.forms import PojazdyForm, EditPojazdyForm
from pojazdy.models import Pojazdy, Baterie
from django.views import View
from django.template.defaulttags import register




@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class PojazdyDetails(View):
    def get(self, request):
        pojazdy = Pojazdy.objects.all()
        batDict = {}
        for p in pojazdy:
            if p.baterie.all():
                batDict[p] = 0
                for b in p.baterie.all():
                    if b.on:
                        batDict[p] += 1
        batDictAll = {}
        for p in pojazdy:
            if p.baterie.all():
                batDictAll[p] = 0
                for _ in range(len(p.baterie.all())):
                    batDictAll[p] += 1
        return render(request, 'pojazdy_details.html', {
            'pojazdy': pojazdy,
            'batDict': batDict,
            'batDictAll': batDictAll,
           })


class NowyPojazd(View):
    def get(self, request):
        return render(request, 'nowy_pojazd.html', {
})

    def post(self, request):
        userID = request.POST['userID']
        nazwa = request.POST['nazwa']
        baterie = request.POST['baterie']
        p = Pojazdy.objects.create(userID=userID, nazwa=nazwa)
        counter = 1
        counterID = 5
        for _ in range(int(baterie)):
            b = Baterie.objects.create(numer=counter, batID=counterID)
            b.inpojazd = p
            b.save()
            counter += 1
            counterID += 2
        return redirect("/pojazdy")


class EdytujPojazd(View):
    def get(self, request, pojazd_id):
        pojazd = Pojazdy.objects.get(id=pojazd_id)
        pojazdy = Pojazdy.objects.all()
        baterieAll = len(pojazd.baterie.all())
        baterieON = len(pojazd.baterie.filter(on=True))
        return render(request, 'edytuj_pojazd.html', {
            'pojazdy': pojazdy,
            'pojazd': pojazd,
            'baterieON': baterieON,
            'baterieAll': baterieAll,
})

    def post(self, request, pojazd_id):
        p = Pojazdy.objects.get(id=pojazd_id)
        p.userID = request.POST['userID']
        p.nazwa = request.POST['nazwa']
        p.save()
        if request.POST.getlist('doON'):
            a = request.POST.getlist('doON')
            aOn = p.baterie.all().filter(on=False)
            y = []
            for i in range(len(a)):
                if a[i] == 'ON':
                    y.append(i)
            z = []
            for i in y:
                idON = aOn[i].id
                z.append(idON)
            for i in z:
                x = Baterie.objects.get(id=i)
                x.on = True
                x.save()
        if request.POST.getlist('doOFF'):
            a = request.POST.getlist('doOFF')
            aOff = p.baterie.all().filter(on=True)
            y = []
            for i in range(len(a)):
                if a[i] == 'OFF':
                    y.append(i)
            z = []
            for i in y:
                idOFF = aOff[i].id
                z.append(idOFF)
            for i in z:
                x = Baterie.objects.get(id=i)
                x.on = False
                x.save()

        if request.POST.getlist('batDel'):
            a = request.POST.getlist('batDel')
            for i in a:
                x = Baterie.objects.get(id=int(i))
                x.delete()
        if request.POST['baterie'] != "Bez zmian":
            if len(p.baterie.all()) > 0:
                listBat = []
                batAll = p.baterie.all()
                for i in batAll:
                    listBat.append(i)
                counter = (listBat[-1].batID) + 1
                counterID = (listBat[-1].batID) + 2
                for _ in range(int(request.POST['baterie'])):
                    b = Baterie.objects.create(numer=counter, batID=counterID)
                    b.inpojazd = p
                    b.save()
                    counter += 1
                    counterID += 2
            else:
                p = Pojazdy.objects.get(id=pojazd_id)
                counter = 1
                counterID = 5
                for _ in range(int(request.POST['baterie'])):
                    b = Baterie.objects.create(numer=counter, batID=counterID)
                    b.inpojazd = p
                    b.save()
                    counter += 1
                    counterID += 2
                return redirect("/pojazdy")
        return redirect("/pojazdy")

################################################

class AddPojazdView(View):
    def get(self, request):
        ctx = {
            'form': PojazdyForm,
        }
        return render(request, 'add_pojazd.html', ctx)

    def post(self, request):
        form = PojazdyForm(request.POST)
        if form.is_valid():
            pojazd = Pojazdy.objects.create(
                userID=form.cleaned_data['userID'],
                nazwa=form.cleaned_data['nazwa'],
                )
            baterie = request.POST['baterie']
            counter = 1
            counterID = 5
            for _ in range(int(baterie)):
                b = Baterie.objects.create(numer=counter, batID=counterID)
                b.inpojazd = pojazd
                b.save()
                counter += 1
                counterID += 2
            return HttpResponseRedirect(
                reverse('pojazdy-details')
            )
        ctx = {
            'form': PojazdyForm,
        }
        return render(request, 'add_pojazd.html', ctx)


class EditPojazdyView(View):
    def get(self, request, pojazd_id):
        pojazd = Pojazdy.objects.get(pk=pojazd_id)
        form = EditPojazdyForm(initial={
            'userID': pojazd.userID,
            'nazwa': pojazd.nazwa,
            'baterie': len(pojazd.baterie.all()),
            'baterie_on': Baterie.objects.filter(inpojazd_id=pojazd_id),
            'pojazd_id': pojazd_id
        })
        ctx = {
            'form': form,

            }
        return render(request, 'edit_pojazd.html', ctx)