"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from sbi import views #  import home

urlpatterns = [
    path('', views.SBIBankView.as_view(), name='sbi_challan'),
    path('delete_challan/', views.DeleteChallanView.as_view(), name='delete_challan'),
    path('depositor/add/', views.addDepositorView.as_view()),
    path('depositor/delete/<int:pk>/', views.deleteDepositorView.as_view()),
    path('applicant/add/', views.addApplicantView.as_view()),
    path('applicant/delete/<int:pk>/', views.deleteApplicantView.as_view()),
    
    path('otherbanks/', views.OtherBankView.as_view(), name='otherbank_challan'),


    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/<int:pk>/', views.AccountEditView.as_view(), name="account-detail"),

    path('otherbankaccount/', views.OtherbankAccountView.as_view(), name='otherbankaccount'),
    path('otherbankaccount/<int:pk>/', views.OtherbankAccountEditView.as_view()),
    path('ajax_ifsc/', views.IFSCView.as_view(), name='ajax_ifsc'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'sbi.views.custom_page_not_found_view'
handler500 = 'sbi.views.custom_error_view'