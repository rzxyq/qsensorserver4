from django.conf.urls import url, include
from .views import *

urlpatterns = [
        url(r'^results/$', Results.as_view()),
        url(r'^eda_view/$',ResultView.as_view()), # To receive 
        url(r'^mean_view/$',ResultView_mean.as_view()), # To receive 
        url(r'^frequency_view/$',ResultView_frequency.as_view()), # To receive 
        url(r'^sums_view/$',ResultView_sums.as_view()), # To receive 


        url(r'^post_data$', post_data), # To receive data POSTs 

        url(r'^post_graph$', post_graph), # To receive graph POSTs
        url(r'^sums_post_graph$', sums_post_graph), # Ajax in results.js calls this to get JSON data back
        url(r'^frequency_post_graph$', frequency_post_graph), # To receive graph POSTs
        url(r'^mean_post_graph$', mean_post_graph), # To receive graph POSTs

]