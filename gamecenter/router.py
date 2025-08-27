from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'openingsalesbox', OpeningSalesBoxViewSet, basename='openingsalesbox')
router.register(r'person', PersonViewSet, basename='person')
router.register(r'user', UserViewSet, basename='user')
router.register(r'subsidiary', SubsidiaryViewSet, basename='subsidiary')
router.register(r'localsettings', LocalSettingsViewSet, basename='localsettings')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'lot', LotViewSet, basename='lot')
router.register(r'sessions', SessionViewSet, basename='sessions')
router.register(r'game', GameViewSet, basename='game')
router.register(r'consolemaintenance', ConsoleMaintenanceViewSet, basename='consolemaintenance')
router.register(r'sale', SaleViewSet, basename='sale')
router.register(r'saledetail', SaleDetailViewSet, basename='saledetail')
