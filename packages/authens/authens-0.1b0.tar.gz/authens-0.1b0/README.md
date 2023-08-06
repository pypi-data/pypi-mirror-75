# AuthENS

Librairie Django pour l'authentification via le CAS élèves à l'ENS.

AuthENS fournit une page de connexion qui laisse le choix entre "Connexion par
CAS" et "Connexion par mot de passe".
De plus, elle gère de façon transparente les potentiels "conflits" de `username`
liés aux comptes Django standards non-CAS (1) et aux vieux comptes clippers (2).
Plus précisément :

1. Si un compte clipper `dupond` est créé alors qu'un compte Django standard
   avec le `username` `dupond` existait déjà, le compte nouvellement créé
   obtient un `username` différent (typiquement `dupond2`).
   La personne détentrice du compte continue de se connecter en tant que
   `dupond` sur le CAS élèves mais devra utiliser le nom `dupond2` lorsqu'elle
   choisira d'utiliser la connexion par mot de passe sur le site, typiquement
   après la fin de la scolarité lorsque le compte clipper est supprimé.

2. Si, quelques années plus tard, après que `dupond` a terminé sa scolarité, le
   SPI donne le login `dupond` à une nouvelle personne, AuthENS détecte que le
   nouveau compte `dupond` n'est pas le même que l'ancien et crée un nouveau
   compte (par exemple `dupond3`).
   Le compte `dupond3` peut se connecter par CAS en tant que `dupond` et le
   compte `dupond2` ne peut plus se connecter que par mot de passe.


## Configuration

### Urls

Vous devez rendre les pages de connexion de AuthENS accessibles, par exemple en
ajoutant dans votre fichier d'urls :

```python
urlpatterns = [
  ...
  path("authens/", include("authens.urls")),
  ...
]
```

La page de connexion principale de AuthENS est ensuite accessible via l'url
nommée `"authens:login"`.
Par commodité, AuthENS rend accessible la page de déconnexion par défaut de
Django sous le nom `"authens:logout"`.

### Dans le fichier `settings.py`

- Ajouter `"authens"` dans les [`INSTALLED_APPS`](https://docs.djangoproject.com/en/3.0/ref/settings/#installed-apps).
- Ajouter `"authens.backends.ENSCASBackend"` dans les
  [`AUTHENTICATION_BACKENDS`](https://docs.djangoproject.com/en/3.0/ref/settings/#authentication-backends).
  Si `AUTHENTICATION_BACKENDS` n'apparaît pas dans vos settings, utiliser :

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authens.backends.ENSCASBackend",
]
```

- Préciser l'url de connexion:

```python
LOGIN_URL = reverse_lazy("authens:login")
```

- (Optionnel) AuthENS utilise le paramètre Django standard
  [`LOGIN_REDIRECT_URL`](https://docs.djangoproject.com/en/3.0/ref/settings/#login-redirect-url)
  par défaut pour rediriger l'utilisateurice en cas de connexion réussie.
  Il peut être utile de définir ce paramètre.


## Création d'utilisateurices

AuthENS maintient une tables des comptes clipper connus.
Cette table est automatiquement mise à jour lors qu'une personne se connecte via
le CAS pour la première fois.
En revanche lorsqu'un nouveau compte est créé manuellement et que ce compte
correspond à un compte clipper, il faut enregistrer ce compte auprès d'AuthENS,
autrement le compte Django et le compte clipper seront considérés comme deux
comptes différents.

**TODO:** écrire le helper qui fait une requête sur le LDAP pour trouver tout
seul la date de création de compte. Ça ressemblera à quelque chose du genre
`register_clipper(user, login_clipper)`.
