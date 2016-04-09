from django.db import models
#https://docs.djangoproject.com/en/1.9/topics/db/examples/many_to_one/
# python manage.py shell
# from data_.models import Trial, Data
#from django.utils import timezone
# t1 = Trial(1, 'first trial', datetime.date.today()) #1 at beginning is pk
# d1 = Data(1, 9,0.18,0.78,0.75,3.95,32.6,0.167, 0.267,0.167,2, data_text='9,0.18,0.78,0.75,3.95,32.6,0.167', date_time=timezone.now(), trial=t1)
# t1.data_set.all()

# Used to manage Data objects and group into one setting
class Trial(models.Model): 
    num = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    date = models.DateField()
    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.num, self.name)
    class Meta:
        ordering = ['num']

# Used for recording basic data 
class Data(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.date_time, self.eda)
    # Seconds on data incoming 
    seconds = models.FloatField(null=True, 
                                                                verbose_name="Seconds",
                                                                default=0)
    # x-coordinate 
    x_coord = models.FloatField(null=True, 
                                                                verbose_name="X",
                                                                default=0)
    # y-coordinate 
    y_coord = models.FloatField(null=True, 
                                                                verbose_name="Y", 
                                                                default=0)
    # z-coordinate 
    z_coord = models.FloatField(null=True,
                                                                verbose_name="Z",
                                                                default=0)
    # Unknown metric 
    unknown = models.FloatField(null=True,
                                                                verbose_name="Unknown",
                                                                default=0)
    # Temperature 
    temp = models.FloatField(null=True,
                                                         verbose_name="Temperature",
                                                         default=0)
    # Electrodermal Activity (eda)
    eda = models.FloatField(null=True,
                                                        verbose_name="EDA",
                                                        default=0)
    sums = models.FloatField(null=True,
                                                        verbose_name="Sum",
                                                        default=0)

    mean = models.FloatField(null=True,
                                                        verbose_name="Sum",
                                                        default=0)
    frequency = models.FloatField(null=True,
                                                        verbose_name="Sum",
                                                        default=0)
    # The raw tuple of the information flowing in 
    data_text = models.CharField(null=False, 
                                                             verbose_name="Piece of data",
                                                             max_length=270)
    date_time = models.DateTimeField()
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE, verbose_name="trial this point belongs to")

