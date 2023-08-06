from django.contrib import admin
from djangosubscribe.models import QuickEmailSubscriptionModel
from djangosubscribe.models import BasicInformationModel
from djangosubscribe.models import EducationalInformationModel
from djangosubscribe.models import WorkInformationModel
from djangosubscribe.models import ParentalInformationModel
from djangosubscribe.models import CategoryModel
from djangosubscribe.modeladmins import QuickEmailSubscriptionModelAdmin
from djangosubscribe.modeladmins import BasicInformationModelAdmin
from djangosubscribe.modeladmins import EducaionalInformationModelAdmin
from djangosubscribe.modeladmins import WorkInformationModelAdmin
from djangosubscribe.modeladmins import ParentalInformationModelAdmin
from djangosubscribe.modeladmins import CategoryModelAdmin


# Register your models here.
admin.site.register(QuickEmailSubscriptionModel, QuickEmailSubscriptionModelAdmin)
admin.site.register(BasicInformationModel, BasicInformationModelAdmin)
admin.site.register(EducationalInformationModel, EducaionalInformationModelAdmin)
admin.site.register(WorkInformationModel, WorkInformationModelAdmin)
admin.site.register(ParentalInformationModel, ParentalInformationModelAdmin)
admin.site.register(CategoryModel, CategoryModelAdmin)