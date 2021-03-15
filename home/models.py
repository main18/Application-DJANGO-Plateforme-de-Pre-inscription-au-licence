from django.db import models

# Create your models here.

class Departement(models.Model):
    CodeDept = models.CharField(primary_key=True, max_length=60)
    NomDep = models.CharField(max_length=100)
    
class ResponsableLPs(models.Model):
    CodeResponsable = models.CharField(primary_key=True, max_length=60)
    NomResponsable = models.CharField(max_length=100)
    PrenomResponsable = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Telephone = models.CharField(max_length=12)
    
class LPs(models.Model):
    CodeLP = models.CharField(primary_key=True, max_length=60)
    NomLP = models.CharField(max_length=60)
    CodeDept = models.ForeignKey(Departement, on_delete=models.CASCADE)
    CodeResponsable = models.ForeignKey(ResponsableLPs, on_delete=models.CASCADE)
    
class TypesBac(models.Model):
    CodeBac = models.CharField(primary_key=True, max_length=100)
    NomBac = models.CharField(max_length=100, null=True)
    
class LPs_Bac(models.Model):
    CodeLP = models.ForeignKey(LPs, on_delete=models.CASCADE)
    CodeBac = models.ForeignKey(TypesBac, on_delete=models.CASCADE)
    
class Bac_Mention(models.Model):
    Mention = models.CharField(primary_key=True, max_length=60)
    
class Villes(models.Model):
    Nom_Ville = models.CharField(primary_key=True, max_length=60)
    
class DiplomeBacPlus2(models.Model):
    CodeDiplome = models.CharField(primary_key=True, max_length=60)
    NomDiplomeBacPlus2 = models.CharField(max_length=60)
    NatureDiplome = models.CharField(max_length=60, null=True)
    
class LPs_DiplomeBacPlus2(models.Model):
    CodeLP = models.ForeignKey(LPs, on_delete=models.CASCADE)
    CodeDiplomeBacPlus2 = models.ForeignKey(DiplomeBacPlus2, on_delete=models.CASCADE)
    
class Lycee_Academie(models.Model):
    CodeLycee = models.CharField(primary_key=True, max_length=60)
    NomLycee = models.CharField(max_length=60)
    Academie = models.CharField(max_length=60)
    Ville = models.CharField(max_length=60)
    
class EtablissementDipBacPlus2(models.Model):
    codeEtablissement = models.CharField(primary_key=True, max_length=60)
    EtablissementDipBacPlus2 = models.CharField(max_length=60)
    Ville = models.CharField(max_length=60)
    
class Specialites_DiplomeBacPlus2(models.Model):
    spécialite_Option = models.CharField(primary_key=True, max_length=60)
    
class Candidats(models.Model):
    CIN_OU_Passport = models.CharField(primary_key=True, max_length=100)
    CNE_OU_Massar = models.CharField(max_length=100)
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    DateNaissance = models.CharField(max_length=100)
    Nationalite = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Telephone1 = models.CharField(max_length=12)
    Telephone2 = models.CharField(max_length=12)
    Adresse = models.CharField(max_length=100)
    Ville = models.CharField(max_length=100)
    CodeBac = models.ForeignKey(TypesBac, on_delete=models.CASCADE, null=True)
    Annee_Obtention_Bac = models.CharField(max_length=4, null=True)
    MentionBac = models.CharField(max_length=100, null=True)
    Lycee = models.ForeignKey(Lycee_Academie, on_delete=models.CASCADE,null=True)
    Academie = models.CharField(max_length=100, null=True)
    CodeDiplomeBacPlus2 = models.ForeignKey(DiplomeBacPlus2, on_delete=models.CASCADE,null=True)
    Annee_Obtention_DiplomeBacPlus2 = models.CharField(max_length=100, null=True)
    DureeObtentionDiplomeBacPlus2 = models.CharField(max_length=100, null=True)
    Specialite_Diplome = models.CharField(max_length=100, null=True)
    Dominance_Diplome = models.CharField(max_length=100, null=True)
    EtablissementDipBacPlus2 = models.CharField(max_length=100, null=True)
    Ville_DiplomeBacPlus2 = models.CharField(max_length=100, null=True)
    Annee_Obtention_1ereAnnee = models.CharField(max_length=10, null=True)
    Note_1ere_Annee_Diplome = models.FloatField(max_length=10, null=True)
    Note_2eme_Annee_Diplome = models.FloatField(max_length=10, null=True)
    Note_Obtention_Diplome = models.CharField(max_length=10, null=True)
    Note_Semestre1 = models.FloatField(max_length=10, null=True)
    Note_Semestre2 = models.FloatField(max_length=10, null=True)
    Note_Semestre3 = models.FloatField(max_length=10, null=True)
    Note_Semestre4 = models.FloatField(max_length=10, null=True)
    CodeLPChoisie = models.CharField(max_length=100, null=True)
    
    
class Annee(models.Model):
    annee = models.CharField(max_length=10)