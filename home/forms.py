from django import forms
from .models import LPs, TypesBac, Bac_Mention, Annee, Lycee_Academie, DiplomeBacPlus2, EtablissementDipBacPlus2, Villes, Specialites_DiplomeBacPlus2


class loginForm(forms.Form):
    CIN = forms.CharField(max_length=60, label="CIN", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Entrer votre CIN'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Entrer votre mot de passe'}), max_length=100,label="Password")

class homeForm(forms.Form):
    CHOICES=[("Preinscription","Preinscription"),
         ("Modification d'anciennes Informations","Modification d'anciennes Informations")]
    action = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class':'form-check-input'}))

class InfoPersonelForm(forms.Form):
    CIN = forms.CharField(max_length=100,label='CIN ou, N°, Passeport(*)')
    CNE = forms.CharField(label='CNE ou N° MASSAR')
    Nom = forms.CharField(label='Nom(*)')
    Prenom = forms.CharField(max_length=100, label='Prénom(*)')
    DateNaissance = forms.DateField(label='Date de Naissance(*)')
    Nationalite = forms.CharField(label='Nationalité(*)',)
    Email = forms.EmailField(label='Email(*)')
    Tel1 = forms.CharField(label='Télephone 1(*)')
    Tel2 = forms.CharField(label='Télephone 2(*)')
    Adresse = forms.CharField(label='Adresse(*)')
    Ville = forms.CharField(label='Ville(*)')
    MDP1 = forms.CharField(max_length=32, widget=forms.PasswordInput, label="Mot de passe(*)")
    MDP2 = forms.CharField( max_length=32, widget=forms.PasswordInput, label="Confirmer le mot de passe(*)")

class ChoixLicenceForm(forms.Form):
    type_choices = [(i['NomLP'], i['NomLP']) for i in LPs.objects.values('NomLP')]
    choix_licence = forms.ChoiceField(choices=type_choices, label="Sélectionnez une licence")
    
class infoBacForm(forms.Form):
    type_bac = forms.ModelChoiceField(queryset=TypesBac.objects.values_list('CodeBac', flat=True), label="Quel votre type de bac")
    AutreField = forms.CharField(required=False, max_length=100, widget= forms.TextInput(attrs={'class':'autreField'}), label="Autre")
    mention_bac_choices = [(i['Mention'], i['Mention']) for i in Bac_Mention.objects.values('Mention')]
    mention_bac = forms.ChoiceField(choices=mention_bac_choices, label="Mention du Bac")
    annee_obtention_bac_choices = [(i['annee'], i['annee']) for i in Annee.objects.values('annee')]
    annee_obtention_bac = forms.ChoiceField(choices=annee_obtention_bac_choices, label="Année Obtention Bac")
    lycee_bac_choices = [(i['NomLycee'], i['NomLycee']) for i in Lycee_Academie.objects.values('NomLycee')]
    lycee_obtention_bac = forms.ChoiceField(choices=lycee_bac_choices, label="Lycee d'obtention du bac")
    academie_choices = [(i['Academie'], i['Academie']) for i in Lycee_Academie.objects.values('Academie')]
    academie = forms.ChoiceField(choices=academie_choices, label="Academie")

class infoDipPlus2Form(forms.Form):
    diplomebacplus2 = forms.ModelChoiceField(queryset=DiplomeBacPlus2.objects.values_list('CodeDiplome', flat=True), label="Quel est votre diplome Bac + 2")
    AutreFieldDip2 = forms.CharField(required=False, max_length=100, widget= forms.TextInput(attrs={'class':'autreField2'}), label="Autre diplome")
    anneeObtentionDiplomebacplus2_choices = [(i['annee'], i['annee']) for i in Annee.objects.values('annee')]
    anneeObtentionDiplomebacplus2 = forms.ChoiceField(choices=anneeObtentionDiplomebacplus2_choices, label="Année Obtention Diplome Bac + 2")
    EtablissementDipBacPlus2_choices = [(i['EtablissementDipBacPlus2'], i['EtablissementDipBacPlus2']) for i in EtablissementDipBacPlus2.objects.values('EtablissementDipBacPlus2')]
    EtablissementBacPlus2 = forms.ChoiceField(choices=EtablissementDipBacPlus2_choices, label="Etablissement Diplome Bac + 2")
    VilleDipBacPlus2_choices = [(i['Nom_Ville'], i['Nom_Ville']) for i in Villes.objects.values('Nom_Ville')]
    VilleDipBacPlus2 = forms.ChoiceField(choices=VilleDipBacPlus2_choices, label="Ville Diplome Bac + 2")
    Specialite_choices = [(i['spécialite_Option'], i['spécialite_Option']) for i in Specialites_DiplomeBacPlus2.objects.values('spécialite_Option')]
    Specialite = forms.ChoiceField(choices=Specialite_choices, label="Spécialité ou option diplome")
    dominanceDiplome = forms.CharField(required=False, label="Dominance Diplome") 
    
class resultatDipPlus2Form(forms.Form):
    Annee1ereDiplome_choices =  [(i['annee'], i['annee']) for i in Annee.objects.values('annee')]
    Annee1ereDiplome = forms.ChoiceField(required=True, choices=Annee1ereDiplome_choices, label="Annee 1ere annee diplome :")
    AnneeObtention = forms.ChoiceField(required=True, choices=Annee1ereDiplome_choices, label="Annee Obtention diplome :")
    DureeObtention = forms.IntegerField(required=True, label="Duree Obtention Diplome :")
    #DUT + BTS
    Note1ereS = forms.FloatField(required=False, label="Note 1ere annee :") 
    Note2emeS = forms.FloatField(required=False, label="Note 2eme annee :") 
    #DTS
    NoteObtention = forms.FloatField(required=False, label="Note Obtention Diplome :")
    #DEUG + DEUST + DEUT 
    NoteS1 = forms.FloatField(required=False, label="Note Semestre 1 :") 
    NoteS2 = forms.FloatField(required=False, label="Note Semestre 2 :") 
    NoteS3 = forms.FloatField(required=False, label="Note Semestre 3 :") 
    NoteS4 = forms.FloatField(required=False, label="Note Semestre 4 :") 
   

