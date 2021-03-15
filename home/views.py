from django.shortcuts import render, HttpResponseRedirect, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User, auth , Group

from .forms import InfoPersonelForm, ChoixLicenceForm, infoBacForm, infoDipPlus2Form, resultatDipPlus2Form, homeForm, loginForm

from .models import TypesBac, Candidats, Lycee_Academie, DiplomeBacPlus2

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = homeForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data.get("action")
            if action == 'Preinscription':
                return redirect('infopersonnel')
            elif action == "Modification d'anciennes Informations": 
                return redirect('login')
            return redirect('/')
    else:
        form = homeForm()
    return render(request, 'index.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            CIN = form.cleaned_data.get("CIN")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(username=CIN,password=password)
            if user:
                auth.login(request , user)
                return redirect('infopersonnelLogin', CIN=CIN, is_authenticated='T')
            else :
                messages.error(request, 'Le CIN ou le mot de passe est incorrect!')
    else:
        form = loginForm()
    return render(request, 'login.html', {'form':form})
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def infoPersonelView(request):
    submitted = False
    if request.method == 'POST':
        form = InfoPersonelForm(request.POST)
        if form.is_valid():
            CIN = form.cleaned_data['CIN']
            CNE = form.cleaned_data['CNE']
            Nom = form.cleaned_data['Nom']
            Prenom = form.cleaned_data['Prenom']
            DateNaissance = form.cleaned_data['DateNaissance']
            Nationalite = form.cleaned_data['Nationalite']
            Email = form.cleaned_data['Email']
            Tel1 = form.cleaned_data['Tel1']
            Tel2 = form.cleaned_data['Tel2']
            Adresse = form.cleaned_data['Adresse']
            Ville = form.cleaned_data['Ville']
            MDP1 = form.cleaned_data['MDP1']
            MDP2 = form.cleaned_data['MDP2']
            if MDP1 == MDP2 :
                user = User.objects.create_user(first_name=Prenom,last_name=Nom,username=CIN,email=Email,password=MDP1)
                user.save()
            else :
                print("Les mots de pass sont pas identiques!")
            infoCandidat = Candidats(CIN_OU_Passport=CIN, CNE_OU_Massar=CNE, Nom=Nom, Prenom=Prenom, 
                                        Password=MDP1, DateNaissance = DateNaissance, Nationalite=Nationalite, 
                                        Email=Email, Telephone1=Tel1, Telephone2=Tel2, Adresse=Adresse, Ville=Ville)
            infoCandidat.save()
            if(Nationalite == "Marocaine") or (Nationalite == "marocaine"):
                TypesBac.objects.filter(CodeBac="Autre").delete()
                DiplomeBacPlus2.objects.filter(CodeDiplome="Autre").delete()
            if (Nationalite != "Marocaine") and (Nationalite != "marocaine"):   
                autreCodeBac_add = TypesBac(CodeBac="Autre")
                autreCodeBac_add.save()
                autreCodeDip_add = DiplomeBacPlus2(CodeDiplome="Autre")
                autreCodeDip_add.save()
            return redirect('choix_licence', CIN=infoCandidat.CIN_OU_Passport) 
    else:
        form = InfoPersonelForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_personnel.html', {'form': form,'submitted': submitted})

def infoPersoneLoginView(request, CIN, is_authenticated):
    submitted = False
    if request.method == 'POST':
        form = InfoPersonelForm(request.POST)
        if form.is_valid():
            CIN = form.cleaned_data['CIN']
            CNE = form.cleaned_data['CNE']
            Nom = form.cleaned_data['Nom']
            Prenom = form.cleaned_data['Prenom']
            DateNaissance = form.cleaned_data['DateNaissance']
            Nationalite = form.cleaned_data['Nationalite']
            Email = form.cleaned_data['Email']
            Tel1 = form.cleaned_data['Tel1']
            Tel2 = form.cleaned_data['Tel2']
            Adresse = form.cleaned_data['Adresse']
            Ville = form.cleaned_data['Ville']
            MDP1 = form.cleaned_data['MDP1']
            MDP2 = form.cleaned_data['MDP2']
            cinSave = Candidats.objects.get(Nom=Nom)
            cinSave.CIN_OU_Passport = CIN
            if MDP1 == MDP2 :
                user = User.objects.get(username=CIN)
                user.set_password(MDP1)
                user.save()
            info = Candidats.objects.get(CIN_OU_Passport=CIN)   
            infoCandidat = Candidats(CIN_OU_Passport=CIN, CNE_OU_Massar=CNE, Nom=Nom, Prenom=Prenom, 
                                    Password=MDP1, DateNaissance = DateNaissance, Nationalite=Nationalite, 
                                    Email=Email, Telephone1=Tel1, Telephone2=Tel2, Adresse=Adresse, Ville=Ville,
                                    CodeBac=info.CodeBac,Annee_Obtention_Bac=info.Annee_Obtention_Bac, MentionBac=info.MentionBac,
                                    Lycee=info.Lycee, Academie=info.Academie, CodeDiplomeBacPlus2=info.CodeDiplomeBacPlus2,
                                    Annee_Obtention_DiplomeBacPlus2=info.Annee_Obtention_DiplomeBacPlus2,
                                    Specialite_Diplome=info.Specialite_Diplome,  EtablissementDipBacPlus2=info.EtablissementDipBacPlus2,
                                    Ville_DiplomeBacPlus2=info.Ville_DiplomeBacPlus2, CodeLPChoisie=info.CodeLPChoisie)
            infoCandidat.save()
            if(Nationalite == "Marocaine") or (Nationalite == "marocaine"):
                TypesBac.objects.filter(CodeBac="Autre").delete()
                DiplomeBacPlus2.objects.filter(CodeDiplome="Autre").delete()
            if (Nationalite != "Marocaine") and (Nationalite != "marocaine"):
                autreCodeBac_add = TypesBac(CodeBac="Autre")
                autreCodeBac_add.save()
                autreCodeDip_add = DiplomeBacPlus2(CodeDiplome="Autre")
                autreCodeDip_add.save()
            return redirect('choixLicenceLogin', CIN=CIN, is_authenticated=is_authenticated)
    else:
        info = Candidats.objects.get(CIN_OU_Passport=CIN)
        form = InfoPersonelForm(initial={'CIN': CIN, 'CNE' : info.CNE_OU_Massar, 'Nom':info.Nom, 'Prenom':info.Prenom, 'DateNaissance':info.DateNaissance, 'Nationalite':info.Nationalite, 'Email':info.Email, 'Tel1':info.Telephone1, 'Tel2':info.Telephone2, 'Adresse':info.Adresse, 'Ville':info.Ville, 'MDP1':info.Password, 'MDP2':info.Password})
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_personnel.html', {'form': form,'submitted': submitted, 'is_authenticated':is_authenticated})


def choixLicenceView(request, CIN):
    submitted = False
    if request.method == 'POST':
        form = ChoixLicenceForm(request.POST)
        if form.is_valid():
            choix_licence = form.cleaned_data['choix_licence']
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeLPChoisie=choix_licence)
            return redirect('info_bac', CIN=CIN)
    else:
        if CIN : 
            info = Candidats.objects.get(CIN_OU_Passport=CIN)
            print(info.CodeLPChoisie)
            form = ChoixLicenceForm(initial={'choix_licence':'info.CodeLPChoisie'})
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'choix_licence.html', {'form': form,'submitted': submitted})

def choixLicenceLoginView(request, CIN, is_authenticated):
    submitted = False
    if request.method == 'POST':
        form = ChoixLicenceForm(request.POST)
        if form.is_valid():
            choix_licence = form.cleaned_data['choix_licence']
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeLPChoisie=choix_licence)
            return redirect('info_bac_login', CIN=CIN, is_authenticated=is_authenticated)
    else:
        if CIN : 
            info = Candidats.objects.get(CIN_OU_Passport=CIN)
            print(info.CodeLPChoisie)
            form = ChoixLicenceForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'choix_licence.html', {'form': form,'submitted': submitted, 'is_authenticated':is_authenticated})


def infoBacView(request, CIN):
    submitted = False
    if request.method == 'POST':
        form = infoBacForm(request.POST)
        if form.is_valid():
            type_bac = form.cleaned_data['type_bac']
            autreType_bac = form.cleaned_data['AutreField']
            autreTypeBacSubmit = TypesBac(CodeBac=autreType_bac)
            autreTypeBacSubmit.save()
            annee_obtention_bac = form.cleaned_data['annee_obtention_bac']
            mention_bac = form.cleaned_data['mention_bac']
            lycee_obtention_bac = form.cleaned_data['lycee_obtention_bac']
            academie = form.cleaned_data['academie']
            lyceeInstance = Lycee_Academie.objects.get(NomLycee=lycee_obtention_bac)
            typeBacInstance = TypesBac.objects.get(CodeBac=type_bac if not autreType_bac else autreType_bac)
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeBac=typeBacInstance,Annee_Obtention_Bac=annee_obtention_bac,MentionBac=mention_bac, Lycee=lyceeInstance, Academie=academie)
            info = Candidats.objects.get(CIN_OU_Passport=CIN)  
            if info.CodeLPChoisie == 'Mécatronique':
                return redirect('info_dip_plus2', CIN=CIN, isMecatronique=True)
            else:
                return redirect('info_dip_plus2', CIN=CIN, isMecatronique=False)
    else:
        form = infoBacForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_bac.html', {'form': form,'submitted': submitted})

def infoBacLoginView(request, CIN, is_authenticated):
    submitted = False
    if request.method == 'POST':
        form = infoBacForm(request.POST)
        if form.is_valid():
            type_bac = form.cleaned_data['type_bac']
            autreType_bac = form.cleaned_data['AutreField']
            autreTypeBacSubmit = TypesBac(CodeBac=autreType_bac)
            autreTypeBacSubmit.save()
            annee_obtention_bac = form.cleaned_data['annee_obtention_bac']
            mention_bac = form.cleaned_data['mention_bac']
            lycee_obtention_bac = form.cleaned_data['lycee_obtention_bac']
            academie = form.cleaned_data['academie']
            lyceeInstance = Lycee_Academie.objects.get(NomLycee=lycee_obtention_bac)
            typeBacInstance = TypesBac.objects.get(CodeBac=type_bac if not autreType_bac else autreType_bac)
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeBac=typeBacInstance,Annee_Obtention_Bac=annee_obtention_bac,MentionBac=mention_bac, Lycee=lyceeInstance, Academie=academie)
            info = Candidats.objects.get(CIN_OU_Passport=CIN)  
            print(info.CodeLPChoisie)
            if info.CodeLPChoisie == 'Mécatronique':
                return redirect('info_dip_plus2_login', CIN=CIN, isMecatronique=True, is_authenticated=is_authenticated)
            else:
                return redirect('info_dip_plus2_login', CIN=CIN, isMecatronique=False, is_authenticated=is_authenticated)
    else:
        form = infoBacForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_bac.html', {'form': form,'submitted': submitted, 'is_authenticated':is_authenticated})


def infoDipPlus2View(request, CIN, isMecatronique):
    submitted = False
    info = Candidats.objects.get(CIN_OU_Passport=CIN)  
    message= ""
    typeDiplome=""
    if request.method == 'POST':
        form = infoDipPlus2Form(request.POST)
        if form.is_valid():
            diplomebacplus2 = form.cleaned_data['diplomebacplus2']
            AutreFieldDip2 = form.cleaned_data['AutreFieldDip2']
            autreTypeDipSubmit = DiplomeBacPlus2(CodeDiplome=AutreFieldDip2)
            autreTypeDipSubmit.save()
            codeDipPlus2Instance = ''
            if AutreFieldDip2 == '':
                codeDipPlus2Instance = DiplomeBacPlus2.objects.get(CodeDiplome=diplomebacplus2)
            else:
                codeDipPlus2Instance = DiplomeBacPlus2.objects.get(CodeDiplome=AutreFieldDip2)
            anneeObtentionDiplomebacplus2 = form.cleaned_data['anneeObtentionDiplomebacplus2']
            EtablissementBacPlus2 = form.cleaned_data['EtablissementBacPlus2']
            VilleDipBacPlus2 = form.cleaned_data['VilleDipBacPlus2']
            Specialite = form.cleaned_data['Specialite']
            dominanceDiplome = form.cleaned_data['dominanceDiplome']
            dipPlus2 = codeDipPlus2Instance.CodeDiplome
            print(dipPlus2)
            if (dipPlus2 == "DUT" or dipPlus2 == "BTS" or dipPlus2 == "CPGE") or dipPlus2:
                if dipPlus2 != "DTS" and dipPlus2 != "DEUG" and dipPlus2 != "DEUST" and dipPlus2 != "DEUT":
                    typeDiplome = "Dut + BTS"
            if dipPlus2 == "DTS":
                typeDiplome = "DTS"
            if dipPlus2 == "DEUG" or dipPlus2 == "DEUST" or dipPlus2 == "DEUT":
                typeDiplome = "DEUG + DEUST + DEUT"
            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DEUG' or codeDipPlus2Instance.CodeDiplome == 'DUT':
                if info.CodeLPChoisie == 'Comptabilité, Finance et Audit':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2', CIN=CIN, typeDiplome=typeDiplome)
                    
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"

            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DEUG' or codeDipPlus2Instance.CodeDiplome == 'DEUST' or codeDipPlus2Instance.CodeDiplome == 'DEUT' or codeDipPlus2Instance.CodeDiplome == 'DTS' or codeDipPlus2Instance.CodeDiplome == 'DUT' or codeDipPlus2Instance.CodeDiplome == AutreFieldDip2:
                if info.CodeLPChoisie == 'Génie Industriel et Logistique' or info.CodeLPChoisie == 'Génie Logiciel et Administration Avancée des Systèmes et Rés':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2', CIN=CIN, typeDiplome=typeDiplome)
                    
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
            if codeDipPlus2Instance.CodeDiplome == 'DTS' or codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'DUT' or codeDipPlus2Instance.CodeDiplome == AutreFieldDip2:
                if info.CodeLPChoisie == 'Mécatronique':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2', CIN=CIN, typeDiplome=typeDiplome)
                    
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"

            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DUT' or codeDipPlus2Instance.CodeDiplome == 'DEUG' or codeDipPlus2Instance.CodeDiplome == AutreFieldDip2:
                if info.CodeLPChoisie == 'Marketing et Ventes':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2', CIN=CIN, typeDiplome=typeDiplome)
                    
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
        dipPlus2 = codeDipPlus2Instance.CodeDiplome
        print(dipPlus2)
        print(message)
        if (dipPlus2 == "DUT" or dipPlus2 == "BTS" or dipPlus2 == "CPGE") or dipPlus2:
            if dipPlus2 != "DTS" and dipPlus2 != "DEUG" and dipPlus2 != "DEUST" and dipPlus2 != "DEUT":
                typeDiplome = "Dut + BTS"
        if dipPlus2 == "DTS":
            typeDiplome = "DTS"
        if dipPlus2 == "DEUG" or dipPlus2 == "DEUST" or dipPlus2 == "DEUT":
            typeDiplome = "DEUG + DEUST + DEUT"
    else:
        form = infoDipPlus2Form()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_dip_plus2.html', {'form': form, 'submitted': submitted, 'isMecatronique':isMecatronique, 'message':message})

def infoDipPlus2LoginView(request, CIN, isMecatronique, is_authenticated):
    submitted = False
    info = Candidats.objects.get(CIN_OU_Passport=CIN)  
    typeDiplome=""
    message = ""
    if request.method == 'POST':
        form = infoDipPlus2Form(request.POST)
        if form.is_valid():
            diplomebacplus2 = form.cleaned_data['diplomebacplus2']
            AutreFieldDip2 = form.cleaned_data['AutreFieldDip2']
            print(diplomebacplus2)
            autreTypeDipSubmit = DiplomeBacPlus2(CodeDiplome=AutreFieldDip2)
            autreTypeDipSubmit.save()
            codeDipPlus2Instance = DiplomeBacPlus2.objects.get(CodeDiplome=diplomebacplus2 if not AutreFieldDip2 else AutreFieldDip2)
            anneeObtentionDiplomebacplus2 = form.cleaned_data['anneeObtentionDiplomebacplus2']
            EtablissementBacPlus2 = form.cleaned_data['EtablissementBacPlus2']
            VilleDipBacPlus2 = form.cleaned_data['VilleDipBacPlus2']
            Specialite = form.cleaned_data['Specialite']
            dominanceDiplome = form.cleaned_data['dominanceDiplome']
            dipPlus2 = codeDipPlus2Instance.CodeDiplome
            print(dipPlus2)
            if (dipPlus2 == "DUT" or dipPlus2 == "BTS" or dipPlus2 == "CPGE") or dipPlus2:
                if dipPlus2 != "DTS" and dipPlus2 != "DEUG" and dipPlus2 != "DEUST" and dipPlus2 != "DEUT":
                    typeDiplome = "Dut + BTS"
            if dipPlus2 == "DTS":
                typeDiplome = "DTS"
            if dipPlus2 == "DEUG" or dipPlus2 == "DEUST" or dipPlus2 == "DEUT":
                typeDiplome = "DEUG + DEUST + DEUT"
            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DEUG' or codeDipPlus2Instance.CodeDiplome == 'DUT':
                if info.CodeLPChoisie == 'Comptabilité, Finance et Audit':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2_login', CIN=CIN, typeDiplome=typeDiplome, is_authenticated=is_authenticated)
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DEUG' or codeDipPlus2Instance.CodeDiplome == 'DEUST' or codeDipPlus2Instance.CodeDiplome == 'DEUT' or codeDipPlus2Instance.CodeDiplome == 'DTS' or codeDipPlus2Instance.CodeDiplome == 'DUT':
                if info.CodeLPChoisie == 'Génie Industriel et Logistique' or info.CodeLPChoisie == 'Génie Logiciel et Administration Avancée des Systèmes et Rés':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2_login', CIN=CIN, typeDiplome=typeDiplome, is_authenticated=is_authenticated)
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
            if codeDipPlus2Instance.CodeDiplome == 'DTS' or codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'DUT':
                if info.CodeLPChoisie == 'Mécatronique':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2_login', CIN=CIN, typeDiplome=typeDiplome, is_authenticated=is_authenticated)
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
            if codeDipPlus2Instance.CodeDiplome == 'BTS' or codeDipPlus2Instance.CodeDiplome == 'CPGE' or codeDipPlus2Instance.CodeDiplome == 'DUT' or codeDipPlus2Instance.CodeDiplome == 'DEUG':
                if info.CodeLPChoisie == 'Marketing et Ventes':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2_login', CIN=CIN, typeDiplome=typeDiplome, is_authenticated=is_authenticated)
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"
                    
            if codeDipPlus2Instance.CodeDiplome:
                if info.CodeLPChoisie == 'Génie Logiciel et Administration Avancée des Systèmes et Rés':
                    infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(CodeDiplomeBacPlus2=codeDipPlus2Instance,
                            Annee_Obtention_DiplomeBacPlus2=anneeObtentionDiplomebacplus2,
                            EtablissementDipBacPlus2 = EtablissementBacPlus2, Ville_DiplomeBacPlus2=VilleDipBacPlus2, 
                            Specialite_Diplome=Specialite,Dominance_Diplome=dominanceDiplome)
                    return redirect('resultat_dip_plus2_login', CIN=CIN, typeDiplome=typeDiplome, is_authenticated=is_authenticated)
                else:
                    message = "Veuillez choisir une autre filiere ou quitter"

        
    else:
        info = Candidats.objects.get(CIN_OU_Passport=CIN)
        form = infoDipPlus2Form(initial={'dominanceDiplome':info.Dominance_Diplome})
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'info_dip_plus2.html', {'form': form, 'submitted': submitted, 'isMecatronique':isMecatronique, 'is_authenticated':is_authenticated, 'message':message})


def resultatDipPlus2View(request, CIN, typeDiplome):
    submitted = False
    if request.method == 'POST':
        form = resultatDipPlus2Form(request.POST)
        if form.is_valid():
            Annee1ereDiplome = form.cleaned_data['Annee1ereDiplome']
            AnneeObtention = form.cleaned_data['AnneeObtention'] 
            DureeObtention = form.cleaned_data['DureeObtention']
            Note1ereS = form.cleaned_data['Note1ereS']
            Note2emeS = form.cleaned_data['Note2emeS']
            NoteObtention = form.cleaned_data['NoteObtention']
            NoteS1 = form.cleaned_data['NoteS1']
            NoteS2 = form.cleaned_data['NoteS2']
            NoteS3 = form.cleaned_data['NoteS3']
            NoteS4 = form.cleaned_data['NoteS4']
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(Annee_Obtention_DiplomeBacPlus2=AnneeObtention,
                                                                                DureeObtentionDiplomeBacPlus2=DureeObtention, 
                                                                                Annee_Obtention_1ereAnnee=Annee1ereDiplome,
                                                                                Note_1ere_Annee_Diplome=Note1ereS if Note1ereS else None,
                                                                                Note_2eme_Annee_Diplome=Note2emeS if Note2emeS else None,
                                                                                Note_Semestre1=NoteS1 if NoteS1 else None,
                                                                                Note_Semestre2=NoteS2 if NoteS2 else None,
                                                                                Note_Semestre3=NoteS3 if NoteS3 else None,
                                                                                Note_Semestre4=NoteS4 if NoteS4 else None)
            return redirect('finInscription', CIN=CIN)
        else :
            print(form.errors)
    else:
        form = resultatDipPlus2Form()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'resultat_dip_plus2.html', {'form': form, 'submitted': submitted, 'typeDiplome':typeDiplome})

def resultatDipPlus2LoginView(request, CIN, typeDiplome, is_authenticated):
    print(typeDiplome)
    submitted = False
    if request.method == 'POST':
        form = resultatDipPlus2Form(request.POST)
        if form.is_valid():
            print('after Form is valid')
            Annee1ereDiplome = form.cleaned_data['Annee1ereDiplome']
            AnneeObtention = form.cleaned_data['AnneeObtention'] 
            DureeObtention = form.cleaned_data['DureeObtention']
            #DUT + BTS
            Note1ereS = form.cleaned_data['Note1ereS']
            Note2emeS = form.cleaned_data['Note2emeS']
            print(Note1ereS)
            print(Note2emeS)
            #DTS
            NoteObtention = form.cleaned_data['NoteObtention']
            #DEUG + DEUST + DEUT
            NoteS1 = form.cleaned_data['NoteS1']
            NoteS2 = form.cleaned_data['NoteS2']
            NoteS3 = form.cleaned_data['NoteS3']
            NoteS4 = form.cleaned_data['NoteS4']
            infoCandidat = Candidats.objects.filter(CIN_OU_Passport=CIN).update(Annee_Obtention_DiplomeBacPlus2=AnneeObtention,
                                                                                DureeObtentionDiplomeBacPlus2=DureeObtention, 
                                                                                Annee_Obtention_1ereAnnee=Annee1ereDiplome,
                                                                                Note_1ere_Annee_Diplome=Note1ereS if Note1ereS else None,
                                                                                Note_2eme_Annee_Diplome=Note2emeS if Note2emeS else None,
                                                                                Note_Semestre1=NoteS1 if NoteS1 else None,
                                                                                Note_Semestre2=NoteS2 if NoteS2 else None,
                                                                                Note_Semestre3=NoteS3 if NoteS3 else None,
                                                                                Note_Semestre4=NoteS4 if NoteS4 else None)
            return redirect('finInscription', CIN=CIN)
        else :
            print(form.errors)
    else:
        info = Candidats.objects.get(CIN_OU_Passport=CIN)
        form = resultatDipPlus2Form(initial={'DureeObtention':info.DureeObtentionDiplomeBacPlus2,'Note1ereS':info.Note_1ere_Annee_Diplome, 'Note2emeS': info.Note_2eme_Annee_Diplome, 'NoteObtention':info.Note_Obtention_Diplome, 'NoteS1':info.Note_Semestre1, 'NoteS2':info.Note_Semestre2,'NoteS3':info.Note_Semestre3,'NoteS4':info.Note_Semestre4})
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'resultat_dip_plus2.html', {'form': form, 'submitted': submitted, 'typeDiplome':typeDiplome, 'is_authenticated':is_authenticated})


def pdfDownload(request, CIN):
    info = Candidats.objects.get(CIN_OU_Passport=CIN)
    return render(request, 'pdf.html', {'info':info})

def finInscription(request, CIN):
    return render(request, 'fin_inscription.html', {'CIN':CIN})