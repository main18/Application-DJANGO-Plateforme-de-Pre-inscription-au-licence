from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login", ),
    path('infopersonnelLogin/<str:CIN>/<str:is_authenticated>', views.infoPersoneLoginView, name="infopersonnelLogin"),
    path('infopersonnel', views.infoPersonelView, name="infopersonnel"),
    path('choix_licence/<str:CIN>', views.choixLicenceView, name="choix_licence"),
    path('choixLicenceLogin/<str:CIN>/<str:is_authenticated>', views.choixLicenceLoginView, name="choixLicenceLogin"),
    path('info_bac/<str:CIN>', views.infoBacView, name="info_bac"),
    path('info_bac_login/<str:CIN>/<str:is_authenticated>', views.infoBacLoginView, name="info_bac_login"),
    path('info_dip_plus2/<str:CIN>/<str:isMecatronique>', views.infoDipPlus2View, name="info_dip_plus2"),
    path('info_dip_plus2_login/<str:CIN>/<str:isMecatronique>/<str:is_authenticated>', views.infoDipPlus2LoginView, name="info_dip_plus2_login"),
    path('resultat_dip_plus2/<str:CIN>/<str:typeDiplome>', views.resultatDipPlus2View, name="resultat_dip_plus2"),
    path('resultat_dip_plus2_login/<str:CIN>/<str:typeDiplome>/<str:is_authenticated>', views.resultatDipPlus2LoginView, name="resultat_dip_plus2_login"),
    path('finInscription/<str:CIN>', views.finInscription, name="finInscription"),
    path('pdf/<str:CIN>', views.pdfDownload, name="pdf"),
]