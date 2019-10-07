'''Qu'est-ce que cette "SECRET_KEY" ? Est-elle obligatoire ?

La "Secret Key", clé secrète en français, permet de générer toutes les données chiffrées.
Par exemple, elle permet de générer les cookies.

Elle est donc obligatoire ! Il faut également garder cette clé de manière confidentielle.
Pour les besoins du cours, vous y avez accès. Mais dans le cas d'une "vraie" application, la clé ne doit en aucun cas être
accessible par d'autres personnes. Concrètement, il s'agit simplement d'une chaîne de caractères aléatoire qui peut être
générée avec le code indiqué en commentaires. Il existe également des sites qui génèrent des clés (MiniWebTool par exemple).
'''


# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])
#SECRET_KEY = "r0$+jvz9_3_m1bmxvd_zxu1pxnvut5!8n5h5y*vmnc-64uyvkk"

#FB_APP_ID = 1200420960103822


