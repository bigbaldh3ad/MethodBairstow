from django.db import models

class BairstowRegistro(models.Model):
    ecuacion = models.CharField(max_length=255)
    r_inicial = models.FloatField()
    s_inicial = models.FloatField()
    tolerancia = models.FloatField()
    max_iter = models.IntegerField()
    raices = models.TextField()  
    fecha = models.DateTimeField(auto_now_add=True)
    grafica = models.CharField(max_length=255, blank=True, null=True)  

    def __str__(self):
        return f'{self.ecuacion} - {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'
