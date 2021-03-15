from django.contrib import admin
from .models import Departement, ResponsableLPs, LPs, TypesBac, LPs_Bac, Bac_Mention, Villes, DiplomeBacPlus2, LPs_DiplomeBacPlus2, Lycee_Academie, EtablissementDipBacPlus2, Specialites_DiplomeBacPlus2, Candidats, Annee
#from import_export.admin import ImportExportModelAdmin
# Register your models here.


# Register your models here.

class DepartementAdmin(admin.ModelAdmin):
    list_display = ('CodeDept', 'NomDep')
    
class ResponsableLPsAdmin(admin.ModelAdmin):
    list_display = ('CodeResponsable', 'NomResponsable', 'PrenomResponsable', 'Email', 'Telephone')
    
class LPsAdmin(admin.ModelAdmin):
    list_display = ('CodeLP', 'NomLP', 'CodeDept','CodeResponsable')
    
class TypesBacAdmin(admin.ModelAdmin):
    list_display = ('CodeBac', 'NomBac')
    
class LPs_BacAdmin(admin.ModelAdmin):
    list_display = ('CodeLP', 'CodeBac')
    
class DiplomeBacPlus2Admin(admin.ModelAdmin):
    list_display = ('CodeDiplome','NomDiplomeBacPlus2', 'NatureDiplome')
    
class LPs_DiplomeBacPlus2Admin(admin.ModelAdmin):
    list_display = ('CodeLP', 'CodeDiplomeBacPlus2')
    
class Lycee_AcademieAdmin(admin.ModelAdmin):
    list_display = ('CodeLycee', 'NomLycee', 'Academie', 'Ville')
    
class EtablissementDipBacPlus2Admin(admin.ModelAdmin):
    list_display = ('codeEtablissement','EtablissementDipBacPlus2','Ville')
    
class CandidatsAdmin(admin.ModelAdmin):
    list_display = ('CIN_OU_Passport','CNE_OU_Massar','Nom', 'Prenom','Password','DateNaissance','Nationalite',
                    'Email','Telephone1','Telephone2','Adresse','Ville','CodeBac','Annee_Obtention_Bac',
                    'MentionBac','Lycee','Academie','CodeDiplomeBacPlus2','Annee_Obtention_DiplomeBacPlus2',
                    'DureeObtentionDiplomeBacPlus2','Specialite_Diplome','Dominance_Diplome',
                    'EtablissementDipBacPlus2','Ville_DiplomeBacPlus2','Annee_Obtention_1ereAnnee',
                    'Note_1ere_Annee_Diplome','Note_2eme_Annee_Diplome','Note_Obtention_Diplome',
                    'Note_Semestre1','Note_Semestre2','Note_Semestre3','Note_Semestre4','CodeLPChoisie',
                    )

    
    
admin.site.register(Departement, DepartementAdmin)
admin.site.register(ResponsableLPs, ResponsableLPsAdmin)
admin.site.register(LPs, LPsAdmin)
admin.site.register(TypesBac, TypesBacAdmin)
admin.site.register(LPs_Bac, LPs_BacAdmin)
admin.site.register(DiplomeBacPlus2, DiplomeBacPlus2Admin)
admin.site.register(LPs_DiplomeBacPlus2, LPs_DiplomeBacPlus2Admin)
admin.site.register(Lycee_Academie, Lycee_AcademieAdmin)
admin.site.register(EtablissementDipBacPlus2, EtablissementDipBacPlus2Admin)
admin.site.register(Candidats, CandidatsAdmin)
admin.site.register(Bac_Mention)
admin.site.register(Villes)
admin.site.register(Specialites_DiplomeBacPlus2)
admin.site.register(Annee)
