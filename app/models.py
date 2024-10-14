from django.db import models

# Create your models here.



class Client(models.Model):
    FREQUENCY_CHOICES = [
        ('Mensuel', 'Mensuel'),
        ('Trimestriel', 'Trimestriel'),
        ('Semestriel', 'Semestriel'),
        ('Annuel', 'Annuel')
    ]
    CREDIT_TYPE_CHOICES = [
        ("véhicules particuliers de tourisme", "véhicules particuliers de tourisme"),
        ("cycles et tricycles à moteur", "cycles et tricycles à moteur"),
        ("informatique, téléphonie, electroménager, téléviseurs, meubles, accessoires en bois, tissues d'ameublement", 
         "informatique, téléphonie, electroménager, téléviseurs, meubles, accessoires en bois, tissues d'ameublement")
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10)
    revenu = models.FloatField()
    age = models.IntegerField()
    revenue_codebiteur = models.FloatField(null=True, blank=True)
    age_codebiteur = models.IntegerField(null=True, blank=True)
    type_credit = models.CharField(max_length=1000, choices=CREDIT_TYPE_CHOICES)
    frequence = models.CharField(max_length=1000, choices=FREQUENCY_CHOICES)
    duree = models.IntegerField()
    hamish_jiddiya=models.FloatField(null=True, blank=True)
    credit=models.FloatField()
    def __str__(self):
        return f"{self.nom} {self.prenom}"
 
class Admin(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
     